# READY TO DOWNLOAD — start here

**Branch:** `claude/quirky-maxwell-k2oybu` (not `main`). On GitHub: *Code* → branch selector (top left, says `main`) → choose **`claude/quirky-maxwell-k2oybu`** → open the folder **`READY_TO_DOWNLOAD`**.
Or open the pull request **#1** → tab *Files changed*: https://github.com/michelcrou7575-eng/404-Trans-System/pull/1

This folder always holds the **latest** version of each block to load. Older versions are only in the git history.

| # | File | Block | Version | Status | What it fixes | Details |
|---|---|---|---|---|---|---|
| 1 | [ALL_NEW_FC9xx.AWL](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/ALL_NEW_FC9xx.AWL) | FC911…FC986 | 2026-11-18 | ✅ PLCSIM OK | FC911 = clearing fix (C10 leftovers, S3.2 skipped). FC924/938/978 = init fixes. Others = copies | [NEW_FC9xx/README.md](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/NEW_FC9xx/README.md) |
| 2 | [OB0001 - CYCLIC (FC9xx switches).AWL](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/OB0001%20-%20CYCLIC%20%28FC9xx%20switches%29.AWL) | OB1 | 2026-11-18 | ✅ PLCSIM OK | Old/new switch per block (`M280.0`…`M282.4`, all 0 = as today) | same |
| 3 | [NEW_FC9xx_SYMBOLS.asc](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/NEW_FC9xx_SYMBOLS.asc) | Symbols | 2026-11-18 | — | Names for FC911…FC986 and the switch bits | same |
| 4 | [FC1208 - HMI PACKET COUNTER NEW v0.8.AWL](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/READY_TO_DOWNLOAD/FC1208%20-%20HMI%20PACKET%20COUNTER%20NEW%20v0.8.AWL) | FC1208 | **v0.8** | ⏳ not compiled yet | C13 + C23 count down by 2 (U-shape packet): −1 only for a packet seen on the edge and seen leaving, once per delivery | [CODE_REVIEW.md](https://github.com/michelcrou7575-eng/404-Trans-System/blob/claude/quirky-maxwell-k2oybu/CODE_REVIEW.md) §16.3–16.4 |

## Order (one per shift window, ~10 min)
1. Office: import #3, compile #1 and #2 (done in PLCSIM ✅).
2. Window A: download FC911…FC986 + OB1 (all switches 0 → no change). Then at the next order change: `M280.0` = 1 (new clearing).
3. Window B: compile + download #4 FC1208 v0.8. VAT C23: `B 15.7`, `M 87.5`, `M 283.1`, `T 138`, `…Conveyor_C23_Delivery.Count_Result`. VAT C13: `B 11.2`, `M 67.5`, `M 283.3`, `T 139`, `…Conveyor_C13_Delivery.Count_Result`.

## Change log (latest first)
| Date | Block | Change |
|---|---|---|
| 2026-11-18 | FC1208 v0.8 | C13: same as C23 (`B11.2`, `M67.5`, `M283.2/283.3`, `T139`) |
| 2026-11-18 | FC1208 v0.7 | C23: count-down only for a packet seen by `B15.7` (replaces v0.4–v0.6) |
| 2026-11-18 | FC8, FC911, FC1208 | Your layout (`//;` between logic groups). Code unchanged |
| 2026-11-18 | FC911…FC986 + OB1 | New block numbers with old/new switch. PLCSIM OK |
