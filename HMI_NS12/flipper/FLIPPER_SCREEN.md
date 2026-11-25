# Flipper conveyor adjust screen - NS12 side (DB15 "PACKET POSITION DB", FC1215, was FC1221)

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

## v1.2 / v1.3 - C9 Pusher 2 (Loader -> Feeder screen), FC1215 "PACKET POSITIONING"
Same length class as the flipper (`DB0015_DBW00002`, lamps DBX16..19). Time 0 = `"HMI_DB".CONV_9_POS_mS` x 10 (the existing HMI value, as before).

| Object | NS12 address | Settings |
|---|---|---|
| C9 stop time [mS] (numeric) | `SERIALA:DB0015_DBW00102` | INT |
| C9 arrow -> (longer) | `SERIALA:DB0015_DBX00104.00` | Momentary (PLC resets: one press = +10 mS) |
| C9 arrow <- (shorter) | `SERIALA:DB0015_DBX00104.01` | Momentary (-10 mS) |
| C9 DEFAULT button (optional) | `SERIALA:DB0015_DBX00104.02` | Momentary: this class back to CONV_9_POS_mS x 10 |
| Packet length (numeric / drawing) | `SERIALA:DB0015_DBW00086` | as on the flipper screen |

Reserved for the moving drawing (later): `DB0015_DBW00098` tail, `DB0015_DBW00100` front.

## v1.3 / v1.4 - C9 drawing: ONE packet moved laterally (16 positions)
16 copies of the same packet drawing (Bit Lamp, rectangle), same size, each one step to the right. **Control Flag -> Display** of copy n = its bit below (only one ON). Lamp address of all copies: `SERIALA:M00000.00` (M0.0 always ON) -> always khaki.
Position = C9 stop time used: copy = (time - C9_View_Min_ms) / C9_View_Step_ms (defaults 0 / 60 mS -> 0...900 mS).

| Copy | Address | Copy | Address |
|---|---|---|---|
| 0 (left) | `DB0015_DBX00173.00` | 8 | `DB0015_DBX00172.00` |
| 1 | `DB0015_DBX00173.01` | 9 | `DB0015_DBX00172.01` |
| 2 | `DB0015_DBX00173.02` | 10 | `DB0015_DBX00172.02` |
| 3 | `DB0015_DBX00173.03` | 11 | `DB0015_DBX00172.03` |
| 4 | `DB0015_DBX00173.04` | 12 | `DB0015_DBX00172.04` |
| 5 | `DB0015_DBX00173.05` | 13 | `DB0015_DBX00172.05` |
| 6 | `DB0015_DBX00173.06` | 14 | `DB0015_DBX00172.06` |
| 7 | `DB0015_DBX00173.07` | 15 (right) | `DB0015_DBX00172.07` |

Settable: `DBW174` C9_View_Min_ms, `DBW176` C9_View_Step_ms. Display: `DBW178` copy shown.

## DB15 v1.6 / FC1215 v1.7 - C9 limits
C9 time used `DB0015_DBW00102` [mS], 1...500 mS (`DBW182` C9_Max_ms). DEFAULT / size without time = `DBW180` C9_Default_ms = 250 mS (center). Drawing: copy = time / 32 mS (`DBW176`) -> 250 mS = copy 7, 500 mS = copy 15.
