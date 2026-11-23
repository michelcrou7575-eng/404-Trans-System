# NS12 alarm list (DB13 "HMI ALARMS", written by FC1220 v1.0)

Address format from the NS12 project: `SERIALA:DB0013_DBXbbbbb.ii`

| # | NS12 address | Group | Text | PLC condition |
|---|---|---|---|---|
| 1 | `SERIALA:DB0013_DBX00000.00` | General | Fuse fault | `A "M 0.4"` |
| 2 | `SERIALA:DB0013_DBX00000.01` | General | Motor protection tripped | `A "M 0.5"` |
| 3 | `SERIALA:DB0013_DBX00000.02` | General | Motor temperature fault | `A "M 0.6"` |
| 4 | `SERIALA:DB0013_DBX00000.03` | General | Compressed air below 5 bar | `A "M 0.7"` |
| 5 | `SERIALA:DB0013_DBX00000.04` | E-Stop | E-STOP desk X120 (HMI box) | `A "M 1.0"` |
| 6 | `SERIALA:DB0013_DBX00000.05` | E-Stop | E-STOP desk X121 (feeder box) | `A "M 1.1"` |
| 7 | `SERIALA:DB0013_DBX00000.06` | E-Stop | E-STOP elevator station | `A "M 1.2"` |
| 8 | `SERIALA:DB0013_DBX00000.07` | E-Stop | E-STOP flipper station | `A "M 1.3"` |
| 9 | `SERIALA:DB0013_DBX00001.00` | Door | Door open - feeder | `A "M 1.5"` |
| 10 | `SERIALA:DB0013_DBX00001.01` | Door | Door open - elevator | `A "M 1.6"` |
| 11 | `SERIALA:DB0013_DBX00001.02` | Door | Door open - flipper | `A "M 1.7"` |
| 12 | `SERIALA:DB0013_DBX00002.00` | Conveyor | C2 angle conveyor fault | `A "M 22.7"` |
| 13 | `SERIALA:DB0013_DBX00002.01` | Conveyor | Elevator rollers (C0) fault | `A "M 30.1"` |
| 14 | `SERIALA:DB0013_DBX00002.02` | Conveyor | Elevator pusher fault | `A "M 30.2"` |
| 15 | `SERIALA:DB0013_DBX00002.03` | Conveyor | Elevator - packet not centered | `A "M 14.7"` |
| 16 | `SERIALA:DB0013_DBX00002.04` | Conveyor | C4 collator fault | `A "M 30.0"` |
| 17 | `SERIALA:DB0013_DBX00002.05` | Conveyor | C4 collator timeout stop | `A "M 30.7"` |
| 18 | `SERIALA:DB0013_DBX00002.06` | Conveyor | C4 infeed obstruction | `A "M 33.7"` |
| 19 | `SERIALA:DB0013_DBX00002.07` | Conveyor | C6 flipper delivery fault | `A "M 38.7"` |
| 20 | `SERIALA:DB0013_DBX00003.00` | Conveyor | Flipper flip obstructed | `A "M 42.7"` |
| 21 | `SERIALA:DB0013_DBX00003.01` | Conveyor | C10 pivot conveyor fault | `A "M 54.7"` |
| 22 | `SERIALA:DB0013_DBX00003.02` | Conveyor | Pivot timeout | `A "M 98.1"` |
| 23 | `SERIALA:DB0013_DBX00003.03` | Conveyor | Pivot / conveyor conflict | `A "M 98.2"` |
| 24 | `SERIALA:DB0013_DBX00003.04` | Conveyor | C13 delivery fault (low) | `A "M 66.7"` |
| 25 | `SERIALA:DB0013_DBX00003.05` | Conveyor | C23 delivery fault (high) | `A "M 86.7"` |
| 26 | `SERIALA:DB0013_DBX00004.00` | Drive | Drive U44.3 fault - C4 | `A "M 3.0"` |
| 27 | `SERIALA:DB0013_DBX00004.01` | Drive | Drive U45.0 fault - C5 | `A "M 3.1"` |
| 28 | `SERIALA:DB0013_DBX00004.02` | Drive | Drive U45.3 fault - C6 | `A "M 3.2"` |
| 29 | `SERIALA:DB0013_DBX00004.03` | Drive | Drive U45.6 fault - C7 flipper conveyor | `A "M 3.3"` |
| 30 | `SERIALA:DB0013_DBX00004.04` | Drive | Drive U46.0 fault - Flipper | `A "M 3.4"` |
| 31 | `SERIALA:DB0013_DBX00004.05` | Drive | Drive U46.4 fault - C8 turntable conveyor | `A "M 3.5"` |
| 32 | `SERIALA:DB0013_DBX00004.06` | Drive | Drive U47.0 fault - Turntable | `A "M 3.6"` |
| 33 | `SERIALA:DB0013_DBX00004.07` | Drive | Drive U47.5 fault - C9 pusher 2 conveyor | `A "M 3.7"` |
| 34 | `SERIALA:DB0013_DBX00005.00` | Drive | Drive U47.6 fault - Pusher 2 | `A "M 4.0"` |
| 35 | `SERIALA:DB0013_DBX00005.01` | Drive | Drive U48.0 fault - C10 | `A "M 4.1"` |
| 36 | `SERIALA:DB0013_DBX00005.02` | Drive | Drive U48.3 fault - C11 | `A "M 4.2"` |
| 37 | `SERIALA:DB0013_DBX00005.03` | Drive | Drive U48.6 fault - C12 | `A "M 4.3"` |
| 38 | `SERIALA:DB0013_DBX00005.04` | Drive | Drive U49.0 fault - C13 | `A "M 4.4"` |
| 39 | `SERIALA:DB0013_DBX00005.05` | Drive | Drive U53.2 fault - C21 | `A "M 4.5"` |
| 40 | `SERIALA:DB0013_DBX00005.06` | Drive | Drive U53.4 fault - C22 | `A "M 4.6"` |
| 41 | `SERIALA:DB0013_DBX00005.07` | Drive | Drive U54.0 fault - C23 | `A "M 4.7"` |
| 42 | `SERIALA:DB0013_DBX00006.00` | Sensor | Sensor Elevator platform infeed B5.1 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 5.1"` |
| 43 | `SERIALA:DB0013_DBX00006.01` | Sensor | Sensor Elevator platform limit B5.2 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 5.2"` |
| 44 | `SERIALA:DB0013_DBX00006.02` | Sensor | Sensor C1 exit B5.4 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 5.4"` |
| 45 | `SERIALA:DB0013_DBX00006.03` | Sensor | Sensor C2 infeed B5.5 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 5.5"` |
| 46 | `SERIALA:DB0013_DBX00006.04` | Sensor | Sensor C2 roller center B6.0 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 6.0"` |
| 47 | `SERIALA:DB0013_DBX00006.05` | Sensor | Sensor C4 infeed B6.7 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 6.7"` |
| 48 | `SERIALA:DB0013_DBX00006.06` | Sensor | Sensor C4 exit B7.0 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 7.0"` |
| 49 | `SERIALA:DB0013_DBX00006.07` | Sensor | Sensor C5 exit B7.1 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 7.1"` |
| 50 | `SERIALA:DB0013_DBX00007.00` | Sensor | Sensor C6 reaching B7.2 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 7.2"` |
| 51 | `SERIALA:DB0013_DBX00007.01` | Sensor | Sensor C6 exit B7.3 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 7.3"` |
| 52 | `SERIALA:DB0013_DBX00007.02` | Sensor | Sensor Flipper infeed B7.4 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 7.4"` |
| 53 | `SERIALA:DB0013_DBX00007.03` | Sensor | Sensor Flipper exit B8.2 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 8.2"` |
| 54 | `SERIALA:DB0013_DBX00007.04` | Sensor | Sensor C9 infeed B9.6 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 9.6"` |
| 55 | `SERIALA:DB0013_DBX00007.05` | Sensor | Sensor C9 packet edge B9.7 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 9.7"` |
| 56 | `SERIALA:DB0013_DBX00007.06` | Sensor | Sensor C10 infeed B10.4 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 10.4"` |
| 57 | `SERIALA:DB0013_DBX00007.07` | Sensor | Sensor C10 full B10.5 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 10.5"` |
| 58 | `SERIALA:DB0013_DBX00008.00` | Sensor | Sensor C11 exit B10.7 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 10.7"` |
| 59 | `SERIALA:DB0013_DBX00008.01` | Sensor | Sensor C12 exit B11.0 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 11.0"` |
| 60 | `SERIALA:DB0013_DBX00008.02` | Sensor | Sensor C13 slow B11.1 ON - line empty (packet left or dirty sensor) | `A #CUE A "B 11.1"` |
| 61 | `SERIALA:DB0013_DBX00008.03` | Sensor | Sensor C1 exit B5.4 OFF - line empty (check sensor / reflector) | `A #CUE AN "B 5.4"` |
| 62 | `SERIALA:DB0013_DBX00008.04` | Sensor | Sensor C9 packet edge B9.7 OFF - line empty (check sensor / reflector) | `A #CUE AN "B 9.7"` |
| 63 | `SERIALA:DB0013_DBX00009.00` | Status | Clearing (F4) active | `A "M 10.0"` |
| 64 | `SERIALA:DB0013_DBX00009.01` | Status | Packets present on C1-C2 / C7-C9 | `A "M 11.7"` |
| 65 | `SERIALA:DB0013_DBX00009.02` | Status | Control voltage OFF - press START | `AN "M 0.3" AN "M 0.2" AN "M 0.1"` |
| 66 | `SERIALA:DB0013_DBX00009.03` | Status | Start ready (10 s) | `A "M 0.2" AN "M 0.3"` |
