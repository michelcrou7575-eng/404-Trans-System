# OMRON NS12 (Service HMI) - CX-Designer Exports

| File | What |
|---|---|
| `Caption_ORIGINAL_2026-11-20.csv` | Caption export as received (UTF-16) |
| `Caption_FIXED_v0.1.csv` | Same, 11 corrections - import back in CX-Designer (UTF-16, CRLF kept) |

## v0.1 (2026-11-20) corrections
| Screen | Part | Was | Now |
|---|---|---|---|
| 1 SERVICE 1 | PB0028 Conv 4 Test SW, OFF caption | CONV 3 | CONV 4 |
| 2 SERVICE 2 | PB0040 Pusher 2 Test SW, OFF caption | CONV 9 | PUSHER 2 |
| 2 | PLW0074 comment | CONVEYOR 73 STATUS | CONVEYOR 23 STATUS |
| 1 | PL0180 comment | M 46.6 - Pusher 1 | M 42.6 - Pusher 1 (caption is 42.6) |
| 2 | PB0164 comment | Flipper Service | TurnTable Service |
| 6 FLIPPER page | PB0013 comment | Packet to Feeder | Packet -> Flipper |
| 0 / 2 | PL0183, PL0030 caption | `8\n` | `8` |
| 2 | LBL0171 caption | `C12\n` | `C12` |

## Left as is - to confirm
- PB0106 / PB0163 OFF caption `CONV 2` (ON = CONV 2B / CONV 2R)
- PB0071 Loader Service OFF caption `FEEDER` (ON = LOADER)
- PB0076 Belt JOG `BELT` / `BELT ON`, PB0282 `Tst` / `OFF`, Screen 5/6 PB0013 `->` / `to` / `in`
- ConfirmDialog, StringTable and Alarm tables are empty (no alarm list on the NS12)
