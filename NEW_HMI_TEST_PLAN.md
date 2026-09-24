# New OMRON HMI: debug and test plan before running it without the LAUER panel

**Situation:** the machine runs 24/7. The **LAUER panel** and the **new OMRON HMI (NS12, DB12 `HMI_DB`)** are both in use. The new HMI must be proven before it takes over alone.

**Rule for the whole plan:** keep the LAUER panel as the fallback. No PLC change is needed to start testing. Everything below can be done with a VAT and the two panels.

---

## 1. How the two panels share control

| Area | Who controls it | PLC selector |
|---|---|---|
| **Run screen:** turntable direction, flipper, hand feed, roller "goes through", clearing, and the C7/C8/C9 position timers | New HMI **when `M140.3` = 1**, LAUER when 0 | `M140.3` = `HMI_DB.ON_SW` **AND** `HMI_DB.SERVICE_SW_3_STATUS` (HMI CONTROL, line 52) |
| **Service pages** (`ALL_SERVICE_ENABLE_SW`, `SERVICE_SW_1/2/3`, all `*_TEST_SSW` / `*_PB`) | **New HMI only** | none |
| **LAUER service** (`M190.x` + keys `M161.x`, `M171.x`) | LAUER only | none |
| **Packet counts, lamps, graphics** | Written by the PLC to `HMI_DB` for the new HMI (and to `DB LAUER` for LAUER) | none |

⚠️ `M140.3` drops **by itself**: after 10 s on screen 0 the "HMI Service Switch Reset" clears `SERVICE_SW_3_STATUS` when the 2145 flap opens (`E34.7`), which happens on every packet. From that moment the run-screen functions follow the LAUER panel again. Keep this in mind for every test in §3, because it is the most likely reason for "the new HMI button does nothing".

`M140.3` affects these blocks: CONVEYOR 0 (roller REV / hand feed), CONVEYOR 7 (flipper enable, position timer), CONVEYOR 8 (turntable direction, REV time), CONVEYOR 9 (position timer), CONVEYORS CLEARING (clearing call), HMI CONTROL (hand feed, flipper, roller switches).

---

## 2. VAT for the tests ("VAT_NEW_HMI", VAT22 already exists)

Watch these while testing:

| Address | Meaning |
|---|---|
| `M 140.3` | **New HMI in control** of the run screen |
| `"HMI_DB".ON_SW`, `"HMI_DB".SERVICE_SW_3_STATUS` | The two conditions of `M140.3` |
| `"HMI_DB".ACTUAL_HMI_SCREEN_NO` | Current screen (0 = run screen) |
| `M 110.0` / `M 111.0` / `M 111.1` | Hand feed / roller "goes through" / flipper, **from the new HMI** |
| `M 152.0` / `M 152.2` / `M 152.5` | The same functions **from LAUER** |
| `M 7.3` | Turntable direction memory (1 = reverse) |
| `M 10.0` | Clearing active |
| `M 11.1` | VFD not all ready (latched) |
| `M 333.3` | 1 = FC1208 + FC8 packet counter, 0 = FC1206 + FC6 |
| `"HMI_DB".CONV_4_COUNT` … `CONV_23_COUNT` | Packet counts shown on the HMI |

---

## 3. Test checklist (one line per HMI command)

Mark each line ✅ / ❌ and add notes. "Prod" means the test can be done during production. "Stop" means it needs the station idle or in service.

### 3.1 Run screen (screen 0), which needs `M140.3` = 1
| # | HMI command | PLC field → effect | How to test | When | Known issue |
|---|---|---|---|---|---|
| R1 | ON / new HMI enable | `ON_SW` + `SERVICE_SW_3_STATUS` → `M140.3` | Set both and watch `M140.3` = 1. Stay on screen 0 for more than 10 s and let a packet come through: **`M140.3` drops** | Prod | **H1**, see §4 |
| R2 | Roller "goes through" | `ROLLER_SSW_MAIN` → `M111.0` → CONVEYOR 0 `M133.4` | Switch it on: packets go through. It is OR'd with the LAUER/desk switch `S28.3` | Prod | Up to 1.6 s delay (H3). Stays active while **either** panel has it ON |
| R3 | Hand feed | `MAN_FEED_SSW_MAIN` → `M110.0` → C0 REV path | Switch it on with the flap closed: C0 reverse runs. It times out after 20 min (`Timer 103`) | Stop | Exclusive: LAUER `M152.0` is ignored while `M140.3` = 1 |
| R4 | Flipper | `FLIPPER_SSW_MAIN` → `M111.1` → C7 `M42.0` enable | Switch on/off: `M42.0` follows at the next packet | Prod | Exclusive with LAUER `M152.5` |
| R5 | Turntable direction | `TURNTABLE_SSW_MAIN` → C8 `M46.2` → `M7.3` | Change it while no packet is on C8: `M7.3` changes at the next cycle, and `TURNTABLE_SSW_STATUS` follows | Prod | Exclusive with LAUER `M152.2` |
| R6 | Clearing | `CLEARING_SSW_MAIN` → `M5.2` → `M10.0` | Start clearing from the HMI. `CLEARING_FUNCTION` = 8 while active. Turn it off: clearing aborts (`M5.4`) | Stop (end of order) | OR'd with LAUER F4 (`M150.4`) |
| R7 | Service main switch | `SERVICE_SSW_MAIN` → `SERVICE_SSW_STATUS` | On, then off after 20 min (`Timer 101`) | Prod | — |
| R8 | New HMI ON / SIGNAL / OFF / E-STOP buttons | `E34.0` / `E34.1` / `E34.2` / `E28.7` → `M146.0..3` | ON switches control voltage on (with `S2.1`). SIGNAL = fault reset. **OFF does nothing.** E-STOP lamp `H57.3` | Stop | **H2** (OFF not wired), **H4** (lamp polarity) |

### 3.2 Position timers (new HMI values, used only when `M140.3` = 1)
| # | HMI value | Used by | How to test | Known issue |
|---|---|---|---|---|
| T1 | `CONV_9_POS_mS` | C9 → `MW184` → `Timer 62` (stops the packet on the pusher) | Change the value: the stop position on C9 changes | Value × 10 ms (not ms, whatever the comment says) |
| T2 | `CONV_8_POS_REV_mS` | C8 → `MW234` → `Timer 49` (forward run after the packet end, non-inverting) | Change the value: the packet end position on the turntable changes | Value × 10 ms |
| T3 | `CONV_7_POS_mS` | C7 → `MW186` → `Timer 60` | **Has no effect:** `Timer 60` is started but never used. Step 8N6 uses a fixed 1.5 s (`Timer 42`) | **H8**, see §4 |

### 3.3 Service pages (new HMI only: `ALL_SERVICE_ENABLE_SW` + page switch 1/2/3)
Test with the station **empty and stopped**, one conveyor at a time.

| # | Page / switch | Expected | Known issue |
|---|---|---|---|
| S1 | Page 1: C0 roller FWD/REV, Pusher 0 | Jog as long as the switch is held. FWD/REV interlocked | — |
| S2 | Page 1: Elevator service, UP/DN, round trip, Pusher 1 | Slow speed only. The brake releases only with the motor energised | Keep the LAUER panel away from `M190.0` at the same time |
| S3 | Page 1: C1 belt, C2 belt / lift / rollers, C3 slat, C4 | Runs the conveyor, disables the upstream one | Servicing C3 does **not** stop C2 (`Conveyor_2_Disable` is not read) |
| S4 | Page 2: C5, C6, C7 belt, flipper service + FLIP | FLIP holds until position reached. CW/CCW interlocked (fixed) | `SERVICE_SW_2_TIME_ADJ` is cleared every scan, so the time-adjust switch does nothing |
| S5 | Page 2: C8 turntable CW/CCW, round trip, auto-home (INIT) | Auto-home = TURNTABLE SW + INIT, 20 s max | — |
| S6 | Page 2: C9 roller, Pusher 2 | Runs/pushes, disables C8/Pusher 2 upstream | — |
| S7 | Page 2: C10 pivot service UP/DN, C10 belt | UP/DN mutually exclusive (fixed) | Servicing C11/C21 does **not** hold the pivot (`Pivot_Disable` is not read) |
| S8 | Page 2: C11/C21 (the same switch also enables C12/C13, C22/C23) | Drive test of each belt | C12/C13 have no own service switch |
| S9 | Page 3: Loader lift TOP/UP/DN, fingers extend/retract/tilt, fingers belt | Light curtain must be clear for DN / tilt / extend | `Conveyor_13/23_Disable` is written by both loader blocks |
| S10 | INIT button (`SERVICE_INIT_PB`) on each page | Resets that station's step register | C6, C12, C13, C22, C23 have no INIT |
| S11 | Leave service | Go to screen 0 and wait 10 s: once the flap opens, all service switches reset | **This also drops `M140.3`** (H1) |

### 3.4 Displays
| # | Item | How to test | Known issue |
|---|---|---|---|
| D1 | Packet counts C3–C23 | Compare the HMI with the real packets on each conveyor over one order | With `M333.3` = 1, FC1208 is the new counter (see `CODE_REVIEW.md` §12) |
| D2 | Motor / VFD fault colours | Trip a VFD in service and check its colour | C2 fault colour fixed (`M22.7`) |
| D3 | Doors / E-stops | Open each door and press each E-stop | Clears up to 1.8 s late after reset |
| D4 | Light barriers / proxies | Block each sensor | Up to 1.8 s late |
| D5 | Fault lamps X120/X121/X130/X134 and the new HMI lamps `H57.x` | Trip a VFD, press an E-stop, open a door | FC212 lamp fix (§8). `H57.3` polarity (H4) |

---

## 4. New-HMI bugs to decide/fix before running solo

| # | Issue | Proposed fix | Risk of fix |
|---|---|---|---|
| **H1** | `M140.3` drops by itself (service reset clears `SERVICE_SW_3_STATUS`) | **While both panels are used:** keep it, but show `M140.3` on both panels ("NEW HMI IN CONTROL"). **For solo:** `M140.3 = ON_SW` only, and don't reset `SERVICE_SW_3_STATUS` in HMI CONTROL | Low. One network |
| **H2** | New HMI OFF button (`E34.2` → `M146.2`) not wired | Put `ON "M 146.2"` back in the FC211 control-voltage reset | Low. Test at shift change |
| **H3** | Run-screen switches only update every 1.6 s | Move the 4 switch networks (hand feed, flipper, roller, turntable status) above the `JNB MAIN` | Low |
| **H4** | E-stop lamp `H57.3` = `E28.7` directly | Check whether `E28.7` is NO or NC. If NC, use `AN "E 28.7"` | Low |
| **H8** | Flipper position time `CONV_7_POS_mS` has no effect | Step 8N6: use `Timer 60` when `M140.3` = 1, keep `Timer 42` for LAUER (as C9 does) | **Medium:** changes the flip position. Test with the HMI value set to the equivalent of 1.5 s |
| H9 | `SERVICE_SW_2_TIME_ADJ` is reset every scan (C7) | Remove the `R` in C7 network 1, or remove the switch from the HMI | Low |
| H10 | Units of the position values (×50 for C7, ×10 for C8/C9) | Make them the same, or label the HMI fields "× 10 ms" | HMI change only |

**Order:** H4 and H2 (safety/operator), then H1 indicator, then H3, H8, H9, H10. After H1 "solo", the LAUER panel can be removed.

---

## 5. Readiness to run the new HMI alone
- [ ] All lines in §3 ✅ on at least 3 shifts
- [ ] H1–H4 fixed and tested
- [ ] H8 decided (fixed or feature removed from the HMI)
- [ ] Packet counts (D1) correct for a full day with `M333.3` = 1
- [ ] `M140.3` stays 1 through production for a full shift (after the H1 fix)
- [ ] Operators trained: service pages, INIT, fault reset (SIGNAL `E34.1`, `S0.7`, `S2.7`)
- [ ] Only then: disable the LAUER inputs (`M152.x`, `M150.x`, `M190.x`), or unplug the panel
