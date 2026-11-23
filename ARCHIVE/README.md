# ARCHIVE - sources no longer used (moved 2026-11-23)

Kept for history only. **Do not compile these**: some have the same block names as running blocks.

## obsolete_blocks/ - blocks no longer in the CPU, or old variants
| Source | Why |
|---|---|
| `HMI PACKET COUNTER OLD` | FC1206, deleted from the CPU (replaced by FC1208) |
| `DE-BOUNCER LINK CONVEYOR FC6` | FC6, not in the CPU (replaced by FC8) |
| `DB6` | "DEBOUNCER OLD", not in the CPU |
| 16 × `... _ VFD OK -Check` | Old variants of FC1011...FC1086 with the **same block names**: compiling one would overwrite a block |

## superseded/ - older versions of running blocks
| Source | Replaced by |
|---|---|
| `OB1 (v0.2 DB111 switches)`, `OB0001 - CYCLIC (FC9xx switches).AWL` | OB1 v0.3 (no test switches, in the PLC 2026-11-23) - root `OB1` |
| `HMI PACKET COUNTER  NEW (FC1208 v0.8)` | FC1208 v0.12 (in the PLC 2026-11-23) - root `HMI PACKET COUNTER  NEW` |
| `ALL_NEW_FC9xx (...).AWL` | Full FC9xx install of 2026-11-18 (already in the PLC); single files in `NEW_FC9xx/` |

## Next week (about 2026-11-30), if nothing went wrong with OB1 v0.3
Move here too, and delete the blocks in the CPU + project, then compress:
* root `CONVEYORS CLEARING`, `CONVEYOR 0 ... 23`, `ELEVATOR + PUSHER 1`, `LOADER FINGERS`, `LOADER LIFT` -> FC1011...FC1086
* `NEW_FC9xx/FC0924`, `FC0931`, `FC0954` (non-PIW) -> FC924, FC931, FC954
* `NEW_FC9xx/` + `READY_TO_DOWNLOAD/DB0111 - FC9xx SWITCHES v0.2.AWL` -> DB111 "TESTING DB"
* `READY_TO_DOWNLOAD/OB0001 - CYCLIC v0.2`, `FC1208 ... v0.8` (rollback only)
