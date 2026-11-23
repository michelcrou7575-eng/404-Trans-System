# Blanking shadow counts (DB31) - measurement log

| File | What |
|---|---|
| `2026-11-20_1_VAT_after_v0.10_download_Width_958.png` | Width measure v0.10 downloaded. PIW = ACT_CNTV on C3/C4/C10. `"BLANKING DB".Width_ms` = 958 (measured, bigger packets today) |
| `2026-11-20_2_VAT_PIW_check_Width_967.png` | PIW check: PIW 328 ahead of ACT_CNTV0 (read every scan). PIW 332 = Ch2 C4 length, PIW 330 = Ch3 C4 surface (symbol comments were swapped, fixed by user) |
| `2026-11-20_3_VAT_blanking_counts.png` | Count: C10 60 = C11 30 + C21 30; C12 30; C22 25 (one load still on C22) |
| `2026-11-20_4_VAT_blanking_counts_and_raw.png` | Count / Raw: C10 66/66, **C11 (B10.7) 36/41: 5 U-shape fronts ignored**, C12 31/31, C21 30/30, C22 30/30 |
| `2026-11-20_5_VAT_blanking_counts_and_raw.png` | Count / Raw: C10 90/90, **C11 43/48 (still 5 ignored in total)**, C12 37/37, C21 42/42, C22 37/37. Still on the conveyors at that moment (by difference): C11+C21 5, C12 6, C22 5 - to check against the HMI |
| `2026-11-20_6_VAT_blanking_counts_and_raw.png` | Count / Raw: C10 132/132, C11 66/71 (still 5 ignored, no new ones since reading 3), C12 61/61, C21 61/61, C22 55/55. On conveyors by difference: C11+C21 5, C12 5, C22 6 |
| `2026-11-20_C4_collating_photo.jpg` | C4 collating, order of 2026-11-20 (Omya Snowhite 50 lb sacks): flat packets, gaps about 1/3 to 1/2 packet |
| `2026-11-20_C10_load_photo.jpg` | C10 (pivot) with a full load, same order, seen from the side: packets close together, not perfectly flat |
| `2026-11-23_1/2_DB30_v0.10_online*.png` | DB30 v0.10 downloaded (DBW160 inside the block). New order: Width_mm 571, Width_ms_31 1035, Cal_mm_Pulse 0.2802, Cal_Speed 504 mm/s |
| `2026-11-23_3/4_DB31_weekend_totals_*.png` | Weekend totals Count/Raw/Sag/Butt: C10 9340/9340/1/1, **C11 4670/4698/28/0**, C12 4667/4667/0/0, **C21 4671/4684/14/1**, **C22 4666/4673/7/0**. C10 9340 vs C11+C21 9341: 1 off in 9340 |

## Result so far (2026-11-20)
- The blanking corrects B10.7 (C11 exit = C12 infeed), exactly where C12 counted wrong.
- No butted packets. Blank_Pct 90 / Butt_Pct 140 unchanged.
- Next: 1-2 more days, a U-shape order, readings with C12/C22 empty. Then FC1208 v0.12 (cleaned pulses for C11..C13 and C21..C23).

## Result after the weekend (2026-11-23)
- About 4670 packets per level. The blanking ignored 28 extra fronts at B10.7, 14 at B15.4, 7 at B15.5 (U-shape sags) that raw counting would have added.
- 1 packet difference out of 9340 between C10 exit and C11 + C21 exits (C10 Sag 1 + Butt 1 and C21 Butt 1 are the candidates).
- Ready for FC1208 v0.12 (cleaned pulses for C11..C13 / C21..C23), on the user's go.
