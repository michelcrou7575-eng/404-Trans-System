# Packet width measure (C10 transfer, B10.5 + B10.6) — MEASUREMENT ONLY v0.6

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

## v0.4: encoder calibration on every transfer (no jog)
First live result (2026-11-18): `Width_mm` 477, real sack **407 mm**, `Speed_mm_s` 557. FM350 ch5 = **single** counting, OMRON E6C2-CWZ6C 600 P/R, wheel Ø 91–93 mm (≈ 300 mm standard wheel → 0.5 mm/pulse). The code factor 0.31 fits neither, and time/speed (855 ms × 517 mm/s = 442 mm) fits the sack better than the encoder.

**Calibration:** the `B10.5` and `B10.6` beams are **527 mm** apart (`Sensor_Dist_mm`). The pitch (packet + gap ≈ 650 mm) is longer, so the first packet front at `B10.6` after a front at `B10.5` is the **same packet**. For each such pair: pulses and mS between the two sensors. At the end of the transfer:
* `Cal_mm_Pulse` = 527 × pairs / pulses → **real encoder factor** (the code uses 0.31)
* `Cal_Speed_mm_s` = 527 × pairs × 1000 / mS → **real C10 fast speed** (31 m/min = 517)
* `Width_mm_Cal` = verified width with the real factor (compare with 407 mm minus the light-barrier extra)

Desk check (`desk_check_calibration.py`): 6 packets, gaps 163–217 → factor 0.2878 for a true 0.288, speed 517 for 517. Also correct with a packet between the sensors at start, and with U-shape sags.

| VAT | |
|---|---|
| `.Cal_Count` | Pairs used (≈ packets) |
| `.Cal_mm_Pulse` | Real mm/pulse |
| `.Cal_Speed_mm_s` | Real C10 fast speed |
| `.Width_mm_Cal` | Width with the real factor |

If `Cal_mm_Pulse` is stable over a few transfers, the same correction applies to C10's own width measurement (FC1054 uses 0.31 for "Collator Full"): to decide after the data.

### C10 fast speed = 30.6 m/min = 510 mm/s (operator, 2026-11-18)
With the first transfer (≈ 1797 pulses/s, 855 ms per packet):
* Encoder factor ≈ 510 / 1797 = **0.284 mm/pulse** (code: 0.31, +9 %). A Ø 92 mm wheel with single counting would give 0.48: the wheel in the photo is probably not on the C10 encoder, or there is a ratio. `Cal_mm_Pulse` (v0.4) will confirm it.
* Optical width = 855 ms × 510 mm/s = **436 mm** for a **407 mm** sack: the light barriers see about **+29 mm** (beam + response + sack edges). C11…C23 sensors see the same, so `Width_ms_31` is the right value for the blanking.
* Expected v0.4 values: `Cal_Speed_mm_s` ≈ 510, `Cal_mm_Pulse` ≈ 0.284, `Width_mm_Cal` ≈ 436.

## v0.5: encoder read directly from the module (operator idea)
FC1300 reads the FM350-2 count values with **read jobs**: `CNT2_RD` job 100 (ch 0–3) on the rising edge of `M6.0` (100 mS clock) and job 101 (ch 4–7) on the falling edge, **called once only**. `CNT2_RD` is asynchronous, so `ACT_CNTV5` can be **100 mS or more old** (≥ 51 mm at 30.6 m/min). This also affects the C4/C10 measurements in FC1031/FC1054.

In another project the operator reads the FM350-2 directly: `L PID 264` = channel 0 count value. v0.5 can do the same, **switchable online** (no download):
| DB30 | |
|---|---|
| `Enc_Direct` | 0 = `ACT_CNTV5` (as before) / **1 = direct `PID` read every scan** |
| `Enc_PID_Addr` | Direct address. Default **328** (= module 320 + 8, like 410) |
| `Enc_Live` | Value used this scan |

**Try (online, no download):**
1. VAT: `PID 340`, `PID 348`, `"FM350 DB".ACT_CNTV5`. With C10 running, the right address **changes smoothly every refresh** and follows `ACT_CNTV5`.
2. Set `Enc_PID_Addr` to that address, then `Enc_Direct` = 1. `Enc_Live` must follow.
3. Compare `Cal_mm_Pulse`, `Cal_Speed_mm_s` (≈ 510) and `Width_mm_Cal` (≈ 436 for the 407 mm sacks) with `Enc_Direct` = 0 and = 1.

A wrong address only gives an access error (OB122 exists, the CPU stays in RUN, see the diagnostic buffer).

### From project 410 (same FM350-2)
`FC120`: `L PID 264` = channel 0 `ACT_CNTV`, **module base 256 + offset 8**, input area **PIW 256…271 (16 bytes)**, confirmed live. For 404 (module 320, `MOD_ADR` = `W#16#140`): **channel 0 = `PID 328`**, input area 320…335. 340/348 are outside it (access error), so the default is now 328.
**Open:** C10 is **channel 5**. With 16 input bytes there is room for 2 count values only (+8, +12). **Check online:** VAT `PID 328`, `PID 332` and `"FM350 DB".ACT_CNTV0` … `ACT_CNTV7` with C10 running: which channel do they follow? If channel 5 is not there, the fix is in FC1300 instead: call `CNT2_RD` until the job is done (`BUSY` = 0) and only then start the next one.

## FM350-2 hardware setup (operator screenshots, 2026-11-19)
* Module address **320** (`MOD_ADR` = `W#16#140`). Channels 0–7 as **single counters**, encoders **pulse & direction**. Ch 0: single counting, ch 2 and ch 5: **continuous counting**. No hardware gate, no interrupts, outputs **no comparison**.
* Program use (whole export): ch 0 = C3 slat, ch 2/3 = C4, ch 4/5 = C10, all through `ACT_CNTV` (read jobs in FC1300). Ch 1, 6, 7 unused. **Nothing reads the direct area** (no `PID`/`PIW`/`USER_STAT_WORD` access).
* **Direct area ("Specify Channels")**: User_Type1 (`PID 328`) = Word ch1 low + Word ch0 low; User_Type2 (`PID 332`) = Word ch3 low + Word ch2 low. **Channel 5 (C10) is not in it.**
* **Plan:** User_Type2 → **DWORD, Channel 5, Count Value** ⇒ `PID 332` = C10 count live, then DB30 `Enc_PID_Addr` = 332, `Enc_Direct` = 1. HW config download = CPU STOP for a moment, line empty (counters restart). First check the principle online: `PIW 328` / `PIW 330` follow `ACT_CNTV0` (C3) low word.

## v0.6: direct read as a 16-bit word (2026-11-19)
**Confirmed online:** `PIW 328` increases with C3 (`DB2.DBD 148` = `ACT_CNTV0`) with today's configuration, so in "Specify Channels" the **right-hand column is the lower address**. With the new configuration (User_Type1 = Ch3 | Ch0, User_Type2 = Ch5 | Ch2):

| Address | Channel | Conveyor |
|---|---|---|
| `PIW 328` | Ch 0 | C3 |
| `PIW 330` | Ch 3 | C4 surface |
| `PIW 332` | Ch 2 | C4 length |
| **`PIW 334`** | **Ch 5** | **C10** |

FC1210 v0.6: `Enc_Direct` = 1 reads **`PIW [Enc_PIW_Addr]`** (default **334**). The word wraps at 65536, so only the **difference to the last scan** (INT subtraction, wrap-safe up to 32767 pulses per scan) is added to `Enc_Live` (DINT). The rest of the measure is unchanged. Switching `Enc_Direct` online is bumpless (`Enc_Live` continues from its last value).
**Order:** HW Config change first (User_Type2 = Ch5 | Ch2), check `PIW 334` follows `ACT_CNTV5`, then `Enc_Direct` = 1.

### 2026-11-19: new HW Config active, confirmed online
Before the change, with the gates forced: `PIW 332` = Ch2 (`SW_GATE2`), `PIW 334` = Ch3 (`SW_GATE3`), `PIW 330` = 0 (Ch1). After the change: **`PIW 334` follows C10 (`ACT_CNTV5`)**. Direct area now: 328 = Ch0 (C3), 330 = Ch3 (C4 surface), 332 = Ch2 (C4 length), **334 = Ch5 (C10)**. Next: width measure v0.6 with `Enc_Direct` = 1.
