# VAT "Clearing sequence" (FC911 v0.1): bits in the order they turn on

Paste the **Address** column into a VAT (one per line), display BOOL (timers: SIMATIC_TIME).

## A. Clearing (after F4)
| # | Address | Symbol / meaning | Turns ON when | Then |
|---|---|---|---|---|
| 1 | `M 150.4` | LAUER F4 (or `M 5.2` = new HMI broom switch) | Operator starts clearing | Reset by FC911 when clearing ends |
| 2 | `M 10.0` | **Clearing CMD** | Right after F4 | Stays ON until clearing done. `K41.0` (TS OK → 2145) goes OFF: feeding stops |
| 3 | `M 8.4`, `M 8.5` | Hold / clearing done (from the previous order) | — | **Reset at clearing start** (v0.1, `FP M283.4`) |
| 4 | `T 128` | Clearing timeout 30 s (C1-C2 cleared, C3 cleared, C4 not yet) | Runs while waiting for C4 | **Must NOT reach 0** (it would switch clearing off) |
| 5 | `M 10.1` | Elevator + C1, C2 cleared | Those are empty | → C3 slat clearing (`M 26.7` = slat full belt cycle) |
| 6 | `M 10.2` | C3 slat cleared | C3 belt cycle done | → C4 clearing after 3 s (`T 10`) |
| 7 | `"DB UTILITY".T33_DN` | C4 clearing timeout done (soft timer, **was S5 Timer 33 = never ran**) | C4 had nothing / timed out | Allows `M 10.3` even with C4 empty |
| 8 | `M 10.3` | C4 cleared | C4 empty (`M 31.5`) or `T33_DN` | → C5, C6 after 3 s (`T 11`) |
| 9 | `M 10.4` | C5, C6 cleared | Empty | → C7 |
| 10 | `T 56` → `M 10.5` | C7, C8, C9 cleared (3 s delay) → **C10 upstream cleared** | Empty | Sets `M 58.2` (call C10) + pulse `T 58` (1 s) |
| 11 | `M 58.2` | Call C10 transfer | With `M 10.5` | Reset when C10 starts transferring |
| 12 | `M 9.3` | Clearing trigger C11/C21 (1 scan, with `T 58`) | `T 58` + `M 10.0` | v0.1: only the pivot side starts |
| 13 | `P 15.0` / `P 15.1` | Pivot HIGH / LOW | — | Decides C21 or C11 |
| 14 | `M 79.1` **or** `M 59.1` | C21 / C11 filling = calls C10 | `M 9.3` / `M 58.2` on its pivot side | **Only one of the two** |
| 15 | `M 55.5` | C10 transferring | Called by C11/C21, `M8.4` = 0 | C10 belt fast (`A 48.0` + `A 48.1`) |
| 16 | `M 55.6`, `M 58.3` | C10 steps reset / all steps reset memory | Transfer done | — |
| 17 | `T 137` | C10 proven empty, 10 s (v0) | C10 belt fast, exit `B 10.6` clear | Any packet seen restarts it |
| 18 | `M 10.7` | **C10 proven empty** | `T 137` done | If not: C10 called again (`M 58.2`) |
| 19 | `M 10.6` | **C10 cleared** | `M 10.7` + C10 steps reset + C5/C6 OK | → clearing done |
| 20 | `M 8.4`, `M 8.5` | **C10 HOLD + clearing done** | With `M 10.6` | Stay ON until S3.2 |
| 21 | `MB 10` = 0 → `M 10.0` OFF | Clearing end | `M 10.6` (clearing abort path) | `K41.0` back ON: **feeding order B restarts**. F4 reset |

## B. New order (order B) until S3.2
| # | Address | Meaning | Turns ON when |
|---|---|---|---|
| 22 | `Q 49.5` (`H 49.5`) | S3.2 lamp | **Steady** while `M8.4` and not ready (v0.1) |
| 23 | `M 55.1`, `M 55.2` | C10 start / collating (first B packets) | B packets arrive on C10 |
| 24 | `M 7.4` | C10 filling with new order | `M 55.2` + `M 8.5` |
| 25 | `M 55.3`, `M 55.4` | C10 collating stop / **C10 full** | C10 full (`B 10.5` or count `M 54.4`) |
| 26 | `M 7.5` | C10 full with new order | `M 7.4` + `M 55.4` |
| 27 | `M 7.6` | C11…C23 ready | `M 7.5` + (C10 reset or all empty) |
| 28 | `M 7.7` | C11, C21 empty (idle) | `M 59.0` and `M 79.0`, not filling, not transferring |
| 29 | `M 8.0` | C12, C22 empty | Idle |
| 30 | `M 8.1` | C13, C23 empty | Idle |
| 31 | `M 8.2` | **Feeder empty → READY** | Loader done (`M 71.1`, not `M 71.2`/`M 71.4`) |
| 32 | `Q 49.5` | S3.2 lamp **BLINKING** | `M 8.2` |
| 33 | `I 3.2` (`S 3.2`) | Operator presses S3.2 | — |
| 34 | `M 8.3` | Operator enabled | `S 3.2` + `M 8.2` → resets `M 8.4`, `M 8.5`, `M 7.4`…`M 8.2`, C11/C12/C21/C22 registers |
| 35 | `M 59.1` or `M 79.1` → `M 55.5` | C10 transfers order B | Normal production again |

**Escape (v0.1):** `S 3.2` held 3 s (`T 140`) while `M 8.4` and not `M 10.0` → hold released even if the chain (#26–#31) is stuck.

## Paste list
```
M 150.4
M 5.2
M 10.0
T 128
M 10.1
M 26.7
M 10.2
"DB UTILITY".T33_DN
M 10.3
M 10.4
T 56
M 10.5
M 58.2
T 58
M 9.3
P 15.0
P 15.1
M 59.1
M 79.1
M 55.5
M 55.6
T 137
M 10.7
M 10.6
M 8.4
M 8.5
Q 49.5
M 55.2
M 7.4
M 55.4
M 7.5
M 7.6
M 7.7
M 8.0
M 8.1
M 8.2
I 3.2
M 8.3
T 140
K 41.0
```
