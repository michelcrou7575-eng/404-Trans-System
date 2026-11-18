# Packet width measure (C10 transfer, B10.5 + B10.6) — MEASUREMENT ONLY v0.1

Operator idea (2026-11-18): measure the packet width with **two independent sensors** at the end of C10 while it transfers, compare them to get a **verified** width, then use it later for **sensor blanking** on the C11/C12/C13 and C21/C22/C23 counters (same speed).

Facts from the operator: `B10.5`/`B10.6` are mounted a little lower than the C23 sensor. Packets are **separated by about half a packet** during the transfer. The C10 count is correct. The C10 encoder counts during the transfer (not used today). C10 fast = C11/C12 = C21/C22 speed (31 m/min), C13/C23 slower (23.7 m/min).

## How it measures
* Window: C10 transferring (`M55.5 AN M55.6`). Encoder `"FM350 DB".ACT_CNTV5`, **0.31 mm/pulse**: independent of speed and stops.
* For each sensor: front of a packet = sensor ON, end = sensor OFF **for longer than `Gap_Min_mm`** (default 100 mm). A shorter OFF is a **sag** (U-shape / low packet) inside the same packet; it is counted and its length kept (`Sag_Count`, `Sag_Max_mm`).
* A packet already covering the sensor when the transfer starts is partial → not measured (`Skipped`).
* End of transfer: **verified** only if both sensors measured packets, saw the same number (= C10 count), and their average widths agree within `Tolerance_Pct` (10%). Then `Width_mm`, `Width_ms_31`, `Width_ms_237` are written, `Valid` = 1, `Good_Count` +1. Otherwise `Bad_Count` +1 and the last verified width is kept.
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
| `.Width_ms_31`, `.Width_ms_237` | Width in mS for the link / delivery conveyors (for the later blanking) |

**Goal of this step:** a few orders, normal and U-shape, with `Width_mm` within a few % of the tape measure, `Last_OK` = 1, and `Sag_Max_mm` well below the real gaps. Only then: step 2 = blanking on C11…C23 (same change on low and high level).
