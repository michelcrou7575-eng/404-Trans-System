# Online download procedure - 2026-11-27 (production running, LAUER in charge)

All blocks below are **new, not in the PLC yet**. Each step is **one small download in RUN** (SIMATIC Manager, block by block).
Every change is either **the same behaviour as today** (4e with Tst OFF, 4f) or **acts only when a switch is ON** (4g, 4h, 4i).
So a step can be done during production, but **check the "before" bits first**: a bit that is already ON acts at once.

## 0. Before anything (once)
1. **Backup**: File > Archive the project, and PLC > Upload Station to a **copy** of the project (keep the online state).
2. Copy the AWL files into the project **Sources** folder (Insert > External Source).
3. **Compile only** (no download yet), in this order. Each must compile with **0 errors**:

| # | Source | Creates |
|---|---|---|
| 1 | `DB0001 - DB UTILITY v0.4 (C4 encoder PPR + gate).AWL` | DB1 offline (new names, **same addresses**) |
| 2 | `FC0932 - NEW C4 PIW v0.4 (encoder PPR + gate).AWL` | FC932 |
| 3 | `FC0002 - SETUP v0.2 (C4 encoder PPR).AWL` | FC2 |
| 4 | `FC0948 - NEW C8 - TURNTABLE v0.1 (encoder PPR).AWL` | FC948 |
| 5 | `FC1208 - HMI PACKET COUNTER NEW v1.1 (encoder PPR).AWL` | FC1208 |
| 6 | `FC0922 - NEW C2 - ANGLE B+R v0.1 (C2 disable).AWL` | FC922 |
| 7 | `FC0955 - NEW C10 PIW v0.2 (C10 + pivot disable).AWL` | FC955 |
| 8 | `FC0962 - NEW C12 - LINK 2 LO v0.1 (C12 disable).AWL` | FC962 |
| 9 | `FC0982 - NEW C22 - LINK 2 HI v0.1 (C22 disable).AWL` | FC982 |
| 10 | `FC0970 - NEW LOADER FINGERS v0.1 (fingers disable).AWL` | FC970 |
| 11 | `FC0974 - NEW LOADER LIFT v0.1 (lift disable).AWL` | FC974 |
| 12 | `DB0015 v2.0 + FC1215 v2.2 - PACKET POSITIONING.AWL` | DB15 + FC1215 |
| 13 | `FC1100 - HMI CONTROL v0.4 (bumpless).AWL` (only after renaming DB12 1.5 to `TST_SWITCH_STATUS`) | FC1100 |

4. Open one **VAT** with the addresses of the "before / after" checks below.

> **DB1 is NOT downloaded** (the FCs fill its new words themselves). A DB1 download would reset all its actual values,
> including the NS12 conveyor disable bits. Online / offline compare will show DB1 different: that is expected.

## Step 1 - Set 4e: DB15 v2.0 + FC1215 v2.2 (NS12 C7 drawing with 2 Level Meters)
- **Before:** `M140.3` = **0** (LAUER in charge, Tst OFF).
- **Download DB15 first, then FC1215** (FC1215 v2.2 writes DBW192…200, which only exist in DB15 v2.0).
- DB15 values go back to their initial values (tables empty = defaults): no effect on the machine while M140.3 = 0.
- **After:** `DB15.DBW196` = 1500, `DBW198` = 400, `DBW200` = 665; `DBW192` / `DBW194` follow the C7 time on the NS12.

## Step 2 - Set 4f: C4 encoder PPR (same behaviour at 100 P/R)
- **Before:** nothing special. Best between two C4 cycles (C4 stopped).
- **Download FC932 first** (it writes the defaults into DB1), then FC1208, FC948, FC2.
- **After (VAT):**

| Address | Expected |
|---|---|
| `DB1.DBW0` C4_Encoder_PPR | **100** |
| `DB1.DBW18` C4_Wheel_Circ_01mm | **6350** |
| `DB1.DBW8` C4_Stop_Delay_ms | **1500** |
| `DB1.DBD62` T91_ET (gate OFF time) | **~3500 or more** while C4 is collating |
| `"HOUSE_KEEPING DB".C4_Packet_Length_mm`, `MW202` | same values as before for the same packets |

- FC2 only runs at setup (S2.2): Surface_Length_C4 stays 800 anyway.

## Step 3 - Set 4g: C2 / C10 / pivot service interlocks
- **Before:** `DB1.DBX20.4` (Conveyor_2_Disable), `DBX21.5` (Conveyor_10_Disable), `DBX21.6` (Pivot_Disable) = **0**.
  No C3 / C11 / C21 service test running.
- Download FC922, FC955.
- **After:** nothing changes in production. Check later with a C3 service test (C2 belt + rollers stop) and a C11 / C21 test (C10 belt + pivot stop).

## Step 4 - Set 4h: C12 + C22 disable (identical, download both together)
- **Before:** `DB1.DBX22.0` (Conveyor_12_Disable) and `DBX22.3` (Conveyor_22_Disable) = **0** - these NS12 switches did nothing until now, one may be left ON!
- Download FC962 and FC982, one right after the other.
- **After:** C12 / C22 keep running. Test later: NS12 disable ON = belt stops, OFF = it continues.

## Step 5 - Set 4i: feeder fingers + lift disable
- **Before:** `DB1.DBX22.5` (Feeder_Lift_disable) and `DBX22.6` (Feeder_Fingers_disable) = **0** (same reason as step 4).
- Download FC970, FC974.
- **After:** feeder runs as before. Test later with the NS12 disable switches (lift / fingers stop where they are).

## Step 6 (optional, when ready to try the NS12 takeover) - Set 4d: FC1100 v0.4
- Needs: DB12 1.5 renamed `TST_SWITCH_STATUS` (names only, **no DB12 download**), NS12 "Tst" button **Momentary** on `DB12.DBX1.4`, lamp on `DBX1.5`.
- **Before:** `DB12.DBX1.5` = **0**, so `M140.3` stays 0 and the LAUER stays in charge.
- **After:** hold "Tst" 2 s = NS12 takes over with the LAUER values (bumpless); LAUER F2 gives control back.

## Rollback (any step)
Download the previous block from the backup copy (step 0.1). The versions in the PLC before this procedure:
FC2 v0.1, FC922 v0.0, FC932 v0.1, FC948 v0.0, FC955 v0.1, FC962 v0.0, FC970 v0.0, FC974 v0.0, FC982 v0.0, FC1208 v1.0,
DB15 v1.9 + FC1215 v2.1, FC1100 (current). DB1 was not changed online.

When a step is done, tell me: I mark the row "in the PLC" in README.md.
