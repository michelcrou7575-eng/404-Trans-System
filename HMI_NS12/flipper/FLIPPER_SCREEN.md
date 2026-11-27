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
C9 time used `DB0015_DBW00102` [mS], 1...500 mS (`DBW182` C9_Max_ms). DEFAULT / size without time = `DBW180` C9_Default_ms (v1.7: 90 mS). Max `DBW182` C9_Max_ms (v1.7: 200 mS). Drawing: copy = time / C9_View_Step_ms (`DBW176`, v1.7: 13 mS) -> 90 mS = copy 6, 200 mS = copy 15.

## Fork geometry (from maintenance, 2026-11-26)
7 long fingers, **210 mm** between fingers (6 x 210 = 1260 mm first -> last finger) + 1 short finger.
Best stop ("no loose ends"): packet centred on the finger group it can cover.

| Packet length | Spaces x 210 | Fingers under the packet | Overhang each end |
|---|---|---|---|
| 510-629 mm | 2 (420 mm) | 3 | 45-105 mm |
| 630-839 mm | 3 (630 mm) | 4 | 0-105 mm |
| 840-975 mm | 4 (840 mm) | 5 | 0-68 mm |

Drawing scale: Level Meter Max [mm] = meter width [px] x 210 / finger spacing [px].
Still needed for the time calculation: two stop measurements (time -> packet tail distance from the first long finger).

## DB15 v1.7 (2026-11-26): field names
Flipper fields renamed `C7_...` (C7_Time_Used_ms, C7_Plus_PB, C7_Stop_S5T, C7_Time_ms, C7_Disp_Length_mm, C7_Width_Class_1...4 ...). C9 fields `C9_...`. Shared: Length_mm, Class, Class_Lamps, Step_ms. **All NS12 addresses unchanged.**

## DB15 v1.8 / FC1215 v1.9 - C7 flipper drawing: ONE packet moved (16 positions), like C9
16 copies of the packet (Bit Lamp, lamp address `SERIALA:M00000.00`, Control Flag -> Display = bit below). Copy = (C7 time shown - 700) / 100 mS (`DBW186` / `DBW188`, settable). 1500 mS (default) = copy 8.

| Copy | Time from | Control Flag |
|---|---|---|
| 0 | 700 mS | `DB0015_DBX00185.00` |
| 1 | 800 mS | `DB0015_DBX00185.01` |
| 2 | 900 mS | `DB0015_DBX00185.02` |
| 3 | 1000 mS | `DB0015_DBX00185.03` |
| 4 | 1100 mS | `DB0015_DBX00185.04` |
| 5 | 1200 mS | `DB0015_DBX00185.05` |
| 6 | 1300 mS | `DB0015_DBX00185.06` |
| 7 | 1400 mS | `DB0015_DBX00185.07` |
| 8 | 1500 mS | `DB0015_DBX00184.00` |
| 9 | 1600 mS | `DB0015_DBX00184.01` |
| 10 | 1700 mS | `DB0015_DBX00184.02` |
| 11 | 1800 mS | `DB0015_DBX00184.03` |
| 12 | 1900 mS | `DB0015_DBX00184.04` |
| 13 | 2000 mS | `DB0015_DBX00184.05` |
| 14 | 2100 mS | `DB0015_DBX00184.06` |
| 15 | 2200 mS | `DB0015_DBX00184.07` |

Display: `DBW190` copy shown. Remove leftover macros (screen / object / project).

## FC1215 v2.0 - arrows auto repeat (C7 and C9)
Press = 1 step (10 mS). Hold 0.5 s = 1 step every 100 mS (100 mS per second). (v2.1: no fast step.) Release = stop.
**The arrow buttons MUST be Momentary** (the PLC no longer resets them; Alternate would keep counting).

## DB15 v2.0 / FC1215 v2.2 - C7 drawing with 2 Level Meters (packet moves, keeps its length)
| Level Meter | Address | Direction | Range |
|---|---|---|---|
| Left half (from the fork centre to the left) | `SERIALA:DB0015_DBW00192` (C7_Left_mm) | **Left** | Min 0, Max = C7_Half_mm (665) |
| Right half (from the fork centre to the right) | `SERIALA:DB0015_DBW00194` (C7_Right_mm) | **Right** | Min 0, Max 665 |

Left = L/2 + offset, Right = L/2 - offset, offset = (C7 time - C7_Center_ms 1500) x C7_Speed_mm_s (400) / 1000. More time = packet further LEFT (downstream). 673 mm: 1500 mS = 336 / 336 (centred), 1800 mS = 456 / 216, 1200 mS = 216 / 456.
Settable online: `DBW196` C7_Center_ms, `DBW198` C7_Speed_mm_s (set the measured C7 speed), `DBW200` C7_Half_mm (= meter Max).

### Level Meter layout (2026-11-26, from the test photos)
Test result: Left 615 = short block, Right 615 hidden by the Left meter, both 1200 = full fork.
So the meters were set **Min ~600** and **overlapping**. The PLC sends **half lengths 0..665 mm** (a 724 mm packet = about 362 / 362), so with Min 600 almost nothing shows.

Scale: fingers 210 mm apart = about **70 px** on the screen → **3 mm per px**. 665 mm = **222 px**.

| | Left meter (`DBW192`) | Right meter (`DBW194`) |
|---|---|---|
| Direction | **Left** (grows from its right edge) | **Right** (grows from its left edge) |
| Range | Min **0**, Max **665**, INT | Min **0**, Max **665**, INT |
| Width | **222 px** | **222 px** |
| X | right edge = centre of **finger 4** (X_f4 - 222) | left edge = centre of **finger 4** (X = X_f4) |
| Y / Height | same as the other meter | same |
| Frame / background | none / transparent (or fork grey) | same |

The two meters must **touch at finger 4 and never overlap**. Values to test on the VAT: 362 / 362 (724 mm centred), 500 / 224 (moved left), 224 / 500 (moved right).

Checked 2026-11-27 on the user's drawing: the 7 long fingers span 1260 mm = 420 px, 70 px apart, so **3 mm per px exactly**. Finger "0" (far left) is ignored. The meters join at the **centre of finger 4**. The fingers must be in **front** of the meters (Bring to Front), so the packet shows behind them.
Screen 800 x 600. **Finger 4 centre = X 426** (centre line 0051). So: **L1-L4 X = 204**, **R1-R4 X = 426**, width 222 each (L spans 204-426, R spans 426-648).
