# STEP 7 blocks - generated from the offline project (uploaded 2026-11-25)

`ALL_BLOCKS_2026-11-25.AWL` = the upload (Generate Source, all blocks). Split into one file per block (83 blocks). Compared with `STEP7_BLOCKS_2026-11-23` and `READY_TO_DOWNLOAD`:

| Block | Result |
|---|---|
| OB1 v1.0 | = READY v1.0 (+ `CALL "ALARM MANAGER"` = FC1220, symbol renamed by user) ✅ |
| FC1208 v1.0 | = READY v1.0 (only symbol names `"M 283.x"`, `"Timer 138/139"` added) ✅ |
| DB13 / FC1220 v1.1 (new) | = READY v1.1 ✅ - FC1220 symbol = "ALARM MANAGER" |
| DB15 v1.4 / FC1215 v1.5 (new) | = READY ✅ - all tables empty (defaults) |
| FC942 v1.2 / FC950 v1.1 | = READY ✅ |
| **DB12 HMI_DB** (user) | renamed: `ON_SW` -> `TRANS_SYSTEM_ON_SW` (DBX0.2), `AERIAL_LINK_RUN_PB` -> `TRANS_SYSTEM_RUN_STATUS` (DBX0.4). Same addresses. Version still 0.1 |
| FC1100 HMI CONTROL, OB100 (user) | follow the DB12 renames only |
| **FC2 SETUP (user)** | `R "HMI_DB".ON_SW` **removed**: START no longer resets the NS12-in-control switch (M140.3 path, see NEW_HMI_TEST_PLAN H1). Version still 0.1 |
| All other blocks | unchanged since 2026-11-23 |
