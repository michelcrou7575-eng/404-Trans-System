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
| 5 | 🔴❓ | ELEVATOR + PUSHER 1 | VFD/brake fault `M92.5` does not drop brake release `A56.2` or drive release `A63.0`, and is never reset |
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
* `M92.5` is never reset in any block in this repo.
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
* 🟠 **Faults Monitor:** `L "MD 1"; L 0; >I` compares only the **low word** (`MW3` = MB3, MB4). `MB1` (E-stops `M1.x`) and `MB2` (motor faults `M2.x`) never reach `M5.1`. Use `<>D` (not `>D`, because bit 31 would make the value negative).
* Call order: CLEARING runs before the conveyors, and OLD counter runs before them too. This matches the one-scan pulses (`M9.3`) described in §3.
* `HMI COMMS`, `HMI CONTROL` and `LIGHT BAR` aren't called from OB1. Presumably they are called from `"CONTROL"`. Confirm.

### 7.4 DBs
* **DB1 `DB UTILITY`:** every flag used by the code is declared. The start values are `LENGTH_CONST = 0.0` and `WIDTH_CONST = 0.0`. If those are also the actual values, then `MW176`/`MW178` = 0, so the OLD debouncer gets `Debounce_mS = 0` and falls back to `Preset_mS` only. Check the online values. Some comments also don't match the code: T23 "2s" (code 2.5 s), T24 "2.5s" (code 8 s), T35 "20s" (code 30 s).
* **DB4 `COLLATORS DB`:** `Packet_Width_C10_mS` is a DWORD (CONVEYOR 10 uses `+D`, correct). `Packet_Length_C4_mS` is an INT (CONVEYOR 4 uses `+I`, correct, but it overflows at 32.7 s). `Surface_Left_C4` and `Surface_Length_Left_10` are WORDs holding `-D` results, so they are truncated to 16 bits. Encoder data confirms the C10 wheel is 283 mm. The 0.31 mm/pulse in CONVEYOR 10 still doesn't match 283/600 = 0.47 (§4).
* **DB6 / DB8:** instance arrays for the OLD and NEW debouncers. The UDTs `"Sensor Debounce Struct"` and `"Debouncer Counter Struct"` are still missing from the repo.

### 7.5 Still open
Everything else in §2–§4 is unchanged, in particular: elevator `M92.5` fault handling and brake sequencing (§2.5), Clearing `M54.6` (§3.2), Conv 4 REAL math (§3.3), unread disable flags (§3.5/3.6) and guard-door restart (§3.8). Every change above must be tested on the machine before production use: service jog both directions on the flipper and the pivot, an elevator run with the VFD not ready, and a slat / C21 cycle.
