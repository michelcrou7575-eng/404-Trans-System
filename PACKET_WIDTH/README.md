# Packet width measure (C10 transfer, B10.5 + B10.6) — MEASUREMENT ONLY v0.3

Operator idea (2026-11-18): measure the packet width with **two independent sensors** at the end of C10 while it transfers, compare them to get a **verified** width, then use it later for **sensor blanking** on the C11/C12/C13 and C21/C22/C23 counters (same speed).

Facts from the operator: C13/C23 **load** at the same speed (31 m/min), only their **delivery** is slower. `B10.5`/`B10.6` are mounted a little lower than the C23 sensor. Packets are **separated by about half a packet** during the transfer. The C10 count is correct. The C10 encoder counts during the transfer (not used today). C10 fast = C11/C12 = C21/C22 speed (31 m/min), C13/C23 slower (23.7 m/min).

## How it measures
* Window: C10 transferring (`M55.5 AN M55.6`). Encoder `"FM350 DB".ACT_CNTV5`, **0.31 mm/pulse**: independent of speed and stops.
* For each sensor: front of a packet = sensor ON, end = sensor OFF **for longer than `Gap_Min_mm`** (default **150 mm**). A shorter OFF is a **sag** (U-shape / low packet) inside the same packet; it is counted and its length kept (`Sag_Count`, `Sag_Max_mm`).
* **v0.2: the width is also measured in mS** (time from packet front to packet end, sags included), because C11…C23 have no encoder. C10 fast runs at the C11/C12/C21/C22 speed, so this is the time their sensors will see. `Speed_mm_s` (= mm × 1000 / mS) checks it: 31 m/min = 517 mm/s.
* A packet already covering the sensor when the transfer starts is partial → not measured (`Skipped`).
* End of transfer: **verified** only if both sensors measured packets, saw the same number (= C10 count), and their average widths agree within `Tolerance_Pct` (10%). Then `Width_mm` (encoder), `Width_ms_31` (**measured** mS, average of both sensors) and `Speed_mm_s` are written, `Valid` = 1, `Good_Count` +1. Otherwise `Bad_Count` +1 and the last verified width is kept.
* **Writes only DB30.** Nothing else on the machine changes.

## Blocks (all free in the project)
| Block | Symbol | |
|---|---|---|
| UDT10 | `Width Sensor Struct` | Data for one sensor |
| DB30 | `PACKET WIDTH DB` | Settings + results |
| FC1211 | `WIDTH SENSOR` | Measures one sensor |
| FC1210 | `PACKET WIDTH MEASURE` | Calls FC1211 for B10.5 and B10.6, verifies |
| OB1 | — | `CALL FC 1210` after the C10 block (already in the FC9xx OB1) |

## Steps
1. Symbol table → Import `PACKET_WIDTH_SYMBOLS.asc` (**needed**: the source uses `"PACKET WIDTH DB"`).
2. Compile `PACKET_WIDTH_MEASURE.AWL` (UDT10, DB30, FC1211, FC1210 in one source), then the OB1 source.
3. PLCSIM: compiles, no CPU stop.
4. Between shifts: download UDT10, DB30, FC1211, FC1210, then OB1 (together with the FC9xx download, or alone).

## VAT "PACKET WIDTH"
| Address | Meaning |
|---|---|
| `"PACKET WIDTH DB".Width_mm` | **Verified width [mm]**: compare with a tape measure |
| `.Valid`, `.Last_OK`, `.Good_Count`, `.Bad_Count` | Verification result |
| `.S5.Count`, `.S6.Count`, `.C10_Count_Start` | Packets seen by B10.5 / B10.6 / C10 count |
| `.S5.Width_Avg_mm`, `.S6.Width_Avg_mm`, `.S5.Width_Min_mm`, `.S5.Width_Max_mm` | Width per sensor |
| `.S5.Sag_Count`, `.S5.Sag_Max_mm`, `.S6.Sag_Count`, `.S6.Sag_Max_mm` | **Sags** (U-shape) seen inside packets |
| `.S5.Gap_Min_mm`, `.S6.Gap_Min_mm` | Shortest real gap between packets |
| `.Gap_Min_mm` (setting) | Raise it if `Sag_Max_mm` comes close to it. It must stay below `S5/S6.Gap_Min_mm` |
| `.Width_ms_31` | **Measured width [mS]** at 31 m/min: C11/C12/C21/C22 **and C13/C23 loading** (for the blanking) |
| `.Speed_mm_s` | Check: C10 fast speed measured. 517 mm/s = 31 m/min. If far off, C10 stopped during the transfer or the speeds differ |
| `.S5.Width_Avg_ms`, `.S6.Width_Avg_ms`, `.S5.Last_Width_ms` | Width in mS per sensor |

**Goal of this step:** a few orders, normal and U-shape, with `Width_mm` within a few % of the tape measure, `Last_OK` = 1, and `Sag_Max_mm` well below the real gaps. Only then: step 2 = blanking on C11…C23 (same change on low and high level).

## Desk check (no PLCSIM available, 2026-11-18)
The FC1211 logic was replayed step by step in a model (10 ms scan, 517 mm/s, 600 mm packets, 300 mm gaps):

| Case | Result |
|---|---|
| 6 flat packets | 6 measured, 600 mm, 1171 ms (exact: 1161 ms, +1 scan) |
| 6 U-shape, sag 120 mm, `Gap_Min` 150 | 6 measured, 600 mm, 6 sags seen, `Sag_Max` 119 |
| Gaps 250–350, sag 100 | 6 measured, 600 mm, `Gap_Min` seen 248 |
| First packet already covering the sensor | 5 measured + 1 skipped (counted as seen) |
| **Sag 200 mm, `Gap_Min` 150 (too small)** | **12 "packets" of 200 mm**: transfer rejected (`Last_OK` = 0), and `S5/S6.Gap_Min_mm` shows ≈ the sag length → **raise `Gap_Min_mm`** above it, below the real gap |

**Runtime safety without PLCSIM:** FC1210/1211 write only DB30. No division by zero (divisions only after a packet is counted, or by constants). OB121/OB122 exist, so a programming/access error would not stop the CPU. Download order: UDT10 → DB30 → FC1211 → FC1210 (nothing calls them yet) → **then** the `CALL FC 1210` in OB1. Check the CPU diagnostic buffer and cycle time after. Rollback = remove the call from OB1.
