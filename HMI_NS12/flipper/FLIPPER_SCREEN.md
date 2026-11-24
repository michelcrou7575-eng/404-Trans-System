# Flipper conveyor adjust screen - NS12 side (DB15 "FLIPPER POS DB", FC1215, was FC1221)

Stop time = C7 belt run after the packet tail leaves B7.4 (was a fixed 1.5 s). One time per packet length class (15 mm).

## Objects

| Object | NS12 address | Settings |
|---|---|---|
| Packet length [mm] (numeric display) | `SERIALA:DB0015_DBW00000` | INT, no decimals |
| **Stop time [mS]** (numeric display, big) | `SERIALA:DB0015_DBW00004` | INT |
| **Packet size bar** (Bar Graph, horizontal) | `SERIALA:DB0015_DBW00000` | Min 400, Max 1000 → the bar grows with the packet length, drawn over the fork |
| Arrow → (longer, packet stops further) | `SERIALA:DB0015_DBX00014.00` | **Momentary** button (the PLC resets it: one press = +10 mS) |
| Arrow ← (shorter, packet stops earlier) | `SERIALA:DB0015_DBX00014.01` | **Momentary** (−10 mS) |
| "DEFAULT" button (optional) | `SERIALA:DB0015_DBX00014.02` | Momentary: this class back to 1500 mS |
| Class lamps 510-525 … >975 | below | Bit lamps, one per class |

## Class lamps

| Class | Length [mm] | Address |
|---|---|---|
| 0 | <525 | `SERIALA:DB0015_DBX00019.00` |
| 1 | 525-540 | `SERIALA:DB0015_DBX00019.01` |
| 2 | 540-555 | `SERIALA:DB0015_DBX00019.02` |
| 3 | 555-570 | `SERIALA:DB0015_DBX00019.03` |
| 4 | 570-585 | `SERIALA:DB0015_DBX00019.04` |
| 5 | 585-600 | `SERIALA:DB0015_DBX00019.05` |
| 6 | 600-615 | `SERIALA:DB0015_DBX00019.06` |
| 7 | 615-630 | `SERIALA:DB0015_DBX00019.07` |
| 8 | 630-645 | `SERIALA:DB0015_DBX00018.00` |
| 9 | 645-660 | `SERIALA:DB0015_DBX00018.01` |
| 10 | 660-675 | `SERIALA:DB0015_DBX00018.02` |
| 11 | 675-690 | `SERIALA:DB0015_DBX00018.03` |
| 12 | 690-705 | `SERIALA:DB0015_DBX00018.04` |
| 13 | 705-720 | `SERIALA:DB0015_DBX00018.05` |
| 14 | 720-735 | `SERIALA:DB0015_DBX00018.06` |
| 15 | 735-750 | `SERIALA:DB0015_DBX00018.07` |
| 16 | 750-765 | `SERIALA:DB0015_DBX00017.00` |
| 17 | 765-780 | `SERIALA:DB0015_DBX00017.01` |
| 18 | 780-795 | `SERIALA:DB0015_DBX00017.02` |
| 19 | 795-810 | `SERIALA:DB0015_DBX00017.03` |
| 20 | 810-825 | `SERIALA:DB0015_DBX00017.04` |
| 21 | 825-840 | `SERIALA:DB0015_DBX00017.05` |
| 22 | 840-855 | `SERIALA:DB0015_DBX00017.06` |
| 23 | 855-870 | `SERIALA:DB0015_DBX00017.07` |
| 24 | 870-885 | `SERIALA:DB0015_DBX00016.00` |
| 25 | 885-900 | `SERIALA:DB0015_DBX00016.01` |
| 26 | 900-915 | `SERIALA:DB0015_DBX00016.02` |
| 27 | 915-930 | `SERIALA:DB0015_DBX00016.03` |
| 28 | 930-945 | `SERIALA:DB0015_DBX00016.04` |
| 29 | 945-960 | `SERIALA:DB0015_DBX00016.05` |
| 30 | 960-975 | `SERIALA:DB0015_DBX00016.06` |
| 31 | >975 | `SERIALA:DB0015_DBX00016.07` |

`NS12_Symbols_DB15_Flipper.txt`: all these addresses as NS12 symbols (Symbol Table → Import).

## v1.1 - packet drawing (centered, 4 width pairs)
| Object | Address | Settings |
|---|---|---|
| Left half meter (Display Direction **Left**), right half meter (Direction **Right**), side by side from the fork center | `SERIALA:DB0015_DBW00086` (both) | INT, **Min 0, Max = fork length in mm** (the whole fork width), so the drawn length is in proportion |
| Width pair 1 / 2 / 3 / 4 (Control Flag → Display) | `DB0015_DBX00090.00` / `.01` / `.02` / `.03` | < 450 / 450-500 / 500-550 / >= 550 mm (limits in DB15 DBW92 / 94 / 96) |
| Packet width (numeric, optional) | `SERIALA:DB0015_DBW00088` | INT [mm] |
