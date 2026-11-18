# 404 Trans-System: STL/AWL code review

**Scope:** all 28 STEP 7 STL (AWL) source blocks in this repository, about 11,900 lines. Every block was read in full, then cross-checked against the others: shared memory bits, timers, edge memories, "DB UTILITY" disable/freeze flags, and HMI DBs.
**Date:** 2026-09-23
**Method:** static reading only. Nothing was compiled or simulated, because OB1, the symbol table, the DBs/UDTs and several called FCs are not in the repo (see §5).

Severity scale:

| Level | Meaning |
|---|---|
| 🔴 **HIGH** | Can move a machine element wrongly or unsafely, or randomly corrupt a sequence during normal production |
| 🟠 **MEDIUM** | A real logic bug that causes wrong behaviour in some situations (service mode, clearing, counters, sync) |
| 🟡 **LOW** | Display/HMI errors, dead code, misleading comments, maintainability |
| ❓ **VERIFY** | Depends on hardware or code that isn't in the repo. Check it on site. |

Line numbers refer to the files as committed (CRLF).

---

## 1. Summary

Overall the code is **structured and consistent**. Each station is one FC with a service-mode header, a step chain in a memory byte/word, timeouts on almost every step, and "freezable" soft timers in `DB UTILITY`. Most reversing outputs have proper software cross-interlocks (`K62.0/1`, `K62.2/3`, `K42.6/7`, `K47.6/7`, `A46.4/5`, `A47.0/1`, `A50.0/1`, `K50.5/6`).

The main problems:

1. **Two reversing actuator pairs have no cross-interlock:** the Flipper (`K46.0/K46.1`) and the Pivot (`K53.0/K53.1`).
2. **Uninitialised temp variables are read** in 5 places. Two of them (Conv 3, Conv 21) run **during normal production** and can randomly reset a step chain.
3. **Elevator VFD fault handling** does not drop the brake-release or drive-release outputs.
4. **Packet counting is split** between the old and new counter blocks and two HMI DBs. The auto re-sync (Conv 5) and the light bar read the *old* DB, while most *new* counter calls are commented out.
5. **Several "disable" flags are written but never read**, so service mode does not isolate the neighbouring conveyor as intended.

| # | Sev | Block | Finding |
|---|---|---|---|
| 1 | ✅ | CONVEYOR 7 - FLIPPER | No cross-interlock between CW `K46.1` and CCW `K46.0`. **Fixed (§7)** |
| 2 | ✅ | CONVEYOR 10 - PIVOT | No cross-interlock between DOWN `K53.0` and UP `K53.1`. **Fixed (§7)** |
| 3 | ✅ | CONVEYOR 3 - SLAT | `#INITIALISATION` read uninitialised in normal operation, so MB27 can reset at random. **Fixed (§7)** |
| 4 | ✅ | CONVEYOR 21 - LINK 1 HI | Same bug: `#INITIALISATION` not reset at label `CO21`, so MW79/MB81 can reset at random. **Fixed (§7)** |
| 5 | 🟠❓ | ELEVATOR + PUSHER 1 | VFD/brake fault `M92.5` does not drop `A63.0`. **Downgraded (§10):** the brake is dropped by `E15.3` (motor energised), and `M92.5` is reset by FC212 |
| 6 | ✅ | CONVEYOR 6 - FLIP DELIVERY | `#INITIALISATION` never assigned, and read as garbage while in service mode. **Fixed (§7)** |
| 7 | ✅ | LOADER LIFT | `#FEEDER_SW` never assigned, and read as garbage while in service mode. **Fixed (§7)** |
| 8 | 🟠 | CONVEYOR 10 - PIVOT | `#SURFACE_LENGTH_LEFT_10` read when it may not have been written this scan |
| 9 | 🟠 | CONVEYORS CLEARING | Uses `M54.6` (C10 full flag) where the comment and logic need `M54.2` (C11…C23 empty) |
| 10 | 🟠 | CONVEYOR 4 - COLLATOR | REAL math applied to INT `MW202`, so the HMI length hysteresis is always 0 |
| 11 | 🟠 | CONVEYOR 5 / LIGHT BAR / COUNTERS | Old `"HMI_DB"` and new `"HMI DB NEW"` counters are mixed, and most new counter calls are commented out |
| 12 | 🟠 | CONV 2 / 3 / 11 / 21 | `Conveyor_2_Disable`, `Conveyor_10_Disable`, `Pivot_Disable` are written but never read |
| 13 | 🟠 | LOADER LIFT + FINGERS | `Conveyor_13/23_Disable` written by both blocks (`S/R` in one, `=` in the other) |
| 14 | 🟠❓ | HMI CONTROL | The service auto-reset clears `SERVICE_SW_3_STATUS`, which silently switches `M140.3` back to "LAUER panel" mode |
| 15 | 🟠❓ | TURNTABLE / FLIPPER / LOADER | Sequences freeze (instead of resetting) when the guard door opens, and resume by themselves when it closes |
| 16 | 🟠 | DE-BOUNCER LINK CONVEYOR (FC6) | `IO_Count_Done` never reset (only one count ever); `Bit1_Front_End` never reset; 5 s reset is overwritten |
| 17 | 🟠 | DE-BOUNCER-COUNTER-WIP | No error reset, Delivery type empty, ms accumulator overflow, stale exit window |
| 18 | ~~🟡~~ | LIGHT BAR | ~~Lamps 4/5/6 operator precedence~~. **Withdrawn:** STL evaluates `O <operand>` left to right, so these lamps are correct |
| 19 | 🟡 | many | Calibration constants and timer values that disagree with their comments |
| 20 | 🟡 | many | Dead code, debug/test leftovers, misc. (see §4) |

---

## 2. HIGH severity

### 2.1 Flipper motor: no CW/CCW cross-interlock 🔴
`CONVEYOR 7 - FLIPPER` lines 448–460 (`K46.1` CW) and 491–503 (`K46.0` CCW).

```
K46.1 := (M42.5 OR (M42.4 AND M161.1) OR #FLIP_CW)  AND P8.0 AND NOT M42.7 AND NOT A45.6 AND M42.2
K46.0 := (M42.6 OR (M42.4 AND M161.0) OR #FLIP_CCW) AND P8.1 AND NOT A45.6 AND NOT M42.7 AND M42.2
```

Neither coil checks the other. Mid-travel, `P8.0` and `P8.1` are both 1, so both contactors energise if both trigger branches are true in the same scan. For example, auto flip `M42.5` is active while the LAUER service jog (`M42.4` + `M161.0`) is pressed, or `M161.0` and `M161.1` are both 1. Note that CONVEYOR 0 treats `M161.0 AND M161.1` as a valid state. Every other reversing pair in the project has this interlock.

**Fix:** add `AN "K 46.0"` to the `K46.1` network and `AN "K 46.1"` to the `K46.0` network. Also confirm there is a hardware (auxiliary contact) interlock.

### 2.2 Pivot up/down: no cross-interlock 🔴
`CONVEYOR 10 - PIVOT` lines 588–600 (`K53.0` down) and 605–617 (`K53.1` up).

`#PIVOT_DN` and `#PIVOT_UP` come from two **independent** HMI switches (lines 49–55). Unlike the turntable CW/CCW service switches, they are not made mutually exclusive. Between positions (`P15.0` = `P15.1` = 0), both outputs energise if both switches are on, or if `M161.0` and `M161.1` are both 1.

**Fix:** add `AN "K 53.1"` to `K53.0` and `AN "K 53.0"` to `K53.1`. Also make `PIVOT_UP`/`PIVOT_DN` exclusive in the service header, the same way `TURN_CW`/`TURN_CCW` are.

### 2.3 Slat conveyor 3: uninitialised `#INITIALISATION` 🔴
`CONVEYOR 3 - SLAT` label `CON3` (line 36) resets only `#SERVICE_RUN`. In normal operation (service off) the JNB jumps straight to `CON3`, so `#INITIALISATION` is **never written**. It is then read at line 306 (`O #INITIALISATION`) and, if true, clears `MB27` (the whole slat step chain) and `M26.7`.
The value is whatever the previous block left in that L-stack byte, so the result depends on OB1 call order and can change after any unrelated edit.

Every other conveyor (1, 2, 4, 5, 8, 9, 10, 11) has `R #INITIALISATION` after its service label.
**Fix:** add `R #INITIALISATION;` after `CON3:`.

### 2.4 Link conveyor 21: same bug 🔴
`CONVEYOR 21 - LINK 1 HI` label `CO21` (line 41) is missing the `R #INITIALISATION` that its twin `CONVEYOR 11` has. The garbage value is read at line 72 and clears `MW79` + `MB81` (the C21 step chain).
**Fix:** add `R #INITIALISATION;` after `CO21:`.

### 2.5 Elevator: fault handling leaves brake and drive released 🔴❓
`ELEVATOR + PUSHER 1` lines 453–531.

* When `E14.4` (drive OK) drops or `#BRAKE_CONTACTOR_KO` is true, `M92.5` is set and the code jumps to `OFF`. `OFF` only resets `A63.0` **if the brake feedback says the brake is applied** (`AN #BRAKE_RELEASE_OK`). The speed outputs `A63.1..3` keep their last state as long as an up/down command is still active.
* The brake-release output `A56.2` (line 355) is `UP_OUT OR DN_OUT`, and neither of those terms looks at `M92.5`. So after a fault the brake stays released while a move is commanded. The only other brake drop is `AN "E 15.3"` (line 359), whose comment ("Motor Stopped") doesn't match how it is used. Confirm what that input really is.
* ~~`M92.5` is never reset in any block in this repo.~~ **Update:** FC212 resets it with `M9.1` (fault-reset buttons), see §8.
* The brake is released in the **same scan** as the drive enable (`A63.0`), with no wait for the drive to be magnetised or to have torque. On a vertical axis the usual order is: drive enable → torque/ready feedback → release brake → confirm → move.

**Recommended:** gate `M92.0`/`M92.1` (and so `A56.2`) with `AN "M 92.5"`. On a fault, reset `A63.0..A63.3` unconditionally once the brake is confirmed applied. Add an explicit fault reset. Have the hoist sequence checked against the drive manual and the machine's risk assessment.

---

## 3. MEDIUM severity

### 3.1 Other uninitialised temp reads
| Block | Line | Detail |
|---|---|---|
| `CONVEYOR 6 - FLIP DELIVERY` | 33 / 91 | `#INITIALISATION` is never assigned. It is reset at `CON6` only when the jump is taken (RLO = 1). While in service mode it holds garbage, which can clear `MW39`, `MB41` and the C6 count. |
| `LOADER LIFT` | 59 | `ON #FEEDER_SW`: `#FEEDER_SW` is declared but **never assigned**. During loader service this randomly resets the HMI service switches and `Conveyor_13/23_Disable`. It was probably meant to be `#FEEDER_SERVICE_SW` (compare LOADER FINGERS). |
| `CONVEYOR 10 - PIVOT` | 172–216 | `#SURFACE_LENGTH_LEFT_10` is written only inside `A M166.5 / JNB M665`, but read unconditionally in "Space Between Packet" (line 192) and "Collating Surface Manager" (line 216). Read `"COLLATORS DB".Surface_Length_Left_10` instead. |

### 3.2 Clearing: wrong bit for "C11…C23 empty" 🟠
`CONVEYORS CLEARING` line 473: `A "M 54.6" // Empty C11...C23` then `R "M 8.5"`.
`M54.2` is the "C11…C23 empty" latch (set at line 47). `M54.6` is **"C10 collator full"** from CONVEYOR 10. As written, `M8.5` (New-Order / Clearing-Done) is reset whenever C10 flags full, which can break the New-Order sequence (Case A/B).

### 3.3 Conveyor 4: REAL math on an INT 🟠
`CONVEYOR 4 - COLLATOR` "Packet Length to HMI + Hysteresis" (line 350 on): `L "MW 202"; L 3.0; *R`.
`MW202` is an INT (from `RND` in the old counter). Multiplying its raw bits as a REAL gives ≈ 0, so `W_TUBE_PERCENT` = 0 and the ±band = 0. The hysteresis does nothing. The band is also re-centred on every new value, so slow drift never reaches the HMI. The comment says 5 %, the code says 3 %.
**Fix:** `L "MW 202"; ITD; DTR; L 3.0; *R; L 100.0; /R; RND`. Keep the band centred on the last value *sent to the HMI*.

### 3.4 Packet counters split across two blocks and two DBs 🟠
* `HMI PACKET COUNTER OLD` writes `"HMI_DB".CONV_x_COUNT`. `HMI PACKET COUNTER NEW` writes `"HMI DB NEW".CONV_x_COUNT`.
* **Readers of the old DB:** CONVEYOR 5 auto re-sync (lines 208, 213, 218), which decides when C5 runs its 13 s synchronisation, and every LIGHT BAR lamp.
* **Resets use the new DB:** CONVEYOR 5 and 6 reset `"HMI DB NEW"`, CONVEYOR 10 resets `"HMI_DB"`.
* In the NEW block, the counter CALLs for **C6, C10, C11, C12, C13, C21, C22, C23 are commented out**. Those counts only ever get reset, never incremented.
* If both FCs are called from OB1, they both write `M143.0..7` and both run `Timer 80/81`.

If OB1 calls only NEW, then re-sync and the lamps run on stale counts. If it calls only OLD, then C5/C6 resets go to the wrong DB. Decide which one is live and point every reader and writer at it.

### 3.5 Disable flags that nothing reads 🟠
| Flag | Set by | Read by |
|---|---|---|
| `Conveyor_2_Disable` | CONVEYOR 3 service (line 26) | **nobody**. CONVEYOR 2 reads `Conveyor_1_Disable` at line 339 |
| `Conveyor_10_Disable`, `Pivot_Disable` | CONVEYOR 11 / 21 service (lines 30–31) | **nobody**. CONVEYOR 10 has no disable input |

Result: jogging C3 doesn't stop C2 from feeding it, and drive-testing C11/C21 doesn't stop the pivot sequence from transferring onto it.

### 3.6 `Conveyor_13/23_Disable`: two writers 🟠
`LOADER LIFT` lines 42–43 use `S`/`R`. `LOADER FINGERS` lines 46–47 use `=` (i.e. `FINGERS_SERVICE_SW`). Whichever block runs later in OB1 wins. Use one owner.

### 3.7 HMI mode silently reverts to the LAUER panel 🟠❓
`HMI CONTROL` line 50–52: `M140.3 = ON_SW AND SERVICE_SW_3_STATUS` ("New HMI ON Temporary").
The "HMI Service Switch Reset" network resets `SERVICE_SW_3_STATUS` after 10 s on screen 0 with the flap open. That drops `M140.3`, so roller, flipper, turntable direction, clearing and hand feed all switch back to their **LAUER** inputs (`M152.x`) without the operator knowing. If the LAUER panel is gone, give `M140.3` its own permanent bit.

### 3.8 Automatic restart after guard closing 🟠❓
> **Update (§10):** the symbol table shows that `E9.0`, `E12.5` and `E4.6` are *safety-relay* "door closed" contacts. If those relays are manual-reset types, the door already needs a deliberate reset before motion can restart, and this finding is covered in hardware. Check the relay type.

* Turntable: `M46.3` includes `E9.0` (line 163).
* Flipper: `M42.2 = E9.0 AND M0.3` (line 150).
* Loader lift: `M74.0` includes `E12.5` (line 91).

Opening the door freezes the step chain but does **not** reset it. When the door closes, the chain continues from where it stopped (turn, flip, or lift-down `A50.1`, which unlike lift-up is not gated by the `M74.5` door latch). Unless the safety relay behind `M0.3` needs a manual reset, motion restarts with no operator action. Confirm against the safety concept (ISO 12100 / EN 60204-1 §9.2.5.4).

Also related: the loader light barrier (`E1.4`, "Light Barrier Buffer") runs in standard PLC logic with a bypass bit `M90.0`. Nothing in this repo sets `M90.0`, but it must never be settable from the HMI, and the light curtain itself must be wired through a safety relay.

### 3.9 `DE-BOUNCER LINK CONVEYOR` (v0.4, old FC6) 🟠
No block in this repo calls it, but it is broken if it ever comes back:
* `IO_Count_Done` is set (lines 171, 189) and **never reset**, so it counts once, ever.
* "Reset All" resets `IO_Bit0_Front_End` twice (lines 261–262). The second one should be `IO_Bit1_Front_End`.
* The 5 s bypass `= #RESET_ALL` (line 218) is overwritten by the Monitor network (`= #RESET_ALL`, line 238), so it never takes effect.
* The INT ms accumulators overflow after 32.7 s of latch.

### 3.10 `DE-BOUNCER / COUNTER` (v0.6, WIP) 🟠
* `IO_DB.Error` (line 411) latches and can only be cleared by first-scan init. It needs a reset input.
* Delivery type (line 342) is an empty stub. C6/C13/C23 are declared as Delivery, which is why their calls are commented out.
* If a short pulse on `Bit_0` latches `Bit0_ON_Latch`, `Bit0_Entry_mS` keeps counting. The next real packet then counts on its first scan, raises a false error once the count passes 5000 ms, and the counter wraps at 32767.
* `Exit_Window_mS` is only computed when `Bit_0` starts. If `Bit_1` comes first (after power-up), the stale or zero window counts down immediately.

---

## 4. LOW severity: display, dead code, comments

~~**Light bar precedence**~~ (withdrawn). In STL, `O <operand>` resets the OR status bit, so `a O b A c` evaluates left to right as `(a OR b) AND c`. AND-before-OR only applies to `O` without an operand. Lamps >4<, >5< and >6< therefore work as intended.

**Constants that don't match their comments:**
| Where | Code | Comment |
|---|---|---|
| CONVEYOR 3 line 61 | `1.3` mm/pulse | 900 mm / 600 PPR = **1.5** |
| CONVEYOR 10 line 150 | `0.31` mm/pulse | 283 mm / 600 PPR = **0.47** |
| CONVEYOR 0 line 141 | `S5T#200MS` | "Debouncer 300mS" |
| CONVEYOR 10 line 351 | `S5T#5S` | title "TimeOut 10s" |
| CONVEYOR 5 line 190 | `>= 10` runs | "every 5 runs" |
| CONVEYOR 3 line 274 | Timer **28** | title "Soft Timer 27 Done 11s" |
| CONVEYOR 4 | 3 % | "Tube 5 %" |
| CONVEYOR 7 line 247 / CONVEYOR 8 / CONVEYOR 9 | HMI value × 50 / × 10 | "Integer contains MILLISECONDS" |

Check the encoder factors against a measured packet before changing them. They may have been tuned on site and only the comment is wrong.

**Dead code and leftovers:**
* CONVEYOR 7: `Timer 60` (line 283, HMI-adjustable flip position) is started but never read. Step 8N6 uses a fixed 1.5 s `Timer 42`. `SERVICE_SW_2_TIME_ADJ` is reset every scan (line 30), so `#TIME_SW` is always 0.
* HMI PACKET COUNTER NEW: test forces `"TESTM 400.0"` (line 60) and `M400.1` (line 98). Line 208 has a `<>R` compare on a DINT whose result is never used. `#I_O_DB` is unused. Also check that the CPU has ≥ 401 M-bytes (`M400`, `MW354`).
* HMI PACKET COUNTER OLD line 180: debug `L MW280; T MW282`.
* Written but never read here: `M24.4`, `M30.3`, `M9.7`, `M11.4` (set, never reset).
* `CONVEYORS CLEARING` line 257–260: `A M0.3 A T9 ON M11.6 S M9.7` evaluates as `(M0.3·T9) + ¬M11.6`, which is probably not what was meant (harmless, because `M9.7` is unused).
* LOADER LIFT line 294, "Fill MB76": `2#11111100000000` actually sets **MB75** bits 0–5 and clears MB76. Check this is the intended re-entry step.

**Robustness and maintainability:**
* `M9.0` is used as a shared scratch bit across 6 FCs. It works only because each write comes before its read. Use a `VAR_TEMP` instead.
* 16-bit `-I` / `>=I` on the 32-bit FM350 counters (CONVEYOR 3 line 57, CONVEYOR 4, CONVEYOR 10). This is fine while differences stay under 32767 pulses and the count only goes up. Use `-D`.
* HMI CONTROL line 68: `JNB MAIN` jumps across networks. It is legal in STL but fragile, and it means the 20-min service/hand-feed timers are only evaluated on update pulses.
* The service-exit pattern (`JNB label` … `label: R temps; FP; = M x.y`) depends on RLO = 1 after a *taken* JNB. It works, but add a comment. Several of the bugs above come from copies of this header that lost a line.
* HMI COMMS line 1073: the Conveyor 2 fault colour uses `M30.7` (C4 infeed fault) instead of `M22.7`. The change detection uses sums of input words, so two different bit patterns can give the same sum (the periodic refresh covers this).
* CONVEYOR 13 resets "Ready" with `M9.1`, while CONVEYOR 23 uses `S2.7`. Is the asymmetry intended?
* CONVEYOR 12/13/22/23 are enabled by `CONVEYOR_11/21_SERVICE_SW` (a shared page). This is probably intended, but it isn't documented.

---

## 5. Repository and completeness

* Files have **no `.AWL` extension**, and the file names don't always match the block names (`LOADER FINGERS` → `FUNCTION "FEEDER FINGERS"`, `DE-BOUNCER LINK CONVEYOR FC6` → `"DE-BOUNCER LINK CONVEYOR"`).
* **Missing for a compile or full review:** OB1 (call order matters for several findings above), the symbol table (`.SDF`/`.SEQ`), all DB and UDT sources (`HMI_DB`, `HMI DB NEW`, `DB UTILITY`, `COLLATORS DB`, `HOUSE_KEEPING DB`, `FM350 DB`, `DEBOUNCER COUNTER DB`, `"Debouncer Counter Struct"`, `DB LAUER`, `DB12`), and the called FCs `SCALER`, `LAUER TIME`, `DE-BOUNCER OLD`. The alarms/LAUER FC ("FC 212") that drives `M0.3`, `M9.1`, `M161.x`, `M171.x`, `M190.x` and the freeze flags is also missing.
* **Suggested next step:** export the whole S7 program as source (all blocks + symbols) into this repo. Then the call order, data types and the "never written" bits above can be confirmed.

---

## 6. Suggested fix order

1. Add the interlocks to Flipper `K46.0/1` and Pivot `K53.0/1` (§2.1, §2.2).
2. Add `R #INITIALISATION` in CONVEYOR 3 and 21, assign or reset it in CONVEYOR 6, and fix `#FEEDER_SW` (§2.3, §2.4, §3.1).
3. Review elevator fault/brake handling on site (§2.5).
4. Fix the Clearing `M54.6` → `M54.2` bit (§3.2).
5. Choose one counter FC and one HMI DB, then re-point CONVEYOR 5 re-sync and LIGHT BAR (§3.4).
6. Connect the disable flags (§3.5, §3.6), then fix the display and comment items.

Every change must be commissioned on the machine. Test service mode, clearing and the door-open/close cycles for each station.

---

## 7. Update: fixes applied, and review of the "VFD OK -Check" blocks, OB1 and DBs

### 7.1 Fixes applied on this branch
Each fix was applied to **both** the original file and its `_ VFD OK -Check` copy, so the fix is in whichever version gets imported. Every change is marked with a `//` comment in the code.

| Block | Change |
|---|---|
| CONVEYOR 7 - FLIPPER | `K46.1` CW: added `AN "K 46.0"`. `K46.0` CCW: added `AN "K 46.1"` |
| CONVEYOR 10 - PIVOT | `K53.0` DOWN: added `AN "K 53.1"`. `K53.1` UP: added `AN "K 53.0"`. Service `#PIVOT_DN`/`#PIVOT_UP` are now mutually exclusive: if both HMI switches are on, neither output runs |
| CONVEYOR 3 - SLAT | `R #INITIALISATION` after `CON3:` |
| CONVEYOR 21 - LINK 1 HI | `R #INITIALISATION` after `CO21:` |
| CONVEYOR 6 - FLIP DELIVERY | `CLR / = #INITIALISATION` at the start of the service network. No behaviour change: this conveyor never had an INIT button |
| LOADER LIFT | `ON #FEEDER_SW` → `ON #FEEDER_SERVICE_SW`, which matches the same line in LOADER FINGERS |
| ELEVATOR + PUSHER 1 _ VFD OK -Check | `AN "M 11.1"` added to the Rise (`M92.0`) and Fall (`M92.1`) networks. See 7.2 for why |

Each interlock line is appended at the end of the chain, just before the `=`. With left-to-right STL evaluation, it therefore blocks **every** branch (auto, LAUER jog and HMI service).

### 7.2 "VFD OK -Check" blocks (`M11.1` = VFD NOT all ready)
The change blocks VFD release outputs while `M11.1` is set. It is correct and consistent on C1, C2, C3, C4, C7, C8 belt, C9, C10, C11, C12, C21 and C22. Conveyor 0 sends packets "through" while `M11.1` is set and blocks Pusher 0 FWD. That also looks correct.

Issues found:
1. 🔴 **Elevator (fixed, see 7.1).** `AN M11.1` had been added only to the two **UP** speed branches of the VFD network. Two consequences:
   * DOWN was not blocked at all.
   * When UP was blocked, `#ELEVATOR_UP_OUT` stayed true. That kept brake release `A56.2` energised while the drive was never enabled (`A63.0` not set). **The brake would open with no torque on the vertical axis.**

   `M11.1` now gates `M92.0`/`M92.1`, the signals that drive both the brake and the drive. So when the VFDs aren't ready the brake stays applied. The original `AN M11.1` lines in the speed branches were left in place (harmless).
2. 🟠 **Not gated by `M11.1`:** Conveyor 5 (`A45.0`), Conveyor 6 (`A45.3`), Conveyor 13 (`A49.0`), Conveyor 23 (`A54.0`), Feeder Fingers belt (`A51.0`) and TurnTable turn (`A47.0/A47.1/A47.2`). No "VFD OK -Check" version exists for C5, C6, C13, C23 and the loader blocks. Check whether these are on the same VFD-ready circuit.
3. 🟠 **Block name mismatch.** `CONVEYOR 6 - FLIP DELIVERY _ VFD OK -Check` renames the FUNCTION to `"CONVEYOR 6 - FLIP DELIVERY"`, but OB1 calls `"CONVEYOR 6 - FLIP DELIV."`. Also, OB1 calls `"FEEDER LIFT"` while the `LOADER LIFT` file declares `FUNCTION "LOADER LIFT"`. Make sure the symbol table matches, or the source import creates a new, uncalled block.
4. 🟡 Where `M11.1` is computed isn't in the repo (probably FC "CONTROL").
5. 🟡 Step timeouts that don't depend on the running output keep counting while `M11.1` holds a conveyor, so a long VFD-not-ready period ends in a step-register reset. Examples: C6 `Timer 40`, and the C11/C21 filling branch of `Timer 59/79`. This is acceptable, but be aware of it.

### 7.3 OB1
* **Counters:** `HMI PACKET COUNTER OLD` is always called. `NEW` is called only when test bit `M333.3` is set. So the **OLD counter and `"HMI_DB"` are live**, and the CONVEYOR 5 re-sync and the LIGHT BAR are reading the right DB (this reduces finding 3.4). While `M333.3` is on, both FCs write `M143.0..7` and run `Timer 80/81`. Keep `M333.3` off in production.
* ✅ **Faults Monitor (fixed, now `<>D`):** `L "MD 1"; L 0; >I` compares only the **low word** (`MW3` = MB3, MB4). `MB1` (E-stops `M1.x`) and `MB2` (motor faults `M2.x`) never reach `M5.1`. Use `<>D` (not `>D`, because bit 31 would make the value negative).
* Call order: CLEARING runs before the conveyors, and OLD counter runs before them too. This matches the one-scan pulses (`M9.3`) described in §3.
* `HMI COMMS`, `HMI CONTROL` and `LIGHT BAR` aren't called from OB1. Presumably they are called from `"CONTROL"`. Confirm.

### 7.4 DBs
* **DB1 `DB UTILITY`:** every flag used by the code is declared. The start values are `LENGTH_CONST = 0.0` and `WIDTH_CONST = 0.0`. If those are also the actual values, then `MW176`/`MW178` = 0, so the OLD debouncer gets `Debounce_mS = 0` and falls back to `Preset_mS` only. Check the online values. Some comments also don't match the code: T23 "2s" (code 2.5 s), T24 "2.5s" (code 8 s), T35 "20s" (code 30 s).
* **DB4 `COLLATORS DB`:** `Packet_Width_C10_mS` is a DWORD (CONVEYOR 10 uses `+D`, correct). `Packet_Length_C4_mS` is an INT (CONVEYOR 4 uses `+I`, correct, but it overflows at 32.7 s). `Surface_Left_C4` and `Surface_Length_Left_10` are WORDs holding `-D` results, so they are truncated to 16 bits. Encoder data confirms the C10 wheel is 283 mm. The 0.31 mm/pulse in CONVEYOR 10 still doesn't match 283/600 = 0.47 (§4).
* **DB6 / DB8:** instance arrays for the OLD and NEW debouncers. The UDTs `"Sensor Debounce Struct"` and `"Debouncer Counter Struct"` are still missing from the repo.

### 7.5 Still open
Everything else in §2–§4 is unchanged, in particular: elevator `M92.5` fault handling and brake sequencing (§2.5), Clearing `M54.6` (§3.2), Conv 4 REAL math (§3.3), unread disable flags (§3.5/3.6) and guard-door restart (§3.8). Every change above must be tested on the machine before production use: service jog both directions on the flipper and the pivot, an elevator run with the VFD not ready, and a slat / C21 cycle.

---

## 8. Update: FC212 "GENERAL FAULTS"

FC212 builds the fault registers `MB1`–`MB4` and `MB7`, the VFD-ready latch `M11.1`, the overtemp and air faults (`M0.6`, `M0.7`) and the fault lamps. It also answers several earlier "not in the repo" questions:
* `M9.1` = fault-reset buttons `S0.7 OR S2.7 OR E34.1`.
* `M92.5` (elevator fault) is reset by `M9.1`.
* `M11.1` is **latched**. It is set as soon as any VFD-ready input drops (`M11.0`) and is cleared only by the reset buttons. So after a VFD trip, every conveyor stays stopped until the operator presses reset. That design is correct.

FC212 is not called from OB1, so it is presumably called from `"CONTROL"`. Confirm that.

### 8.1 Findings
| # | Sev | Line | Finding |
|---|---|---|---|
| F1 | ✅ | 687–870, 909+ | **Fixed:** the lamp networks now come before the overtemp/fault-code networks. **`BEC` skipped the fault lamps.** The overtemp and fault-code networks end the block with `BEC` as soon as one matches. The lamp networks X120 `H40.2`, X121 `H40.3`, X130 `H40.4` and X134 `H40.5` come **after** them, so they are not executed while an overtemp (`M0.6`) or an `M3.x`/`M4.x` fault is active. The outputs freeze in whatever state they had, so the red fault lamp may never light for exactly those faults. (`H57.2` in HMI CONTROL mirrors `H40.2` too.) **Fix:** move the four lamp networks above the "Elevator OverTemp" network, or replace each `BEC` with `JU` to a label placed after the fault-code networks and before the lamps. |
| F2 | ✅ | 594, 607, 620 | **Fixed:** resets now use `E28.0/1/2`. **Wrong reset input for C21/C22/C23 VFD faults.** `M4.5`, `M4.6` and `M4.7` are set by `E28.0/E28.1/E28.2` but reset by `E13.5/E13.6/E13.7`, which are the C11/C12/C13 ready inputs (copy-paste from the LO line). A C21 fault clears as soon as C11 is OK, even if the C21 VFD is still faulted. `M11.1` still stops the machine, but the HMI no longer shows which drive it is. **Fix:** `A "E 28.0"`, `A "E 28.1"`, `A "E 28.2"`. |
| F3 | ✅ | 28, 910 | **Fixed** (`<>D`, in both FC212 and OB1). **`L "MD 1"; L 0; <>I`** is the same bug as in OB1: it only tests `MW3` (MB3, MB4). `#FAULT_TRIGGERED` therefore ignores E-stops (`M1.x`) and the C0–C3 / elevator faults (`M2.x`). Those don't light lamp X120, and no fault code is written for them. **Fix:** `<>D`. |
| F4 | 🟠❓ | 72–86 | **The 8 s VFD init delay does not mask power-up.** `SP "Timer 4"` only runs while all VFDs are already ready (`M11.0`). While any VFD is still booting, `T4` = 0, so `#INIT_DELAY` = 1 and every VFD fault latches immediately. It only masks the 8 s *after* all drives report ready. As a result, every power-on probably ends with latched faults that need a reset. The intent was probably to delay after `M0.3`, e.g. `A "M 0.3"; L S5T#8S; SD "Timer 4"; A "Timer 4"; = #INIT_DELAY`. |
| F5 | ✅ | LOADER LIFT line 88 | **Fixed:** now `AN "M 7.0"`. Feeder Lift "Ready" `M74.0` used `AN "M 3.7"`, which is the **Conveyor 9** fault slot. That slot is a placeholder that is never set (`AN "M 50.0"`). The Feeder Lift VFD fault is `M7.0`. So the lift does not stop on its own VFD fault, and only `M11.1` catches it. Probably this should be `AN "M 7.0"`. |
| F6 | 🟡 | 289 | "VFD U42.0 Elevator Fault" `M2.2` is **set by `M1.6` (elevator door open)**, not by the drive: the `AN #ELEVATOR_U42_0` line is commented out. The HMI shows "Elevator motor fault" when the door is opened. |
| F7 | 🟡 | 383, 511 | `HMI_DB.SCREEN_CALL_2` is assigned by both register 3 and register 4, so register 4 wins. Faults in MB3 (C4–C9) never pop the screen. **Fix:** OR the two registers. |
| F8 | 🟡 | 786, 867+ | Fault code 0 in `MB183` is used both for "no fault" and for `M3.0` (C4 VFD). The `MB182` codes are `W#16#10..14` (16..20 decimal), not 10..14. `M4.7` (C23) has no code at all. The `E14.6`/`E14.7` overtemp codes `B`/`C` can't be reached because the Pivot network (code 6) already exits on them. |
| F9 | 🟡 | 18–114 | New faults are only latched on the `M6.7` check pulse (or while the register is already non-zero). Detection is therefore delayed by up to one clock period. That is fine for display, but these bits must never be the only stop path. The E-stop and door stops must stay hardwired (they are, since `E0.0`, `E4.6`, `E9.0` and `E12.5` are used directly). |
| F10 | 🟡 | many | Placeholder faults (`AN "M 50.0"`, never set): C0, Pusher 0, Pusher 1, C2 belt/roller, Flipper, C9, Pusher 2, Feeder Fingers. **The C2 belt (U43.4) and C2 roller (U43.5) VFDs have no fault monitoring**, and they aren't in the `M11.0` ready list either. `E14.6`/`E14.7` appear twice in the overtemp OR (harmless). |

### 8.2 Relation to the "VFD OK -Check" changes
The `M11.0` ready list includes C5 (`E7.6`), C6 (`E7.7`) and the TurnTable turn (`E9.5`). Their outputs (`A45.0`, `A45.3`, `A47.x`) are still not gated by `M11.1` (§7.2 item 2). A fault on any of those drives stops everything else, but not the drive's own sequence, which keeps running its timeouts.

F1, F2, F3 and F5 were applied afterwards, along with the OB1 Faults Monitor (`<>D`). After these fixes, E-stops and `M2.x` faults also light lamp X120 and set `M5.1` (the fast blink in OB1). F4 and F6–F10 are still open.

---

## 9. FC1208 "HMI PACKET COUNTER  NEW" + FC8 "DE-BOUNCER / COUNTER" (WIP), the replacement for FC1206 "HMI PACKET COUNTER OLD" + FC6

**Correction (from the symbol table, §10):** FC1208 = `HMI PACKET COUNTER  NEW`, FC1206 = `HMI PACKET COUNTER OLD`, FC8 = `DE-BOUNCER / COUNTER` (the WIP counter), FC6 = `DE-BOUNCER OLD`. This section covers both FC1208 and the FC8 it calls, so the findings stand. Originally this section reviewed `DE-BOUNCER-COUNTER-WIP` (`FUNCTION "DE-BOUNCER / COUNTER"`, instance data in DB8 `"DEBOUNCER COUNTER DB"`) and its caller `HMI PACKET COUNTER  NEW`. The FC1206 source (`"DE-BOUNCER OLD"`, DB6) and both UDTs are not in the repo, so feature parity was judged from the FC1206 call interface in `HMI PACKET COUNTER OLD`.

### 9.1 Is it ready to replace FC1206?
**Not yet.** The Collator path (C3, C4) and the Link path (C5) run, but items P1–P4 below miscount in normal production, and resetting the counts from the HMI or the conveyor FCs does not work (P5). The Delivery type is an empty stub, so C6, C13 and C23 can't be switched over at all.

### 9.2 Findings
Line numbers refer to `DE-BOUNCER-COUNTER-WIP`.

| # | Sev | Line | Finding |
|---|---|---|---|
| P1 | 🟠 | 218–229, 266–286, 318–338, 370–376 | **Only one count-down per exit-sensor blockage.** A decrement happens once per `Bit1_ON_Latch`, and the latch only clears when `Bit_1` goes OFF. On Link conveyors, packets queue nose-to-tail against the end sensor ("End Sensor On When Full"), so `Bit_1` can stay ON while several packets leave, and only **one** is subtracted. The same applies to count-up when packets arrive nose-to-tail. **Fix:** after a decrement, if `Bit_1` is still ON, clear `Bit1_Exit_mS` and `Count_Done_Latch_1` so another packet is subtracted each `Exit_Window_mS`. |
| P2 | 🟠 | 189 | **Spurious extra decrement.** The Bit_0 start resets `Count_Done_Latch_1`. Scenario: a transfer ends with the next packet already sitting on the exit sensor, so `Bit1_ON_Latch` is still set and `Bit1_Exit_mS` is already past the window. The next infeed packet then clears `Done_1`, and the count drops by 1 immediately with no packet leaving. **Fix:** delete line 189. Bit_0 should only touch the Bit_0 latches. |
| P3 | 🟠 | 243–258, 295–310, 402–411 | **The `Bit0_Entry_mS` timer has no end, and the 5 s "stuck" error is backwards.** `Bit0_Entry_mS` stops counting once the packet is counted (about 500 ms). So a sensor that is really blocked **never** reaches 5000, and the error can't trigger. The opposite case does trigger it: a short blip on `Bit_0` sets the latch, `Bit0_Entry_mS` keeps counting with nothing there, and the next real packet more than 5 s later raises a **false** error. After 32.7 s the INT wraps negative, so a packet arriving 33–65 s after a blip is **not counted**. **Fix:** (a) use a separate "Bit_0 ON time" that counts only while `Bit_0` = 1 and resets when it is 0, and use it for the 5 s error; (b) drop the latch if `Bit_0` has been OFF for longer than a gap timeout (for example `Space_Between`), or clamp `Bit0_Entry_mS` at 30000. |
| P4 | 🟠 | caller, NEW line 35 | **C3 can't count in and out at the same time.** C3 is called with `Transfer_Start = B6.4 AND M27.1`, which is the exit sensor itself. Count-up (line 181) needs `Transfer_Start` = 0, so a packet that passes the infeed sensor `B6.2` completely while another packet is on `B6.4` is **never counted**. That is normal on a slat conveyor that fills and empties at the same time. **Fix:** count in and count out independently, or pass the real "transfer to C4" step instead of the sensor. |
| P5 | 🟠 | caller, NEW 519+ / CONVEYOR 5 line 72 / CONVEYOR 6 line 103 | **Count resets don't work.** Every reset writes `0` to `"HMI DB NEW".CONV_x_COUNT`, but none of them clears `DB8.Conveyor_Cx.Count_Result`. The next time the counter FC runs, it copies the old `Count_Result` back to the HMI. **Fix:** give FC1208 a `Reset` input that clears `Count_Result` and all latches, or reset `DB8.….Count_Result` wherever the HMI count is reset. |
| P6 | 🟡 | 411 | `IO_DB.Error` / `Q_Error` can only be cleared by the first-scan init. FC1206 cleared `Count_Error` on the falling edge of the conveyor run signal (see OLD, e.g. `AN "A 44.0"; FP …; R …Count_Error`). Add an `Error_Reset` input and wire it to `M9.1` or the conveyor stop. |
| P7 | 🟡 | 192–212 | `Exit_Window_mS` and `InFeed_Window_mS` are only computed on a Bit_0 start. After a download or restart, the first count-down uses the DB start value: 0 for every conveyor except C4 `InFeed_Window_mS` = 1163. That means an immediate decrement. Compute both windows on every call. The cost is trivial. |
| P8 | 🟡 | 342–360 | Delivery type (`Conveyor_Type = 2`) is empty. `LowSpd_Dimension_mS`, `COUNT_PLUS`, `COUNT_MINUS`, `COUNT_UP_VALUE`, `EXIT_VALUE`, `SPACE_HALF` and `Transfer_Active` are unused. The comments at 232–239 say Link count-up uses `Preset_MIN_mS`, and Collator uses the "Last_Valid_mm" learning; the code does neither (Link uses `InFeed_Window_mS`, and there is no learning). |
| P9 | 🟡 | caller | The FC is only called while the conveyor output is ON. C5 has a 1 s off-delay (`Timer 120`), but **C3 and C4 have none**, although the FC header says one is required. A sensor change right at stop is missed, and a count-down whose window hasn't elapsed yet fires only on the next run. |
| P10 | 🟡 | caller | `Maximum_Count` is written from `HMI_DB.CONVEYOR_MAXCOUNT_L/W` on every call, and the clamp at 390–396 forces the count to `Maximum_Count`. If the HMI value is 0, every count reads 0. Check the HMI default. |
| P11 | 🟡 | caller | FC1206 read **and wrote back** `HMI_DB.CONV_x_COUNT` (`Word_Count` in/out), so an operator could correct a count on the HMI. FC1208 only writes, so any HMI correction is overwritten. Decide whether that feature has to stay. |

### 9.3 What is good
* A single UDT per conveyor instead of 20+ in/out parameters: much cleaner than FC1206.
* Every accumulator uses the real scan time (`OB1_PREV_CYCLE`), so timing is independent of scan time.
* Clamps at 0 and `Maximum_Count`, and a clear header explaining the principle.

### 9.4 Suggested order before commissioning
P5 (reset) → P2 (delete one line) → P3 (stuck timer and latch timeout) → P1 (repeat count-down while blocked) → P6/P7. Then test on C4 alone (`TESTM 400.0`), comparing against FC1206 on the HMI, before moving C3/C5 over. Implement the Delivery type last.

No code was changed for FC1208.

---

## 10. Symbol table (`404_Symbol_Table.asc`)

1,707 entries: 867 M, 192 I, 184 Q, 121 timers, 59 FCs, 13 DBs, 5 UDTs, 7 OBs, 30 VATs. There are no duplicate names or addresses. Every "letter + address" name (`"M 11.1"`, `"K 46.0"`, `"B 6.2"`, …) maps to exactly that address: `E/B/P/S` → I, `A/K/Y/H` → Q, `FP/FN/TESTM` → M. So the code's symbolic names can be read literally, and every finding above holds as written.

### 10.1 Block names that didn't match (fixed)
A name used in the sources that isn't in the table stops the source from compiling, or silently creates a new, uncalled block.

| Where | Was | Table | Action |
|---|---|---|---|
| OB1 | `CALL "FEEDER FINGERS"` | FC1070 `LOADER FINGERS` | ✅ renamed |
| OB1 | `CALL "FEEDER LIFT"` | FC1074 `LOADER LIFT` | ✅ renamed |
| `LOADER FINGERS` file | `FUNCTION "FEEDER FINGERS"` | FC1070 `LOADER FINGERS` | ✅ renamed |
| `CONVEYOR 6 … _ VFD OK -Check` | `FUNCTION "CONVEYOR 6 - FLIP DELIVERY"` | FC1038 `CONVEYOR 6 - FLIP DELIV.` | ✅ renamed back |
| `DE-BOUNCER LINK CONVEYOR FC6` file | `FUNCTION "DE-BOUNCER LINK CONVEYOR"` | FC6 is `DE-BOUNCER OLD`, with a different interface (see the OLD call) | ⚠️ left alone. This file is **not** the current FC6 source. Don't import it over FC6. |

### 10.2 Earlier assumptions, now confirmed or corrected
| Address | Table comment | Effect on the review |
|---|---|---|
| `E15.3` | ELEVATOR MOTOR ENERGIZED | The "Safety Brake" network (`AN E15.3 → R A56.2`) keeps the brake applied until the motor is energised. That covers the "brake opens before torque" concern in §2.5 and §7.2. The code comment "Motor Stopped" is wrong. **§2.5 downgraded.** The `AN M11.1` added in §7.1 stays, as a second layer. |
| `E14.4` | ELEVATOR VFD - H:READY / L:TRIPPED | Confirms the elevator fault path. |
| `M161.0` / `M161.1` | F-KEYS `+` / `-` on LAUER | Two separate keys, so both can be pressed together. This confirms the flipper and pivot interlock fixes were needed. |
| `M3.7` / `M7.0` | VFD U47.5 fault – **Pusher 2 Conveyor 9** / VFD U50.0 fault – **Feeder Lift** | Confirms the LOADER LIFT fix (`M3.7` → `M7.0`). |
| `M54.2` / `M54.6` | CLEARING ON EMPTY LINK / PIVOT C10 FULL SENSING | Confirms §3.2: Clearing uses the wrong bit. **Still open.** |
| `MD1` | HMI E-Stop to Conveyor 23 | Confirms the `<>D` fix in OB1 and FC212. |
| `M2.2` | VFD U42.0 FAULT – ELEVATOR | Confirms FC212 F6 (it is set by the door, not the drive). |
| `M90.0` | FEEDER TEST with 506 Power Off | The feeder light-curtain "buffer" is a **test bypass**. It must never be settable in production. FC300 "LIGHT CURTAIN - SAFETY" (not in the repo) is the likely writer, so review it. |
| `E9.0`, `E12.5`, `E4.6` | SAFETY RELAY – DOOR CLOSED | See the update in §3.8. |
| `E34.1` | PB NEW HMI – SIGNAL | Used as one of the three fault-reset inputs (`M9.1`). |
| `M333.3`, `M400.1` | not in table | `M333.3`: **removed** (2026-11-18), OB1 calls FC1208 directly. `M400.1`: give it a symbol or remove it. |

### 10.3 Blocks that exist in the PLC but not in the repo
FC1 LAUER CALL, FC2 SETUP, FC3/FC9 SENSOR CHECK, FC5 SENSOR DE-BOUNCER, **FC6 DE-BOUNCER OLD**, FC10/FC105 SCALER, FC100–103 LAUER comms, FC190–201 LAUER, **FC211 CONTROL** (start-up routine, probably calls HMI COMMS/CONTROL, LIGHT BAR and FC212), FC245 BLINKER, **FC300 LIGHT CURTAIN - SAFETY**, FC350/351 FM350, FC1046 CONV 8 - TURNTABLE WIP, FC1205 HMI PACKET COUNTER, FC1300 FM350 COUNTERS, FC1500 ELEVATOR TEST FUNCTION. Also OB35 (100 ms), OB82/86/100/121/122, DB2/3/5/10/12/14/18/22/50 and all 5 UDTs.

Priority to add next: **FC211 CONTROL** (it computes `M0.3` and the start-up sequence), **FC300** (light curtain / `M90.0`), **FC6** and **UDT5/UDT8** (so the counter replacement can be compared properly).

---

## 11. Live counter problem: "count-up works, count-down freezes"

**Live chain:** OB1 → FC1206 `HMI PACKET COUNTER OLD` → FC6 `DE-BOUNCER OLD` (DB6, UDT5). FC1208 and FC8 are not in the PLC.

### 11.1 Root cause (from the code)
* The FC6 source isn't in the repo. However, `DE-BOUNCER LINK CONVEYOR FC6` (v0.4) has **the same in/out layout** as UDT5 / the DB6 instance, field by field: 8 rising pulses, 4 front/rear bits, packet-at-end, **bit 6**, sensor error, first-scan, two ON times, result and limit. It is an earlier version of FC6.
* In v0.4, bit 6 is `IO_Count_Done`. It is **set** by every count (up and down), **required to be 0** by every count, and **never reset inside FC6** (§3.9). In DB6 the same bit is called `Count_Error`, and FC1206 resets it only on the conveyor's **stop** edge (for C3, C4, C5, C10 only).
* **Count-up looks fine** because C4 stops after every collated packet, so the stop edge re-arms the bit. **During a transfer** the conveyor runs without stopping: the first packet out sets the bit, and **every following count-down is blocked** until the conveyor stops. C6 and C11–C23 have no stop-edge reset at all.

### 11.2 How to confirm online (1 minute)
In a VAT, watch `"DEBOUNCER OLD".B6_7_Conv_4_InFeed.Count_Error` and `…Word_Count_Result` during a C4 transfer. If `Count_Error` goes TRUE after the first packet leaves and stays TRUE while the count freezes, this is the cause.

### 11.3 Fix applied: FC1206 only, FC6 unchanged
For the 10 conveyors that count down (C4, C5, C6, C10, C11, C12, C13, C21, C22, C23), a re-arm now follows each FC6 call:
```
AN  <Bit_1 passed to FC6>      // exit sensor clear
A   <Transfer_Start>           // during transfer
L   S5T#300MS
SD  T 1xx                      // clear for >= 300 ms
A   T 1xx
R   "DEBOUNCER OLD".<inst>.Count_Error   // re-arm count-done latch
```
* This re-arms once per packet. A U-shaped packet whose opening passes the sensor in under 300 ms still counts only once. Tune the 300 ms if needed; it must be shorter than the smallest gap between packets during a transfer.
* Timers used: **T138 (was T105 - used by LAUER COMM FC in OB35), T106, T107, T108, T111, T112, T113, T114, T115, T117**. None of them is in the symbol table or used by any block in the repo. **Before downloading, check in the PLC's cross-reference that no block outside the repo uses them.**
* The existing stop-edge resets are unchanged.
* **Test order:** C4 alone first (a full collate + transfer cycle, with the count reaching 0), then C5/C6, then C10 and C11–C23.

### 11.4 If it doesn't fix it
Upload the live FC6 source (Export Source from the S7 project). If FC6 differs from v0.4, the fix must go inside FC6 instead: clear `Count_Done` when a new front-end latch is set.

---

## 12. FC1208 v0.3 + FC8 v0.7 + UDT8: replacement for FC1206 + FC6

### 12.1 What changed
**FC8 `DE-BOUNCER / COUNTER` v0.7** (file `DE-BOUNCER-COUNTER-WIP`), rewritten:
| | How it counts |
|---|---|
| **Up** (`Bit_0`, infeed, gated by the caller) | Adds the ON time. **+1** when ON ≥ `Preset_MIN_mS`. Re-armed only after `Bit_0` has been OFF for the **gap** (`Space_DX_mS / 2`, min 100 ms). A U-shaped packet counts once, and a blip shorter than the preset is dropped. |
| **Down** (`Bit_1` = **raw** exit sensor) | ON time is added **only while `Transfer_Start`**, so a packet parked on the end sensor isn't counted. **−1 when the packet has left**: exit sensor OFF for the gap time **and** ON ≥ preset. **Packets that touch** (the sensor never clears): −1 for every `HighSpd_Dimension_mS + gap` of continuous ON time. |
| HMI | New IN_OUT `Word_Count` (like FC6): an operator edit on the HMI, or a reset writing 0, is taken over on the next call. The result is written back every call. **The resets now work.** |
| Error | Infeed continuously ON for ≥ 5 s → `Error`/`Q_Error`. Cleared by the new `Error_Reset` input (wired to `M9.1`). |
| Robustness | All time accumulators are capped at 30 s (no INT wrap). Delivery type counts like the others. `Maximum_Count = 0` means no limit. |

This fixes P1–P8 from §9. It also fixes the "count-down freezes" problem (§11): the count-done flag re-arms on every gap.

**UDT8 `Debouncer Counter Struct` v0.7:** your uploaded `UDT8` (v0.2) was extended with 4 fields at the end (`Bit0_OFF_mS`, `Bit0_Stuck_mS`, `Bit1_OFF_mS`, `HMI_Last`). The existing fields keep their order, and the DB8 source is unchanged.

**FC1208 `HMI PACKET COUNTER  NEW` v0.3**, rebuilt as a **drop-in replacement for FC1206**:
* **All 11 conveyors** are active: C3, C4, C5, C6, C10, C11, C12, C13, C21, C22, C23.
* Counts are written to **`"HMI_DB"`**, the same words FC1206 used, which the HMI, the LIGHT BAR and the C5 re-sync read. They are also mirrored to `"HMI DB NEW"`.
* The infeed gating is the same as FC1206 (fill steps, and pivot position for C11/C21). The exit sensor is raw. Transfer = step active and not done.
* It also does FC1206's other jobs: `MW202` (packet length in mm for Conv 4), and the flipper/turntable/C9/pusher-2 presence words (to both DBs).
* The count resets are the same as in FC1206.
* A 1 s call-hold is used on every conveyor. C3, C4 and C10 get new ones on timers **T118, T119, T134**.
* Packet dimensions: C4/C5/C6 use `HOUSE_KEEPING DB.C4_Packet_Length_mS`. C10–C12 and C21–C22 use the C10 width scaled 27→31 m/min. C13/C23 use the width scaled 27→23.7 m/min.
* The test leftovers (`TESTM 400.0`, `M400.1`, `<>R`) are removed.

**OB1 (historical, superseded 2026-11-18: `M333.3` removed, FC1208 called directly, FC1206 deleted):** `M333.3` then **selected** the counter (0 = FC1206 + FC6, 1 = FC1208 + FC8), and only one of them runs. Both hand the count over through `HMI_DB`, so you can switch online in either direction without losing counts.

### 12.2 What is needed to compile
Nothing can be compiled here: STEP 7 runs on Windows and the full project isn't in the repo. In the **S7 project** (SIMATIC Manager → S7 Program → Sources → *Insert → External Source*), compile in this order:
1. `UDT8`
2. `DB8 WIP` (DB8, built on UDT8)
3. `DE-BOUNCER-COUNTER-WIP` (FC8)
4. `HMI PACKET COUNTER  NEW` (FC1208)
5. `OB1`

These blocks read or write existing blocks that are in the PLC project but not in the repo, so the compile has to happen in that project: DB1 `DB UTILITY`, DB4 `COLLATORS DB`, DB10 `HOUSE_KEEPING DB`, DB12 `HMI_DB` (`CONV_x_COUNT`, `CONVEYOR_MAXCOUNT_L/W`, `*_PACK_PRESENCE`), DB22 `HMI DB NEW` (`CONV_x_COUNT`, `FP131/132`, `*_PACK_PRESENCE`), and the symbol table (already matches). If a field name differs in your DB12/DB22, the compile names it. Send me the error and I'll adjust.

### 12.3 To run (commissioning)
1. Cross-reference **T118, T119, T134** in the online project (they must be unused), and check that `M333.3` is free.
2. Download UDT8, DB8, FC8, FC1208, then OB1. FC1206 keeps running while `M333.3` = 0.
3. VAT: `M 333.3`, plus `"DEBOUNCER COUNTER DB".Conveyor_C4_Collator.Count_Result`, `.Bit1_Exit_mS`, `.Bit1_OFF_mS` and `"HMI_DB".CONV_4_COUNT`.
4. Set `M333.3 = 1` → FC1208 takes over the current HMI counts. Watch a full C4 collate + transfer: the count should go up for each packet in and down to 0 on transfer.
5. Tune if needed: `Preset_MIN_mS` (500 / 300) and `Space_DX_mS` (600 → gap 300 ms) in the FC1208 calls.
6. To roll back, set `M333.3 = 0`. `M333.3` is probably not retentive, so after a power cycle FC1206 runs again until the bit is made permanent (or the switch is removed).

---

## 13. HMI COMMS (FC1200) and HMI CONTROL (FC1100)

### 13.1 HMI COMMS (FC1200): good design, display-only findings
It updates each HMI group only when its inputs change, plus a round-robin refresh (`COUNTER 11` "DISPLAY_REFRESH", 6 groups × 300 ms). It also animates the pushers and elevator by shifting a bit in MB135–139.
* ✅ **Fixed:** the Conveyor 2 fault colour used `M30.7` (C4 timeout fault). It now uses `M22.7` (Angle Conv 2 fault).
* 🟡 Change detection adds input words together (`IW9+IW12+IB15`, `QW42+…+QB54`, …). Different patterns can give the same sum, so the change is picked up late, by the next round-robin pulse (≤ 1.8 s).
* 🟡 After a door closes or an E-stop is reset, the HMI status clears up to about 1.8 s late (those blocks only run while a door is open or an E-stop is active, or on their pulse).
* 🟡 Absolute writes to `DB12.DBB4…7`, `DBB19` and `DBX88.0–2`: check that they still match the DB12 layout.
* 🟡 About 20 unused temps. `PUSHER_2_COLOR` is BOOL while the others are BYTE.

### 13.2 HMI CONTROL (FC1100)
| # | Sev | Line | Finding |
|---|---|---|---|
| H1 | 🟠❓ | 50–52, 104–118 | **`M140.3` "NEW HMI ON – RUN SCREEN CTRLs" = `ON_SW AND SERVICE_SW_3_STATUS`.** The "HMI Service Switch Reset" clears `SERVICE_SW_3_STATUS` after 10 s on screen 0 once the 2145 flap opens (`E34.7`). The flap opens on every packet, so in production `M140.3` drops, and roller "goes through", flipper, turntable direction, hand feed and clearing all switch back to the **LAUER** inputs (`M152.x`, `M150.x`). If the LAUER panel is no longer used, the new-HMI switches stop working without any warning. **Fix:** base `M140.3` on its own bit (e.g. `ON_SW` alone), or don't reset `SERVICE_SW_3_STATUS` in that network. |
| H2 | 🟠 | FC211 181, 190 | **The new HMI "OFF" button does nothing.** `E34.2` → `M146.2` is computed here, but FC211 has it commented out in both the start and the control-voltage-OFF logic. Control voltage `M0.3` goes off only by `S2.1`, E-stop or faults. Either wire `M146.2` in, or remove the button. |
| H3 | 🟡 | 64–68 | `JNB MAIN` skips the whole switch-status section unless the screen changed or the 1.6 s clock pulses. Operator switches (hand feed `M110.0`, roller `M111.0`, flipper `M111.1`, service status) take effect up to **1.6 s late**. The jump crosses networks: legal, but easy to break when editing. |
| H4 | 🟡❓ | 44–46 | The E-stop lamp is `H57.3 = E28.7` ("PB NEW HMI – E-STOP"). If `E28.7` is the E-stop's NC contact, the lamp is ON when the E-stop is **not** pressed. Check the contact type. |
| H5 | 🟡 | 30–38 | The "Clearing" lamp `H57.0` also shows `M5.3` "Defective start – white", and the "Fault" lamp `H57.2` also shows `M5.5` "Defective start – red". This is probably intended (it copies the X120 lamps). Document it for operators. |
| H6 | 🟡 | — | `E34.1` (NEW HMI SIGNAL) is also a **fault-reset** input (FC212 `M9.1`), and FC211 uses it for the "defective start" display. A long press (> 3 s) while start conditions aren't met makes the white/red lamps blink. Harmless, but surprising. |
| H7 | 🟡 | temps | `CLEARING_ON` is declared and never used. |

---

## 14. CONVEYORS CLEARING (FC1011): detailed review

**What it does:** clearing empties the line at the end of an order, stage by stage: elevator + C1/C2 (`M10.1`) → slat C3 (`M10.2`) → collator C4 (`M10.3`) → C5/C6 (`M10.4`) → C7–C9 (`M10.5`) → pivot C10 (`M10.6`). Then the **new-order sequence** (`M7.4 → M7.5 → M7.6 → M7.7 → M8.0 → M8.1 → M8.2`) holds the pivot (`M8.4`) until C11–C23 and the feeder have run out the old order, and the operator confirms with **S3.2** (amber lamp `H49.5`).
Start: new-HMI broom switch (`M5.2` = `M140.3` AND `CLEARING_SSW_MAIN`) or LAUER **F4** (`M150.4`). Stop: normally when C10 is cleared (`M10.6` → `MB10` := 0).

| # | Sev | Line | Finding | Proposed fix |
|---|---|---|---|---|
| CL1 | 🟠 | 20–22, 280–284 | **A clearing started from the new HMI can abort by itself.** `M5.2` includes `M140.3`. When `M140.3` drops (HMI CONTROL H1: 10 s on screen 0 and the 2145 flap opens), `M5.2` falls. Its falling edge is read as "operator switched clearing off" → `M5.4` **CLEARING ABORT**, and the new-order flags are cancelled too (line 552). | Detect the abort from the HMI switch itself: `A "HMI_DB".CLEARING_SSW_MAIN; FN "FN 155.6"; A "M 140.3"; A "M 10.0"; = "M 5.4"`. Then a drop of `M140.3` no longer aborts. |
| CL2 | 🟠 | 37–47 | **"C11…C23 already empty" (`M54.2`, Case B) is only checked on an HMI start.** A LAUER F4 start never checks it, so it always runs Case A: the pivot is held (`M8.4`) and the operator must press S3.2 even when the lines were already empty. The two panels behave differently. | Check it on the start of `M10.0`, whatever the source: replace `A "M 5.2"; FP "FP 147.4"` with `A "M 10.0"; FP "FP 147.4"`. |
| CL3 | 🟡 | 473 | `A "M 54.6"` (pivot C10 **full** sensing) where the comment and logic say "Empty C11…C23" (`M54.2`). This resets `M8.5` "Clearing done" when C10 becomes full, so the clearing-done lamp goes out early. | `A "M 54.2"`, or delete the 2 lines (in Case B `M8.5` is never set anyway). |
| CL4 | 🟠 | 295–310 | **Only one stage has a timeout:** C4, after 30 s (`Timer 128`). If the elevator/C1/C2 never empty (`M10.1`), or C5–C10 never confirm, clearing stays on with no alarm. Meanwhile `K41.0` "Trans System OK → 2145" is OFF (`AN M10.0`), so **the 2145 stays stopped**. | Add an overall clearing timeout (e.g. 3–5 min while `M10.0`) that sets an alarm and clears `MB10`. |
| CL5 | 🟡 | 334–338 | **"Elevator + Conv 1,2 NOT EMPTY" alarm (`M11.4`)** is set at the start of **every** clearing, because the line is never empty at the start. Nothing in the PLC resets it. | Set it only if not empty after a delay (e.g. 60 s), and reset it on `M9.1` (fault reset) or when the clearing ends. |
| CL6 | 🟡 | 255–263 | `Clearing Done - Ready` sets `M9.7` = `(M0.3 AND T9) OR NOT M11.6`, so it is ON almost all the time. `M9.7` isn't used anywhere in the repo. | Remove it, or fix it if the LAUER panel reads `M9.7`. |
| CL7 | 🟡 | 452–459 | `M9.3` "trigger 1 scan" is actually ON for **1 s** (`Timer 58` SE). It starts filling on **both** C11 and C21, whatever the pivot position. The conveyor not facing the pivot runs empty until its 30 s timeout. Harmless. | Accept as-is, or AND it with `P15.1`/`P15.0` in C11/C21. |
| CL8 | 🟡 | 345–349, 504–517 | Not used: `Timer 10` (started, never read; the title says 3 s, the code says 2 s), `M11.7`, `M142.0` (unless the LAUER panel reads them), and `M9.6` (C3). | Cleanup only. |
| CL9 | 🟡 | 286–293, 297–310 | The **normal end** of clearing goes through `#CLEARING_ABORT` (`O "M 10.6"`). It works only because the "Clearing Done" network (467) runs after `M10.6` is set and before `MB10` is cleared on the next scan. This is fragile if the networks are ever moved. | Rename it, or clear `MB10` in a separate "clearing done" network after line 474. |

**Dual-panel note:** with both panels in use, CL1 and CL2 are the ones operators will notice. The same clearing behaves differently depending on which panel started it, and an HMI-started clearing can stop by itself.

### 14.1 "Packets left on C10 after clearing" (intermittent): root cause and fix ✅
**Root cause:** clearing declares C10 done (`M10.6`) when **all** of these are true:
`M10.5` (C3–C9 cleared) AND `M58.3` (C10 finished *one* transfer and stopped) AND the receiving exit sensor is clear (`B10.7` C11 / `B15.4` C21, or the `Timer 57` bypass) AND the 1 s clock.
**Nothing checks C10 itself.** A C10 transfer ends as soon as C11/C21 reports full (`M59.2`/`M79.2`: first packet at its exit sensor) or after 20 s (`Timer 55`). If more packets are on C10 than C11/C21 can take, or the transfer ends before the last packet has crossed, the rest stay on C10. C10 is only called once during clearing (`M9.3` / `M58.2` are one-shot). When C11 later empties its exit sensor, clearing ends with those packets still on C10. It is intermittent because it depends on how many packets C10 holds, how much room C11/C21 has, and timing.
> **Correction (operator input):** a transfer only starts when the receiver is **empty**, and it is always a **complete** transfer. C11/C21 call C10 only after their own register has reset, and C10 holds the same amount. So "C10 transfers part of its load and waits" is **not** the mechanism (an earlier note here said so). Leftovers are packets that reached C10 **after** the last clearing transfer, or that C10 never registered. Most likely: Pusher 2 pushes the last packet onto an idle C10, but C10 step 11N2 only starts if `B10.3` sees it while `M51.7` is set and `M52.1` is not. If it misses that narrow window, C10 never runs, `M58.3` stays set, and clearing reports done. In production the next push carries the packet along, so it is never noticed.
> **To confirm on site:** check where the packets are left on C10. Near `B10.3`/`B10.4` means a late push that was not registered. Spread along C10 means the transfer ended early; record `M55.0`–`M55.6` and `M58.3`.
> The fix is unchanged: C10 must be proven empty, and the re-call uses the normal C11/C21 call (receiver empty → one complete transfer).

**Fix (CONVEYORS CLEARING only, active only while clearing `M10.0`):**
1. **C10 proven empty (`M10.7`):** the C10 exit sensor `B10.6` must stay clear while the belt runs fast (transfer) for **10 s** (`T137`), long enough for a packet to cross the whole belt. Any packet seen on `B10.3` / `B10.4` / `B10.5` / `B10.6`, or a Pusher 2 push (`M51.7`), cancels the proof. `M10.7` sits in `MB10`, so it is cleared automatically when clearing ends.
2. **Call C10 again:** while clearing, C3–C9 are cleared, and C10 is not proven empty, `M58.2` is re-armed each time C10 is back to idle after a transfer. C11/C21 then call C10 to transfer again, until C10 is empty.
3. **"C10 cleared" now also requires `M10.7`.**

**Effects to expect:**
* Clearing can take about 20–30 s longer when C10 has to prove it is empty (an empty transfer runs until `Timer 55`, 20 s).
* If C10 cannot unload (C11/C21 blocked, or a C10 fault `M54.7`), clearing **waits** instead of ending with packets left. See CL4: an overall clearing timeout is still recommended.
* **Tune** `S5T#10S` = C10 belt length ÷ 0.52 m/s + 1 s.
* **Before download:** cross-reference `T137` and `M10.7` in the PLC. Both are not in the symbol table and not used in the repo.

### 14.2 Packets left near the C10 infeed: corrected analysis
~~Pusher 2 → C10 start race~~ **Withdrawn:** the operator confirms the leftover packets **were collated**. So C10 collator mode worked, but **no transfer actually moved the collated group**, and clearing still ended. There are two possible paths:
1. **Normal end after a "transfer" that barely ran.** `M58.3` is set at the end of step 11N7 whenever C11/C21 reports full (`M59.2`/`M79.2`), even if the C10 belt hardly moved. If C11/C21's register reads empty (idle after a 30 s running timeout or a register reset) while a packet is still on it, the transfer ends almost at once. Clearing reports done once C11/C21 has passed its packets on. **The fix in §14.1 covers this:** a short run never gives the 10 s "proven empty" proof, so C10 is called again until a complete transfer has run.
2. **Clearing switched off before reaching C10.** `Timer 128` (C4 not confirmed cleared within 30 s → `MB10` := 0, no alarm), `Timer 109` (C10 belt running 1 min → `R M10.0`), or an operator abort. C10 is never called. This is **not** covered by §14.1; see CL4 (overall timeout + alarm instead of a silent stop).
**On site:** after a clearing that left packets, check whether the amber New Order lamp `H49.5` and the S3.2 confirmation happened. Yes → path 1. No (and the clearing lamp went off early) → path 2.
The `B10.3`/`M51.7` proof resets added in §14.1 are kept as extra safety.

### 14.3 Order change (A → B): "S3.2 confirmation skipped, orders joined" and "order A packets left on C10"
**Process (operator):** order A finished → clearing called → TS no longer fed (`K41.0` off while `M10.0`) → C1–C10 empty into C11–C13/C21–C23 while the bottomer finishes A → clearing ends → order B fed into TS → C10 fills with B and is **held** (`M8.4`) until the bottomer has finished A → S3.2 lamp (`H49.5`) → operator confirms → C10 sends B.
**Both symptoms mean A and B get mixed.** Ways the hold is skipped or clearing ends too early:

| # | Cause | Panel | Status |
|---|---|---|---|
| A | `M54.2` "C11…C23 already empty" (Case B = **no hold**) is decided at an HMI start from the **exit/slow sensors only**. Packets of A between sensors are invisible, so it decides "empty" → no hold → no S3.2. | New HMI only | **Open: decision needed** (see below) |
| B | CL1: when `M140.3` drops, `M5.2` falls → read as "switch OFF" → `M5.4` abort → clearing stops (C10 not emptied, so **A left on C10**) **and** the new-order hold is cancelled (**orders joined**). | New HMI only | ✅ **Fixed:** abort only on a real `CLEARING_SSW_MAIN` OFF while `M140.3` = 1 |
| C | SIGNAL (`E34.1`, also a fault reset) held ≥ 3 s while waiting → `M5.0` → hold cancelled. | Both | Open: operator training, or remove `M5.0` from "Clearing - Cancelling" |
| D | LAUER F4+ENT+CLR abort; `Timer 128` (C4 30 s) or `Timer 109` (C10 1 min) switching clearing off silently. | Both | Open: CL4 (timeout + alarm instead of a silent stop) |
| E | Clearing ends with packets still on C10. | Both | ✅ **Fixed** (§14.1: C10 must be proven empty) |

**Proposal for A:** always hold C10 and always require S3.2 after a clearing (remove Case B). Operators confirm every order change, which is safe and simple. The alternative is to make the "empty" check use step registers as well as sensors, and to run it on any start (CL2), but it can still be fooled.

### 14.4 Status (operator, 2026-11-17)
* `T137` and `M10.7` confirmed **unused** in the PLC project.
* The machine is in production, so **no download yet**. The clearing changes (§14.1, §14.3 B) wait for a maintenance window.
* While waiting, monitor **read-only** in a VAT during a real order change: `M10.0`, `M10.5`, `M10.6`, `M58.3`, `M55.0`–`M55.6`, `M54.2`, `M5.4`, `M5.0`, `M8.4`, `M8.5`, `M140.3`, `"HMI_DB".CLEARING_SSW_MAIN`, `T128`, `T109`. This shows which path (§14.3 A–D) happens on this machine.

### 14.5 ROOT CAUSE FOUND: clearing switches itself off when C4 is empty (S5 `Timer 33` never started) 🔴
**Operator facts:** the new HMI is only used for service (`M140.3` = 0 in production). Clearing is always started from **LAUER F4**. Operators do not abort it.
→ `M54.2` is never set, so a **normal** end of clearing (`M10.6`) **always** sets the S3.2 hold (`M8.4`). A skipped S3.2 therefore means clearing **did not end normally**.

**Chain:**
1. "C4 cleared" `M10.3` = (`M31.5` **OR S5 `"Timer 33"`**) AND `M10.2`. S5 `Timer 33` is **started nowhere**: CONVEYOR 4 was converted to the soft timer `"DB UTILITY".T33_DN` (20 s), and the clearing block was not updated.
2. If **C4 is empty** when clearing reaches it, no packet reaches `B7.0`, so `M31.5` (via `M30.6`) never comes and `M10.3` never comes.
3. `Timer 128` (30 s from "C3 cleared") then sets **`MB10` := 0: clearing is switched off silently.**
4. C10 is never called, so its **collated order-A group stays near the infeed**.
5. `M10.6` never comes, so **no `M8.4` hold, no S3.2 lamp**.
6. `K41.0` is on again, so **order B is fed**, collates behind A on C10, and both are transferred together **without a gap**.
Intermittent: it only happens when C4 is empty at that moment.

**Fix applied:** `O "Timer 33"` → `O "DB UTILITY".T33_DN`. C4's own 20 s clearing run now confirms "C4 cleared" before `Timer 128` (30 s). OB1 calls CLEARING before CONVEYOR 4, so it sees `T33_DN` in the scan after C4 sets it. That is enough because `M10.3` is latched.
**Confirm online before the window (read-only):** during a clearing with C4 **empty**, watch `M10.2`, `M10.3`, `T128`, `"DB UTILITY".T33_DN`, `M10.0`. Expected today: `M10.3` stays 0, and `M10.0` drops 30 s after `M10.2`.
**Still recommended (CL4):** `Timer 128` should raise an alarm instead of silently clearing `MB10`.

### 14.6 Operator answers (2026-11-17) and resulting changes
* **S3.2 always required: YES.** ✅ Applied: the "Clearing Done" network sets `M8.4` hold on every normal end. The Case B gate `AN M54.2` and the wrong `A M54.6 / R M8.5` lines are removed. `M54.2` is still computed but no longer used.
* **SIGNAL held ≥ 3 s: NO.** Cause C excluded.
* **Clearing lamp goes off early: NO** (as seen by operators). The lamp only shows `M10.0`, so a `Timer 128` stop looks the same as a normal end. The reliable sign is the **missing S3.2 lamp**. With aborts, SIGNAL and HMI excluded, nothing can cancel `M8.4` once it is set. So a skipped S3.2 means `M10.6` was never reached, i.e. clearing was switched off by `Timer 128` (fixed in §14.5) or `Timer 109`. Confirm with the read-only VAT in §14.5.

**Clearing block now contains, for the next maintenance window:**
1. §14.5: `T33_DN` instead of S5 `Timer 33` (**root cause**).
2. §14.1: C10 must be proven empty (10 s, `T137` / `M10.7`) before "clearing done", with a re-call of C10 until it is.
3. §14.6: S3.2 hold always required.
4. §14.3 B: abort only on a real HMI switch-off (harmless while `M140.3` = 0).

## 15. Full PLC export (`ALL_BLOCKS.AWL`, 2026-11-17): what the project contains

The export is split into one file per block in `PLC_EXPORT_2026-11-17/`, named by address (`FC1011 - CONVEYORS CLEARING.AWL`, …). That folder is the **reference copy of the code running in the PLC** (confirmed by the operator, 2026-11-17: everything in the export runs, and the original problems are still there). The files at the repo root are the working copies, with the pending fixes.

### 15.1 Which version runs in the PLC

The September fixes (FC212 E28.x, HMI COMMS `M22.7`, LOADER LIFT/FINGERS, conveyor interlocks, FC8 v0.7 + FC1208 v0.3) **are running**. None of them touches the clearing chain, so the clearing problems are expected to be unchanged.

| Block | Running in the PLC | Fixes from this review **not loaded yet** |
|---|---|---|
| Conveyors 0–23, Elevator | The **"VFD OK -Check"** versions (`M11.1` interlocks) | C3 and C21: `R #INITIALISATION`. C6: `CLR / = #INITIALISATION`. All other conveyor fixes are in (C7 CW/CCW interlock, C10 UP/DN, …) |
| CONVEYORS CLEARING FC1011 | **Original** (not modified, as planned). None of the §14 fixes. **This is why the C10 leftovers and the skipped S3.2 are still there** | All of §14: `T33_DN` (root cause), C10 proven empty (`T137` / `M10.7`), S3.2 always, abort fix. Planned for the Phase 0 trial between shifts |
| GENERAL FAULTS FC212 | Fixed (E28.x resets, `<>D`, lamps) | None. Note: `Timer 4` (VFD ready check) is **15 s** in the project, 8 s in the original. Kept at 15 s |
| LOADER LIFT / FINGERS, HMI COMMS | Fixed | None |
| FC8 v0.7, UDT8, DB8 | Same as the repo (UDT8 field order differs, OK because FC8 is symbolic) | None |
| FC1208 | The repo version, **edited by you**: presence words and `FP131/132` go to `"HMI_DB"` (as FC1206 did), no mirror to `"HMI DB NEW"` | None. Your edit is correct and is now the repo version |
| OB1 | Calls **FC1208 directly** (FC1206 commented out, no `M333.3` selector) | Faults monitor: `>D` → `<>D` (MD1 is negative when `M1.7` = 1, so that fault does not raise `M5.1`). Now in the repo OB1 |
| FC1206 | **Deleted** from the project (2026-11-17) and **not in the CPU** | Rollback to the old counter = re-insert FC1206 from the repo (`HMI PACKET COUNTER OLD`, uses `T138`, not `T105`) + FC6 + DB6, and swap the calls in OB1 |

### 15.2 New findings from the blocks seen for the first time

| # | Sev. | Block | Finding | Action |
|---|---|---|---|---|
| E1 | ✅ (FC1206 deleted) | FC1206 (repo) / OB35 | The FC1206 count-down re-arm used **`T105`**, which is the LAUER comms timeout timer (`LAUER COMM FC`, `TIMT := T 105` in OB35). Running both would have broken the LAUER comms | **Fixed in the repo:** FC1206 now uses `T138` (free). FC1206 is in the project but not called, so no effect today |
| E2 | 🟠 | OB35 (100 ms) | FC212 GENERAL FAULTS, FC1100 HMI CONTROL, FC1200 HMI COMMS and FC1090 LIGHT BAR run in **OB35**, not OB1. They interrupt OB1 and write M bits and timers that OB1 blocks also use (e.g. `M11.1`, `M5.x`). The values are consistent bit by bit, but a bit can change in the middle of an OB1 network | Keep in mind for the spec. Write once, read many: no new writer of an M bit in both OB1 and OB35 |
| E3 | 🟡 | OB82, OB86, OB121, OB122 | All **empty**. The CPU stays in RUN on I/O, rack, programming and access errors, and nothing records them. A wrong DB access in a new block (FC8/FC1208) would go unnoticed | Add an error counter + last-error word (one network each) and show it on the new HMI service page |
| E4 | 🟡 | OB100 | `HMI_DB.AERIAL_LINK_RUN_PB` is **toggled** at each restart (`AN x; = x`) instead of set or reset | Check what the HMI expects. Use `S` or `R` |
| E5 | ✅ | OB100 | Resets `FirstScan_Done` of all 11 DB8 channels on a restart (good, FC8 re-initialises) | — |
| E6 | ✅ | Timers | No S5 timer is started in two blocks. `T118–T127`, `T134` (FC1208) and `T137` (clearing fix) are free in the project | — |
| E7 | ℹ️ | `"HMI DB NEW"` | Only CONVEYOR 5 and 6 still write it (count reset to 0). Nothing reads it. It can be removed after the LAUER panel is retired, or the two writes changed to `"HMI_DB"` | Low priority. The count resets in C5/C6 still do not clear FC8's `Count_Result` (P5) |

### 15.3 To bring the PLC up to the repo (between shifts, one block at a time)
1. **FC1011 CONVEYORS CLEARING** (Phase 0 trial, highest value: fixes the C10 leftovers and the skipped S3.2).
2. **OB1** (`<>D`, one line).
3. **CONVEYOR 3**, **CONVEYOR 21**, **CONVEYOR 6** (init fixes, from the "VFD OK -Check" files).

## 16. C23 counts down by 2 per packet (6 > 4 > 2 > 0, sometimes 6 > 4 > 2 > 1 > 0)

**Cause.** In the delivery step (`M87.4`, not `M87.5`) the C23 belt runs only while the loader is ready: `A54.0 = M87.4 AN M87.5 A M70.0`. When the loader is busy, `M70.0` drops and C23 **stops with a packet on the exit sensor `B15.7`**, but the step stays active. FC1208 gives FC8 `Transfer_Start = M87.4 AN M87.5`, so FC8 keeps adding the exit-sensor ON time of the **stopped** packet. Once it passes `DIM_237 + 300 ms`, the butted-packet rule counts −1. When the packet finally leaves, the rest of the time (≥ 300 ms) counts −1 again. Result: **−2 for one packet**. Sometimes the loader does not stop C23 long enough (last packet), so only −1 is counted: 6 > 4 > 2 > 1 > 0.

C13 (`M67.4`, `A49.0`, also `M70.0`) has the same structure and the same risk.

**Fix (FC1208 v0.4, two lines):** `Transfer_Start` also requires the belt release, so time is only added while the belt moves:
```
A "M 87.4"; AN "M 87.5"; A "A 54.0"; = #XFER;   // C23
A "M 67.4"; AN "M 67.5"; A "A 49.0"; = #XFER;   // C13
```
No change to FC8, the conveyors or the DBs. Download FC1208 only, between shifts.

**Check with a VAT** during one delivery: `"DEBOUNCER COUNTER DB".Conveyor_C23_Delivery.Bit1_Exit_mS`, `.Exit_Window_mS`, `.Count_Result`, `B 15.7`, `A 54.0`, `M 70.0`. After the fix, `Bit1_Exit_mS` must stop increasing while `A54.0` = 0.

**If it still counts 2 with the belt running all the time:** the delivery speed (slow, `A54.2`) is lower than the 23.7 m/min `DIM_237` is scaled to, so a single packet stays on the sensor longer than `DIM_237 + 300 ms`. Then read `Exit_Window_mS` and the highest `Bit1_Exit_mS` for one packet, and correct the scaling of `DIM_237`.
