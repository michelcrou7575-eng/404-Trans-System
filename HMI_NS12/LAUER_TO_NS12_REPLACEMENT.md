# LAUER PCS 900 → OMRON NS12: full replacement inventory

**Goal:** remove the LAUER panel (DB50 `DB LAUER`, FC1 + FC100–FC103 + FC190–FC201). The NS12 (DB12 `HMI_DB`) takes over everything.
**Source:** PLC export 2026-11-17 + FC9xx (running), symbol table, photo of the panel (2026-11-20).
**Related:** `NEW_HMI_TEST_PLAN.md` (H1–H10 new-HMI bugs, test checklist).

---

## 1. Blockers: things that stop working the moment LAUER is unplugged

| # | LAUER item | PLC bit | What depends on it | Without LAUER | NS12 today |
|---|---|---|---|---|---|
| **B1** | **CLR key = fault reset** | `M171.5` | Fault latches that **only CLR can reset**: C0 `M30.1`, Pusher 0 `M30.2`, C2 angle `M22.7`, C4 collator `M30.0` (FC1300), C8 turntable `M48.6`, pivot conflict `M98.2`, elevator (FC916), flipper (FC942), loader lift (FC974), clearing new-order hold `M7.4` | **These faults can no longer be reset → machine stays stopped** | SIGNAL `E34.1` → `M9.1` resets only `M0.7` (and the FC8 counters) |
| **B2** | **F19 = "Link 508 feed by 2145" (label: "F19 doivent toujours être en fonction")** | `M153.7` | C0: eject step, F5/F18 reset, feed path (FC912) | Keeps its last state (MW152 is saved/restored through MW120). Lost after a CPU memory reset → **feeding to 508 stops** | Not on NS12 |
| **B3** | ENT + CLR together | `M171.4` + `M171.5` | Clearing abort (FC911, 2×), turntable service (FC948) | Not possible | Clearing abort exists (`CLEARING_SSW_MAIN` off → `M5.4`). Turntable: NS12 service page |
| **B4** | E-stop / door latches `M1.0–M1.3`, `M1.5–M1.7` | `M171.5` OR `S2.0` / `S2.7` / `M0.2` | FC212 | Still reset by the desk buttons | OK, no action |

## 2. Function keys (F1–F20, +, −)

Key bits are **toggles** (press = on, press again = off), kept in `MW150` / `MW152`. LED = toggle state.

| Key | Strip label | PLC bit | Used in | NS12 equivalent | Status |
|---|---|---|---|---|---|
| F1 | affichage de pas (step display) | `M150.7` | LAUER display only (FC200/201) | — | Drop (or a step page later) |
| F2 | — | `M150.6` | not used | — | Drop |
| F3 | service | `M150.5` | LAUER service (FC195 → `M190.x`) + C8 manual-mode reset | NS12 service pages 1/2/3 | ✅ covered |
| F4 | évacuer automatisation (clearing) | `M150.4` | Clearing (FC911) | `CLEARING_SSW_MAIN` (broom) → `M5.2` | ✅ covered |
| F5 | — (unlabeled) | `M150.3` | C0 "packet goes through" manual run | `ROLLER_SSW_MAIN` → `M133.4` (same OR) | ✅ covered |
| F6 | — | `M150.2` | LAUER message only (DBX95.4) | — | Drop |
| F7, F8 | — | `M150.1`, `M150.0` | not used | — | Drop |
| F9 | temps (times) | `M151.7` | LAUER time entry → DBW240/242/252 → `MW130/122/124`. **Only `MW124` (C9 position, Timer 50) is used, and only when `M140.3` = 0** | `CONV_9_POS_mS`, `CONV_8_POS_REV_mS`, `CONV_7_POS_mS` (SERVICE OFF page) | ✅ once `M140.3` is permanent (H1) |
| F10 | — | `M151.6` | LAUER preset logic only | — | Drop |
| F11 | bande de pressage passage/stockage | `M152.7` | **not used in the PLC** | — | Drop (check with operators) |
| F12 | — | `M152.6` | not used | — | Drop |
| F13 | station de retournement 0-passage 1-retournement | `M152.5` | Flipper (FC942) | `FLIPPER_SSW_MAIN` → `M111.1` | ✅ covered |
| F14 | station de retournement retourner 0-arrêt en marche | `M152.4` | **not used in the PLC** | — | Drop |
| F15 | — | `M152.3` | not used | — | Drop |
| F16 | station de tournement 0-passage 1-tourner | `M152.2` | Turntable direction (FC948) | `TURNTABLE_SSW_MAIN` | ✅ covered |
| F17 | "Paquet vers 504" (handwritten) | `M152.1` | **not used in the PLC** | — | Drop (check: 504 handled elsewhere?) |
| F18 | (Link feed by hand) | `M152.0` | C0 hand feed (FC912) | `MAN_FEED_SSW_MAIN` → `M110.0` | ✅ covered |
| F19 | (must always be ON) | `M153.7` | C0 feed to 508 | — | ❌ **B2** |
| F20 | contrôle des lampes (lamp test) | `M153.6` | 5 s lamp test of the LAUER LEDs only | — | Drop (or NS12 lamp-test button for the desk lamps) |
| + / − | (service jog) | `M161.0` / `M161.1` | LAUER service: C0, elevator, C5, flipper, C8, C9, pivot, loader | NS12 service pages (own buttons) | ✅ covered |
| ENT / CLR | | `M171.4` / `M171.5` | see B1, B3 | | ❌ **B1** |

## 3. Displays sent to LAUER

| LAUER | NS12 |
|---|---|
| Clock (line 1) | NS12 system clock |
| Order / packet line ("H->bottomeuse AD2360/22") | written by the LAUER itself — check what the operators need from it |
| Turntable / pivot / C9 / C4 position words DBW220/232/236/238 | NS12 run screen already shows the proxies |
| **Fault and status messages (FC199 + FC201): 69 conditions, list in §5** | **❌ NS12 Alarm table is empty** |

## 4. Proposed steps

1. **B1, CLR reset** (one network, low risk): in each block that uses `A "M 171.5"` for a reset, change to `O "M 171.5"  O "M 9.1"`, so the SIGNAL button (`E34.1`), `S0.7` and `S2.7` reset everything CLR resets. Works with LAUER still connected.
2. **B2, F19:** NS12 switch "Link 508 feed by 2145" on the run screen, **or** force it in the PLC (`SET` / `= "M 153.7"` after the LAUER call) if it really must always be on.
3. **H1** from `NEW_HMI_TEST_PLAN.md`: `M140.3` = NS12 ON only (position times then always from the NS12).
4. **NS12 alarm list** from §5 (Alarm.csv): needs the NS12 address format for the PLC (export one object with an address).
5. Run 3 shifts with LAUER still connected but not touched.
6. Unplug LAUER. Keep FC1/FC100 called for a week (harmless: keys read 0).
7. Delete the LAUER blocks and DB50 → frees memory (DB50 + 13 FCs).

## 5. LAUER message list (FC199 "Faults" + FC201 "Status") → NS12 alarms

LAUER shows **one message at a time** (first true condition wins, `BEC`). The NS12 can show all active ones.
"Only when running" = also needs `M0.3` (control voltage) and `M11.6`, not `M9.7`.
⚠️ Original bug: lines 59, 61, 62, 63 test `M4.1` (C10 VFD) but their READY input is C21/C22/C23: use the right VFD fault bit in the NS12 alarm.

| # | DB50 bit | Only when running (M0.3, no fault) | Condition (PLC) |
|---|---|---|---|
| 1 | DBX82.3 |  | A M 0.4 — FL FUSE SENS - FAULT |
| 2 | DBX85.3 |  | A M 22.7 — FL ANGLE CONVEYOR - FAULT |
| 3 | DBX85.4 |  | A M 1.0 — FL E-STOP  DESK  X120 - HMI BOX |
| 4 | DBX85.5 |  | A M 1.1 — FL E-STOP  DESK  X121 - FEEDER BOX |
| 5 | DBX85.6 |  | A M 1.2 — FL E-STOP  ELEVATOR STATION |
| 6 | DBX84.0 |  | A M 1.3 — FL E-STOP  FLIPPER STATION |
| 7 | DBX82.2 |  | A M 0.5 — FL MOTOR PROTECT - FAULT |
| 8 | DBX82.4 |  | A M 0.6 — FL MOTOR TEMP CONTROL - FAULT |
| 9 | DBX82.5 |  | A M 0.7 — FL COMPRESSED AIR AT 5 BAR - FAULT |
| 10 | DBX87.0 |  | O M 1.5 — FL DOOR OPEN FEEDER - FAULT |
| 11 | DBX87.1 |  | O M 30.1 — FL ELEVATOR ROLLERS - FAULT |
| 12 | DBX87.2 |  | O M 30.2 — FL ELEVATOR PUSHER - FAULT |
| 13 | DBX84.6 |  | A M 1.6 — FL DOOR OPEN ELEVATOR - FAULT |
| 14 | DBX84.7 |  | A M 1.7 — FL DOOR OPEN FLIPPER - FAULT |
| 15 | DBX87.3 |  | A M 30.7 — FL COLLATOR CONVEYOR 4 - TIMEOUT STOP - FAULT |
| 16 | DBX87.4 |  | A M 38.7 — FL FLIPPER DELIVERY CONVEYOR 6 - FAULT |
| 17 | DBX87.5 |  | A M 54.7 — FL PIVOT CONVEYOR 10 - FAULT |
| 18 | DBX87.6 |  | O M 66.7 — FL DELIVERY CONVEYOR 13 - FAULT<br>O M 86.7 — FL DELIVERY CONVEYOR 23 - FAULT |
| 19 | DBX86.0 |  | A M 30.0 — FL COLLATOR CONVEYOR 4 - FAULT |
| 20 | DBX87.7 |  | A M 98.1 — FL PIVOT - TIMEOUT FAULT |
| 21 | DBX86.1 |  | A M 14.7 — FL ELEVATOR - PKT NOT CENTERED FAULT |
| 22 | DBX86.2 |  | A M 42.7 — FL FLIPPER FLIP - OBSTRUCT - FAULT |
| 23 | DBX86.3 | yes | A B 5.1 — LB  ELEVATOR - PLATFORM INFEED SENS    POS.2 |
| 24 | DBX86.4 | yes | A B 5.2 — LB  ELEVATOR - PLATFORM LIMIT SENS    POS.2 |
| 25 | DBX86.5 | yes | A B 5.4 — LB  CONVEYOR 1 - EXIT SENS    POS.3 |
| 26 | DBX86.6 | yes | A B 5.5 — LB  ANGLE CONVEYOR 2 INFEED SENS     POS.4 |
| 27 | DBX86.7 | yes | A B 6.0 — LB  ANGLE CONVEYOR 2 ROLLER - CENTER ABOVE SENS    POS.4 |
| 28 | DBX89.0 | yes | A B 6.7 — LB  COLLATOR CONVEYOR 4 - INFEED SENS    POS.6<br>O M 33.7 — FL CONVEYOR 4 - INFEED OBSTRUCTION |
| 29 | DBX89.1 | yes | A B 7.0 — LB  COLLATOR CONVEYOR 4 - EXIT SENS    POS.6 |
| 30 | DBX89.2 | yes | A B 7.1 — LB  LINK CONVEYOR 5 - EXIT SENS    POS.7 |
| 31 | DBX89.3 | yes | A B 7.2 — LB  DELIVERY CONVEYOR 6 - REACHING SENS    POS.8 |
| 32 | DBX89.4 | yes | A B 7.3 — LB  DELIVERY CONVEYOR 6 - EXIT SENS    POS.8 |
| 33 | DBX89.5 | yes | A B 7.4 — LB  FLIPPER - INFEED SENS    POS.8 |
| 34 | DBX89.6 |  | A M 98.2 — FL PIVOT / CONVEYOR - COMFLICT FAULT |
| 35 | DBX89.7 | yes | A B 8.2 — LB  FLIPPER STATION EXIT SENS     POS.9 |
| 36 | DBX88.0 | yes | A B 9.6 — LB  PUSHER ROLLER CONVEYOR 9 INFEED SENS      POS.11 |
| 37 | DBX88.1 | yes | A B 9.7 — LB  PUSHER ROLLER CONVEYOR 9 PACKET EDGE SENS      POS.11 |
| 38 | DBX88.2 | yes | A B 10.4 — LB  PIVOT CONVEYOR 10 - INFEED SENS    POS.12 |
| 39 | DBX88.3 | yes | A B 10.5 — LB  PIVOT CONVEYOR 10 - FULL SENS    POS.12 |
| 40 | DBX88.4 | yes | A B 10.7 — LB  CONVEYOR 11 - EXIT SENS    POS.13 L |
| 41 | DBX88.5 | yes | A B 11.0 — LB  CONVEYOR 12 - EXIT SENS    POS.14 L |
| 42 | DBX88.6 | yes | A B 11.1 — LB  CONVEYOR 13 - SLOW SENS    POS.15 L |
| 43 | DBX91.2 | yes | AN B 5.4 — LB  CONVEYOR 1 - EXIT SENS    POS.3 |
| 44 | DBX91.3 | yes | AN B 9.7 — LB  PUSHER ROLLER CONVEYOR 9 PACKET EDGE SENS      POS.11 |
| 45 | DBX91.6 |  | A M 11.7 — FL CONVEYOR 1 - 2, 7 - 9 - PACKETS PRESENT - ALL |
| 46 | DBX91.4 |  | A M 4.5 — FL VFD  U53.2 FAULT - CONVEYOR 21 |
| 47 | DBX91.4 |  | A M 3.0 — FL VFD  U44.3 FAULT - CONVEYOR 4 |
| 48 | DBX91.4 |  | A M 4.0 — FL VFD  U47.6 FAULT - PUSHER 2 |
| 49 | DBX91.4 |  | A M 3.3 — FL VFD  U45.6 FAULT - FLIPPER CONVEYOR 7 |
| 50 | DBX91.4 |  | A M 3.5 — FL VFD  U46.4 FAULT - TURNTABLE CONVEYOR 8 |
| 51 | DBX91.4 |  | A M 4.1 — FL VFD  U48.0 FAULT - CONVEYOR 10<br>AN E 13.4 — SENS CONVEYOR 10 VFD U48.0 - READY |
| 52 | DBX91.4 |  | A M 4.4 — FL VFD  U49.0 FAULT - CONVEYOR 13<br>AN E 13.7 — SENS CONVEYOR 13 VFD U49.0 - READY |
| 53 | DBX91.4 |  | A M 3.1 — FL VFD  U45.0 FAULT - CONVEYOR 5 |
| 54 | DBX91.4 |  | A M 3.2 — FL VFD  U45.3 FAULT - CONVEYOR 6 |
| 55 | DBX91.4 |  | A M 3.4 — FL VFD  U46.0 FAULT - FLIPPER |
| 56 | DBX91.4 |  | A M 3.6 — FL VFD  U47.0 FAULT - TURNTABLE |
| 57 | DBX91.4 |  | A M 3.7 — FL VFD  U47.5 FAULT - PUSHER 2 CONVEYOR 9 |
| 58 | DBX91.4 |  | A M 4.6 — FL VFD  U53.4 FAULT - CONVEYOR 22 |
| 59 | DBX91.4 |  | A M 4.1 — FL VFD  U48.0 FAULT - CONVEYOR 10 |
| 60 | DBX91.4 |  | A M 4.3 — FL VFD  U48.6 FAULT - CONVEYOR 12<br>AN E 13.6 — SENS CONVEYOR 12 VFD U48.6 - READY |
| 61 | DBX91.4 |  | A M 4.1 — FL VFD  U48.0 FAULT - CONVEYOR 10<br>AN E 28.0 — SENS CONVEYOR 21 - VFD  U53.2 - READY |
| 62 | DBX91.4 |  | A M 4.1 — FL VFD  U48.0 FAULT - CONVEYOR 10<br>AN E 28.1 — SENS CONVEYOR 22 - VFD  U53.6 - READY |
| 63 | DBX91.4 |  | A M 4.1 — FL VFD  U48.0 FAULT - CONVEYOR 10<br>AN E 28.2 — SENS CONVEYOR 23 - VFD  U54.0 - READY |
| 64 | DBX95.5 |  | A Timer 0 — TI LAMPS TEST - PULSE |
| 65 | DBX95.4 |  | O M 150.2 — FUNCTION KEYS <F6 > ON LAUER |
| 66 | DBX91.7 |  | A M 10.0 — FL CONVEYORS CLEARING CMD |
| 67 | DBX83.2 |  | O M 150.4 — FUNCTION KEYS <F4 > ON LAUER<br>O M 150.5 — FUNCTION KEYS <F3 > ON LAUER<br>O M 150.7 — FUNCTION KEYS <F1 > ON LAUER<br>ON S 2.1 — PB  STOP           X120 - HMI BOX<br>O S 2.2 — PB  START           X120 - HMI BOX<br>AN M 0.1 — FL START SIGNAL<br>AN M 0.2 — FL START READY 10S<br>AN M 0.3 — FL CONTROL VOLTAGE<br>AN M 1.5 — FL DOOR OPEN FEEDER - FAULT<br>AN M 1.7 — FL DOOR OPEN FLIPPER - FAULT |
| 68 | DBX83.3 |  | A M 0.2 — FL START READY 10S<br>AN M 0.3 — FL CONTROL VOLTAGE |
| 69 | DBX83.4 |  | A M 0.3 — FL CONTROL VOLTAGE<br>AN M 9.7 — FL CLEARING DONE - READY |
