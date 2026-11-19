# NEW FC9xx: fixed program blocks with an old/new switch in OB1

Every program block FC1011…FC1086 has a **new copy FC911…FC986** (number − 100). OB1 calls **either** the old or the new block, chosen by one bit per block:

`M28x.y = 0` → old FC10xx runs (as today) · `M28x.y = 1` → new FC9xx runs

Both use the same M bits, timers and DBs, so switching is bumpless. **Rollback = reset the bit in a VAT. No download.**

| Old | New | Switch | Changes in the new block |
|---|---|---|---|
| FC1011 CONVEYORS CLEARING | **FC911** | `M280.0` | **§14 fixes:** `T33_DN` (root cause), C10 proven empty 10 s (`T137`, `M10.7`), C10 re-call, S3.2 always, abort fix. **2026-11-19:** hold + new-order chain released at every clearing start (`FP M283.4`); S3.2 lamp steady while held / blinking when ready; S3.2 held 3 s releases the hold (`T140`) |
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
| FC1058 CONVEYOR 11 | **FC958** | `M281.5` | **2026-11-19:** clearing trigger `M9.3` only if pivot LOW (`P15.1`) |
| FC1062 CONVEYOR 12 | FC962 | `M281.6` | none (copy) |
| FC1066 CONVEYOR 13 | FC966 | `M281.7` | none (copy) |
| FC1070 LOADER FINGERS | FC970 | `M282.0` | none (copy) |
| FC1074 LOADER LIFT | FC974 | `M282.1` | none (copy) |
| FC1078 CONVEYOR 21 | **FC978** | `M282.2` | `R #INITIALISATION`. **2026-11-19:** clearing trigger `M9.3` only if pivot HIGH (`P15.0`) |
| FC1082 CONVEYOR 22 | FC982 | `M282.3` | none (copy) |
| FC1086 CONVEYOR 23 | **FC986** | `M282.4` | Fault reset by `M9.1` (all reset PBs) like C13; was `S2.7` only |

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
* **2026-11-19: downloaded to the PLC** (maintenance), all switches 0. Next: `M280.0` = 1 at an order change (clearing trial).
* 2026-11-18: compiled and tested in **S7-PLCSIM**: no errors and no CPU stop, with every switch bit on or off. Next: download between shifts (step 5), then the clearing trial (step 6).

## Maintenance test 2026-11-19 (lone packet, `M280.0` = 1)
* Clearing with C4 empty: **finished** (`M8.4`/`M8.5` set). Old bug (clearing stops by itself) did not occur.
* **Found:** F4 pressed again while C10 still held the previous new order (`M8.4`, S3.2 not pressed) → C10 may not transfer, the clearing can never finish. **Fix in FC911:** at every clearing start (rising `M10.0`) `M7.4`…`M8.5` are reset.
* **Found:** during clearing, `M9.3` (Timer 58 pulse + `M10.0`) started **C11 and C21 together**. C10 can only transfer to the side the pivot is on (step 11N6), so the other one always ran empty until its timeout. **Fix in FC958/FC978 (identical):** `M9.3` only with `P15.1` (C11) / `P15.0` (C21).
* To use: download FC911, FC958, FC978. FC958/FC978 need their switches `M281.5` / `M282.2` = 1.

## Commissioning status and plan (2026-11-19)
| Block | Switch | In PLC | Status |
|---|---|---|---|
| **FC911** clearing | `M280.0` | v0.0 | Lone-packet test OK (clearing finished with C4 empty). **v0.1** (hold release at F4, lamp steady/blink, S3.2 3 s) **to compile + download** |
| **FC958 / FC978** C11 / C21 | `M281.5` / `M282.2` | v0.0 | **v0.1** (clearing trigger on pivot side only) **to compile + download** |
| FC924 C3, FC938 C6 | `M280.5`, `M281.0` | v0.0 | Init fix only (service INIT). Low risk |
| FC986 C23 | `M282.4` | v0.0 | Fault reset `M9.1` like C13. Low risk |
| 15 other FC9xx | — | v0.0 | Identical copies of the running code. No reason to switch yet |

**Step 1 ✅ 2026-11-19:** FC911, FC958, FC978 **v0.1** downloaded.
**Step 2 — ACTIVE since 2026-11-19 (`M280.0`, `M281.5`, `M282.2` = 1, VAT "VAT_NewConveyors"). Production trial, 3–5 order changes:** `M280.0` = `M281.5` = `M282.2` = 1 before F4. Check each time:
- [ ] Clearing finishes by itself, C10 empty (`M10.7`), no packets left on C10
- [ ] During clearing only the conveyor on the pivot side starts (C11 if `P15.1`, C21 if `P15.0`)
- [ ] Order B stops on C10, S3.2 lamp **steady**, then **blinking** when ready
- [ ] Nothing leaves C10 before S3.2; short S3.2 when blinking releases it
- [ ] F4 pressed while C10 still holds: hold released, clearing runs
- [ ] (if the chain is stuck) S3.2 held 3 s releases the hold
- [ ] S3.2 lamp hardware OK (see the `Q49.5` LED on the output card while blinking)
**Step 3:** `M280.5`, `M281.0`, `M282.4` = 1 (C3, C6, C23).
**Step 4 (after weeks without problems):** make it permanent: OB1 calls FC9xx directly (no switch), `MB280`–`282` no longer needed; then delete FC1011–FC1086 (frees ~25–30 KB load memory).
⚠️ `MB280`–`282` are probably not retentive: after a power-off the old blocks run until the bits are set again.

### 2026-11-19: ALL 21 switches ON (`MB280`–`MB282` all 1)
The whole TS now runs FC911–FC986. Behaviour differs from the old blocks only in: FC911 v0.1 (clearing), FC958/FC978 v0.1 (clearing trigger on pivot side), FC924/FC938/FC978 (service INIT fix), FC986 (C23 fault reset `M9.1`). The 15 other blocks are identical copies. If a problem appears, reset the switch of the station concerned first (the old block runs again).

### 2026-11-19: first real order change with FC911 v0.1 — PASSED
F4 → clearing (C4 empty did not stop it, only the pivot-side conveyor started) → C10 proven empty (waited for C21 to call again: one run had stopped at 7.3 s) → `M8.4`/`M8.5` → order B fed → **S3.2 lamp solid** (held, not ready) → bottomer finished order A, C11…C23 + loader empty → **lamp blinking** → S3.2. Working as intended (operator).
Open: FC911 v0.3 (encoder-travel proof, ends the clearing sooner) — optional.
