# Blanking shadow counts (DB31) - measurement log

| File | What |
|---|---|
| `2026-11-20_1_VAT_after_v0.10_download_Width_958.png` | Width measure v0.10 downloaded. PIW = ACT_CNTV on C3/C4/C10. `"BLANKING DB".Width_ms` = 958 (measured, bigger packets today) |
| `2026-11-20_2_VAT_PIW_check_Width_967.png` | PIW check: PIW 328 ahead of ACT_CNTV0 (read every scan). PIW 332 = Ch2 C4 length, PIW 330 = Ch3 C4 surface (symbol comments were swapped, fixed by user) |
| `2026-11-20_3_VAT_blanking_counts.png` | Count: C10 60 = C11 30 + C21 30; C12 30; C22 25 (one load still on C22) |
| `2026-11-20_4_VAT_blanking_counts_and_raw.png` | Count / Raw: C10 66/66, **C11 (B10.7) 36/41: 5 U-shape fronts ignored**, C12 31/31, C21 30/30, C22 30/30 |

## Result so far (2026-11-20)
- The blanking corrects B10.7 (C11 exit = C12 infeed), exactly where C12 counted wrong.
- No butted packets. Blank_Pct 90 / Butt_Pct 140 unchanged.
- Next: 1-2 more days, a U-shape order, readings with C12/C22 empty. Then FC1208 v0.12 (cleaned pulses for C11..C13 and C21..C23).
