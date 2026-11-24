# PLC check - addresses written in more than one place (2026-11-24)

Source: `STEP7_BLOCKS_2026-11-23/` (generated from the offline project). Every `=`, `S`, `R`, `T` was listed; an address written by more than one block, or by `=` more than once, is a possible "leftover" (the last write in the scan wins).

## To fix
| Address | Where | Problem |
|---|---|---|
| `"HMI_DB".SCREEN_CALL_2` (NS12 `DB0012_DBX00131.02`) | FC212 line 383 (`MB3 <> 0`, drives C4...C9) and line 511 (`MB4 <> 0`, drives C10...C23) | Two `=`: the second wins. A drive fault C4...C9 alone (MB3) never calls screen 2. Fix: `O` both conditions into one `=` |
| `"DB UTILITY".Conveyor_13_Disable` / `Conveyor_23_Disable` | FC970 (`=`) and FC974 (`S` / `R`) | FC970 overwrites every scan what FC974 set (known, test plan S9). To decide which block owns them |

## Checked - OK (intended)
| Address | Why it is OK |
|---|---|
| `A63.1` / `A63.2` / `A63.3` (elevator drive speed / direction) | 4 `=` in FC916, but in separate jump branches (up fast / up slow / down fast / down slow): only one runs per scan |
| `M9.0` "Events update bit" | Scratch bit, written and used right away in each block (FC911, FC912, FC942, FC950, FC970, FC974) |
| `"PACKET WIDTH DB".Enc_Direct_Mem` | FC1210, two branches (direct / read job) |
| `"HMI_DB".CONV_10_COUNT` | FC1208 counts, FC955 clears at its reset - same as the other conveyors |
| `M10.0`, `M12.1`, `M58.2` | Clearing (FC911) and C10 re-call (FC955): set / reset on purpose |
| `M59.4`, `M63.4`, `M79.4`, `M83.4` | Step resets set by the conveyor block and by the clearing (FC911) |
| `"DB UTILITY".Pivot_Disable`, `Conveyor_10_Disable` | C11 / C21 set / reset (one level at a time) |
| `"HMI_DB".SERVICE_SW_x_STATUS`, `LOADER_..._SERVICE_SSW`, `M90.0`, `MW71` | Service resets (HMI CONTROL, SETUP, loader blocks) |
| `M47.4`, `M167.7`, `M92.5`, `M210.0` | Init (SETUP FC2 / OB100) + the block itself |
| `MW150` / `MW152` | LAUER keys (FC1 restore + FC190 toggles) |

No old block (FC1011...FC1086, FC924 / FC931 / FC954) is called any more (OB1 v0.3).
