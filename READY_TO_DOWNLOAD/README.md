# READY TO DOWNLOAD — start here

**Branch:** `claude/quirky-maxwell-k2oybu` (not `main`). On GitHub: *Code* → branch selector (top left, says `main`) → choose **`claude/quirky-maxwell-k2oybu`** → open the folder **`READY_TO_DOWNLOAD`**.
Or open the pull request **#1** → tab *Files changed*: https://github.com/michelcrou7575-eng/404-Trans-System/pull/1

This folder always holds the **latest** version of each block to load. Older versions are only in the git history.

| # | File | Block | Version | Status | What it fixes | Details |
|---|---|---|---|---|---|---|
| 1 | [ALL_NEW_FC9xx.AWL](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/ALL_NEW_FC9xx.AWL) | FC911…FC986 | 2026-11-18 | ✅ PLCSIM OK | FC911 = clearing fix (C10 leftovers, S3.2 skipped). FC924/938/978 = init fixes. FC986 = C23 fault reset like C13. Others = copies | [NEW_FC9xx/README.md](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/NEW_FC9xx/README.md) |
| 2 | [OB0001 - CYCLIC (FC9xx switches).AWL](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/OB0001%20-%20CYCLIC%20%28FC9xx%20switches%29.AWL) | OB1 | 2026-11-18 | ✅ PLCSIM OK | Old/new switch per block (`M280.0`…`M282.4`, all 0 = as today) + `CALL FC 1210` (width measure). **Compile #6 first** | same |
| 3 | [NEW_FC9xx_SYMBOLS.asc](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/NEW_FC9xx_SYMBOLS.asc) | Symbols | 2026-11-18 | — | Names for FC911…FC986 and the switch bits | same |
| 4 | [FC1208 - HMI PACKET COUNTER NEW v0.8.AWL](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/FC1208%20-%20HMI%20PACKET%20COUNTER%20NEW%20v0.8.AWL) | FC1208 | **v0.8** | ⏳ to test | **= running v0.3 + C13/C23 only**: count down only a packet the exit sensor (`B11.2` / `B15.7`) saw on the edge and saw leaving, once per delivery (U-shape double count). C12/C22 unchanged (as v0.3) | [CODE_REVIEW.md](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/CODE_REVIEW.md) §16.3–16.7 |
| 6 | [PACKET_WIDTH_MEASURE.AWL](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/PACKET_WIDTH_MEASURE.AWL) | UDT10, DB30, FC1211, FC1210 | v0.7 | ⏳ not compiled yet | **Measurement only:** packet width at C10 transfer with B10.5 + B10.6, in **mm (encoder) and mS (measured, for C11…C23 which have no encoder)**, verified. Writes only DB30 | [PACKET_WIDTH/README.md](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/PACKET_WIDTH/README.md) |
| 7 | [PACKET_WIDTH_SYMBOLS.asc](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/PACKET_WIDTH_SYMBOLS.asc) | Symbols | v0.1 | — | **Import before compiling #6** | same |

## Order (one per shift window, ~10 min)
1. Office: import #3, compile #1 and #2 (done in PLCSIM ✅).
2. Window A: download FC911…FC986 + OB1 (all switches 0 → no change). Then at the next order change: `M280.0` = 1 (new clearing).
3. Window B: keep a copy of FC1208 v0.3, download FC1208 **v0.8**. VAT C23: `B 15.7`, `M 87.5`, `M 283.1`, `T 138`, `CONV_23_COUNT`. VAT C13: `B 11.2`, `M 67.5`, `M 283.3`, `T 139`, `CONV_13_COUNT`. Rollback = v0.3. (FC8 stays the running v0.7). VAT C23: `B 15.7`, `M 87.5`, `M 283.1`, `T 138`, `…Conveyor_C23_Delivery.Count_Result`. VAT C13: `B 11.2`, `M 67.5`, `M 283.3`, `T 139`, `…Conveyor_C13_Delivery.Count_Result`.

## Change log (latest first)
| Date | Block | Change |
|---|---|---|
| 2026-11-19 | Packet width v0.7 | Transfers with no packet (clearing re-call of C10) counted in `Empty_Count`, not `Bad_Count`. DB30 changed: download DB30 + FC1210, then **check `Enc_Direct` actual = TRUE** |
| 2026-11-19 | **IN THE PLC** | New FM350-2 HW Config (`PIW 334` = C10), width measure v0.6 (UDT10, DB30, FC1211, FC1210), **FC911–FC986 + OB1** (all switches 0). Downloaded during maintenance |
| 2026-11-19 | Packet width v0.6 | `Enc_Direct` initial value = TRUE (direct `PIW 334` by default) |
| 2026-11-19 | Packet width v0.6 | Direct read = 16-bit word `PIW 334` (Ch5, after HW config), wrap-safe. Order confirmed: right column = lower address (`PIW 328` = Ch0 today) |
| 2026-11-18 | Packet width v0.5 | Encoder source switchable online: `ACT_CNTV5` (read job, ~100 mS old) or direct `PID` (every scan), address in DB30 |
| 2026-11-18 | Packet width v0.4 | Encoder factor + C10 speed calibrated on every transfer from the B10.5→B10.6 distance (527 mm). UDT10/DB30 changed: download UDT10, DB30, FC1211, FC1210 together |
| 2026-11-18 | Packet width v0.3 | Delivery width (`Width_ms_237`) removed: not needed |
| 2026-11-18 | Packet width v0.2 | Width also measured in mS (C11…C23 have no encoder) + speed check |
| 2026-11-18 | UDT10, DB30, FC1210/1211 + OB1 | Packet width measure (measurement only), called in OB1 after C10 |
| 2026-11-18 | FC1208 v0.8 | Back in the folder for a clean test: running v0.3 + C13/C23 delivery count-down only (verified line by line) |
| 2026-11-18 | FC1208 | Operator went back to **v0.3** (running since September): works better than v0.4–v0.11. v0.11 withdrawn |
| 2026-11-18 | FC986 (C23) | Fault reset `M9.1` like C13 (was feeder-box PB `S2.7` only). Low/high lines checked identical |
| 2026-11-18 | FC1208 v0.11 | C12/C22 count up = packets C11/C21 counted down; no own count-up on `B10.7`/`B15.4`; remainder at C11/C21 transfer end moved to C12/C22 |
| 2026-11-18 | FC1208 v0.10 | C12 back to v0.8 (v0.9 worse: C12 = 1). FC8 v0.8 withdrawn (not needed) |
| 2026-11-18 | FC8 v0.8 + FC1208 v0.9 | C12 counted half (butted packets from C11): count-up butted rule, C12 only (`LowSpd_Dimension_mS := #DIM_31`), C12 count-up only while `A48.6` runs |
| 2026-11-18 | FC1208 v0.8 | C13: same as C23 (`B11.2`, `M67.5`, `M283.2/283.3`, `T139`) |
| 2026-11-18 | FC1208 v0.7 | C23: count-down only for a packet seen by `B15.7` (replaces v0.4–v0.6) |
| 2026-11-18 | FC8, FC911, FC1208 | Your layout (`//;` between logic groups). Code unchanged |
| 2026-11-18 | FC911…FC986 + OB1 | New block numbers with old/new switch. PLCSIM OK |
