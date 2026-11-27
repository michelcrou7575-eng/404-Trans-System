# C4 encoder: 100 P/R -> 1000 P/R (E6C2-CWZ6C) - impact list (2026-11-27)

Wheel 202 mm (634.6 mm per turn). Now E6B2-CWZ6C 100 P/R = **6.35 mm/pulse**. New E6C2-CWZ6C 1000 P/R = **0.635 mm/pulse** (x10).
Both are NPN open collector, 5-24 VDC, same colours (Brown +, Blue 0V, Black A, White B, Orange Z) -> same wiring.
Mechanical: E6C2 = body 50 mm, shaft 8 mm (E6B2 = 40 mm / 6 mm) -> new bracket / wheel bore or coupling.
Frequency at 31 m/min (0.52 m/s): 814 Hz -> FM350-2 OK (10 kHz).

## Everything that counts C4 pulses (from STEP7_BLOCKS_2026-11-25) - all x10 or /10

| Block | Line | Now | With 1000 P/R |
|---|---|---|---|
| FC932 | 210 | `6.35` mm/pulse -> C4_Packet_Length_mm (used by FC1215 / DB15) | `0.635` |
| FC932 | 169-183 | PacketLength_C4 (Ch2 pulses), Frac x 0.2 | values x10 (Frac factor stays 0.2, result x10) |
| FC932 | 279 | Surface_Length_C4 vs PIW 330 | follows FC2 |
| FC932 | 440 | clearing: Ch2 > **2000** pulses | **20000** (still < 32767) |
| FC932 | 57-129 | **E 6.6** "encoder stopped" (input unchanged 500 ms) | **RISK**: 1000 P/R = 0.6 ms pulses, faster than the DI input filter (3 ms) -> E 6.6 may look stuck -> T90/T91 -> resets surface gate M166.3. Replace by "PIW 330 unchanged for 500 ms" |
| FC2 | 16 | Surface_Length_C4 = **800** pulses | **8000** |
| FC948 | 272 | SCALER X1 55 / X2 160 pulses (turntable run time) | **550 / 1600** |
| FC1208 | 37-43 | `6.673` mm/pulse -> MW 202 (HMI) | `0.6673` |

Also: FM350 DB / HW Config limits or comparison values for Ch2/Ch3, if any; the LAUER C4 display if it shows pulses.
16-bit check: Ch3 (surface) wraps every 32767 x 0.635 = 20.8 m. Differences with -I stay correct if < 20 m.

Note: FC932 uses 6.35 and FC1208 uses 6.673 for the same encoder - two calibrations. Check one packet with a tape.

## Done 2026-11-27: set 4f in READY_TO_DOWNLOAD (DB1 v0.2, FC2 v0.2, FC932 v0.2, FC948 v0.1, FC1208 v1.1)
DB1.DBW0 `C4_Encoder_PPR` = 100, DB1.DBW18 `C4_Wheel_Circ_01mm` = 6350. At 100 P/R every value is the same as today.
Swap day: set DBW0 = 1000 (VAT) + DB1 initial value 1000. Still open before the swap: replace the E 6.6 checks
(FC932 T90/T91 and **FC1300** Timer 130/131 fault M30.0). Note: PIW 330/332 are gated (count only while their gate
is open), so a free-running count is needed (spare FM350 channel wired in parallel, like Ch2/Ch3) or a check limited
to when the gate is open.
