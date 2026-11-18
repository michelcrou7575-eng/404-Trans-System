# NEW FC9xx: fixed program blocks with an old/new switch in OB1

Every program block FC1011…FC1086 has a **new copy FC911…FC986** (number − 100). OB1 calls **either** the old or the new block, chosen by one bit per block:

`M28x.y = 0` → old FC10xx runs (as today) · `M28x.y = 1` → new FC9xx runs

Both use the same M bits, timers and DBs, so switching is bumpless. **Rollback = reset the bit in a VAT. No download.**

| Old | New | Switch | Changes in the new block |
|---|---|---|---|
| FC1011 CONVEYORS CLEARING | **FC911** | `M280.0` | **§14 fixes:** `T33_DN` (root cause), C10 proven empty 10 s (`T137`, `M10.7`), C10 re-call, S3.2 always, abort fix |
| FC1012 CONVEYOR 0 + PUSHER 0 | FC912 | `M280.1` | none (copy) |
| FC1016 ELEVATOR + PUSHER 1 | FC916 | `M280.2` | none (copy) |
| FC1018 CONVEYOR 1 | FC918 | `M280.3` | none (copy) |
| FC1022 CONVEYOR 2 | FC922 | `M280.4` | none (copy) |
| FC1024 CONVEYOR 3 | **FC924** | `M280.5` | `R #INITIALISATION` |
| FC1031 CONVEYOR 4 | FC931 | `M280.6` | none (copy) |
| FC1034 CONVEYOR 5 | FC934 | `M280.7` | none (copy) |
| FC1038 CONVEYOR 6 | **FC938** | `M281.0` | `CLR / = #INITIALISATION` |
| FC1042 CONVEYOR 7 | FC942 | `M281.1` | none (copy) |
| FC1048 CONVEYOR 8 | FC948 | `M281.2` | none (copy) |
| FC1050 CONVEYOR 9 | FC950 | `M281.3` | none (copy) |
| FC1054 CONVEYOR 10 | FC954 | `M281.4` | none (copy) |
| FC1058 CONVEYOR 11 | FC958 | `M281.5` | none (copy) |
| FC1062 CONVEYOR 12 | FC962 | `M281.6` | none (copy) |
| FC1066 CONVEYOR 13 | FC966 | `M281.7` | none (copy) |
| FC1070 LOADER FINGERS | FC970 | `M282.0` | none (copy) |
| FC1074 LOADER LIFT | FC974 | `M282.1` | none (copy) |
| FC1078 CONVEYOR 21 | **FC978** | `M282.2` | `R #INITIALISATION` |
| FC1082 CONVEYOR 22 | FC982 | `M282.3` | none (copy) |
| FC1086 CONVEYOR 23 | FC986 | `M282.4` | none (copy) |

The "copy" blocks are the running code, unchanged. They are the base for the redesign, and future fixes go into them, never into the running FC10xx.

`MB280–MB282` and `FC900–FC999` are free in the project (checked against the full export and the symbol table).

## Files
* `ALL_NEW_FC9xx.AWL`: all 21 blocks in one source (compile once).
* `FC09xx - ….AWL`: the same, one file per block.
* `OB0001 - CYCLIC (FC9xx switches).AWL`: OB1 with the 21 switches (same as the repo `OB1`). Otherwise identical to the running OB1. The `>D` → `<>D` fault-monitor fix is **not** in it, so that this download changes nothing.
* `NEW_FC9xx_SYMBOLS.asc`: symbols for FC911…FC986 and the switch bits `SW NEW FC9xx`.

## Steps
**Office (no PLC):**
1. Symbol table → *Symbol Table → Import* → `NEW_FC9xx_SYMBOLS.asc` (42 symbols). Optional: the sources use absolute `FC 9xx` and `M 28x.y`, so they compile without it.
2. Sources → *Insert → External Source* → `ALL_NEW_FC9xx.AWL` → *Compile*. Then the same for the OB1 source.
3. Check: 21 new blocks FC911…FC986, no errors.

**Between shifts (≈ 10 min):**
4. Make sure `MB280`, `MB281`, `MB282` = 0 in a VAT (they should be).
5. Download **FC911…FC986** (not called yet → no effect), then **OB1**. With all bits at 0, the machine runs exactly as before.

**Trials (one bit at a time):**
6. `M280.0` = 1 → **new clearing** at the next order change (F4). Check: C10 empties, S3.2 lamp, operator confirms, no "clearing off by itself" when C4 is empty.
7. `M280.5`, `M281.0`, `M282.2` (C3, C6, C21 init fixes): only change behaviour in service / INIT.
8. Problem → bit back to 0.

⚠️ `MB280–282` are probably **not retentive**: after a power-off the old blocks run again. When a new block is accepted, make it permanent (in OB1, call FC9xx without the switch, or make the bit retentive in the CPU properties).

## Status
* 2026-11-18: compiled and tested in **S7-PLCSIM**: no errors and no CPU stop, with every switch bit on or off. Next: download between shifts (step 5), then the clearing trial (step 6).
