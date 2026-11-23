# NS12 symbols -> PLC fields (2026-11-23)

Symbol table exported from CX-Designer, matched with DB12 "HMI_DB" and DB1 "DB UTILITY" (offsets calculated from the DB sources).

⚠️ `Run_PB` = `"HMI_DB".ON_SW` and `ON_Sw` = `"HMI_DB".AERIAL_LINK_RUN_PB`: the two NS12 names are swapped compared with the PLC.

| NS12 symbol | Type | NS12 address | PLC field | Comment |
|---|---|---|---|---|
| AutoGen4 | BOOL | `M00000.00` | "M 0.0" (FL ALWAYS ON) |  |
| Emergency_Blinker | BOOL | `DB0012_DBX00000.01` | "HMI_DB".EMERGENCY_BLINK | FL Emergency Blink |
| Compressed_Air | BOOL | `DB0012_DBX00000.03` | "HMI_DB".COMPRESSED_AIR | FLS Compressed Air |
| Run_PB | BOOL | `DB0012_DBX00000.02` | "HMI_DB".ON_SW | FLS On Sw Temporary |
| ON_Sw | BOOL | `DB0012_DBX00000.04` | "HMI_DB".AERIAL_LINK_RUN_PB | FLS 508 Link Run SW - Diabled |
| AutoGen20 | CHANNEL | `DB0012_DBW00008` | "HMI_DB".word of BOOL bytes 8-9 (ELEVATOR_MOTOR_STATUS ... CONVEYOR_10_MOTOR_STATUS) |  |
| Service_SW_Status_1 | BOOL | `DB0012_DBX00001.00` | "HMI_DB".SERVICE_SW_1_STATUS | FLS Service 1 Switch |
| Service_SW_Status_3 | BOOL | `DB0012_DBX00001.02` | "HMI_DB".SERVICE_SW_3_STATUS | FLS Service 3 Switch |
| Service_SW_Status_2 | BOOL | `DB0012_DBX00001.01` | "HMI_DB".SERVICE_SW_2_STATUS | FLS Service 2 Switch |
| Service_SW_Status_1_2 | BOOL | `DB0012_DBX00001.03` | "HMI_DB".SERVICE_SW_1_2_STATUS | FLS Service 1 or 2 Switch |
| AutoGen25 | BOOL | `DB0012_DBX00001.04` | "HMI_DB".BIT12 | FLS Spare |
| AutoGen26 | BOOL | `DB0012_DBX00001.05` | "HMI_DB".BIT13 | FLS Spare |
| LB_1_Status | BOOL | `DB0012_DBX00003.00` | "HMI_DB".LIGHT_BARRIER_1_STATUS | FL Light Barrier 1 - B5.4 Conveyor 1 Exit - Status Bit |
| AutoGen29 | BOOL | `DB0012_DBX00008.00` | "HMI_DB".ELEVATOR_MOTOR_STATUS | FL Elevator - Motor M42.0 Status Bit |
| AutoGen30 | BOOL | `DB0012_DBX00008.02` | "HMI_DB".CONVEYOR_1_MOTOR_STATUS | FL Conv 1 - Motor M43.0 Status Bit |
| AutoGen32 | BOOL | `DB0012_DBX00005.00` | "HMI_DB".BIT40 | FL Elevator Motion |
| AutoGen33 | BOOL | `DB0012_DBX00005.01` | "HMI_DB".BIT41 | FL Elevator Motion |
| AutoGen34 | BOOL | `DB0012_DBX00005.02` | "HMI_DB".BIT42 | FL Elevator Motion |
| AutoGen35 | BOOL | `DB0012_DBX00005.03` | "HMI_DB".BIT43 | FL Elevator Motion |
| AutoGen36 | BOOL | `DB0012_DBX00005.04` | "HMI_DB".BIT44 | FL Elevator Motion |
| AutoGen37 | BOOL | `DB0012_DBX00005.05` | "HMI_DB".BIT45 | FL Elevator Motion |
| AutoGen38 | BOOL | `DB0012_DBX00005.06` | "HMI_DB".BIT46 | FL Elevator Motion |
| AutoGen39 | CHANNEL | `DB0012_DBW00005` | "HMI_DB".word of BOOL bytes 5-6 (BIT40 ... BIT55) |  |
| AutoGen40 | BOOL | `DB0012_DBX00005.07` | "HMI_DB".BIT47 | FL Elevator Motion |
| AutoGen43 | BOOL | `DB0012_DBX00006.00` | "HMI_DB".BIT48 | FL Pusher 1 Motion |
| AutoGen44 | BOOL | `DB0012_DBX00006.01` | "HMI_DB".BIT49 | FL Pusher 1 Motion |
| AutoGen45 | BOOL | `DB0012_DBX00006.02` | "HMI_DB".BIT50 | FL Pusher 1 Motion |
| AutoGen46 | BOOL | `DB0012_DBX00006.03` | "HMI_DB".BIT51 | FL Pusher 1 Motion |
| AutoGen47 | BOOL | `DB0012_DBX00006.04` | "HMI_DB".BIT52 | FL Pusher 1 Motion |
| AutoGen48 | BOOL | `DB0012_DBX00006.05` | "HMI_DB".BIT53 | FL Pusher 1 Motion |
| AutoGen49 | BOOL | `DB0012_DBX00006.06` | "HMI_DB".BIT54 | FL Pusher 1 Motion |
| AutoGen50 | BOOL | `DB0012_DBX00006.07` | "HMI_DB".BIT55 | FL Pusher 1 Motion |
| AutoGen51 | BOOL | `DB0012_DBX00007.00` | "HMI_DB".BIT56 | FL Pusher 2 Motion |
| Position_Adj_Enable_SW | BOOL | `DB0012_DBX00001.06` | "HMI_DB".SERVICE_SW_2_TIME_ADJ | FLS Service 2 Switch - Time Adjust |
| AutoGen55 | BOOL | `DB0012_DBX00007.01` | "HMI_DB".BIT57 | FL Pusher 2 Motion |
| AutoGen57 | BOOL | `DB0012_DBX00009.00` | "HMI_DB".CONVEYOR_6_MOTOR_STATUS | FL Conveyor 6 - Motor M45.3 Status Bit |
| AutoGen58 | BOOL | `DB0012_DBX00007.02` | "HMI_DB".BIT58 | FL Pusher 2 Motion |
| AutoGen59 | BOOL | `DB0012_DBX00007.03` | "HMI_DB".BIT59 | FL Pusher 2 Motion |
| AutoGen60 | BOOL | `DB0012_DBX00007.04` | "HMI_DB".BIT60 | FL Pusher 2 Motion |
| AutoGen61 | BOOL | `DB0012_DBX00007.05` | "HMI_DB".BIT61 | FL Pusher 2 Motion |
| AutoGen64 | BOOL | `DB0012_DBX00014.05` | "HMI_DB".PROX_11_STATUS | FL Prox 11 - P9.2 TurnTable Rotation Exit Slow - Status Bit |
| AutoGen67 | BOOL | `DB0012_DBX00012.05` | "HMI_DB".LIGHT_BARRIER_19_STATUS | FL Light Barrier 19 - B10.6 Conv 10 Exit Sens - Status Bit |
| AutoGen68 | CHANNEL | `DB0012_DBW00018` | "HMI_DB".word of BOOL bytes 18-19 (PROX_1_STATUS ... BIT159) |  |
| AutoGen69 | BOOL | `DB0012_DBX00018.05` | "HMI_DB".PROX_6_STATUS | FL Prox 6 - P4.5 Pusher 1 Limit - Status Bit |
| AutoGen70 | CHANNEL | `DB0012_DBW00020` | "HMI_DB".word of BOOL bytes 20-21 (SERVICE_SSW_MAIN ... BIT175) |  |
| AutoGen71 | BOOL | `DB0012_DBX00020.05` | "HMI_DB".MAN_FEED_SSW_STATUS | FL Hand Feed SW Main Screen - Status |
| AutoGen72 | CHANNEL | `DB0012_DBW00022` | "HMI_DB".word of BOOL bytes 22-23 (HMI_PUSHER_0_TEST_SSW ... HMI_CONVEYOR_7_TEST_SSW) |  |
| AutoGen73 | BOOL | `DB0012_DBX00022.05` | "HMI_DB".HMI_ROLLER_TEST_REV_SSW | FL Roller REV SW |
| E_Stop_Console_Status | BOOL | `DB0012_DBX00002.00` | "HMI_DB".E_STOP_CONSOLE_STATUS | FL E-Stop Console |
| E_Stop_Elevator_Status | BOOL | `DB0012_DBX00002.01` | "HMI_DB".E_STOP_ELEVATOR_STATUS | FL E-Stop Elevator |
| E_Stop_Flipper_Status | BOOL | `DB0012_DBX00002.02` | "HMI_DB".E_STOP_FLIPPER_STATUS | FL E-Stop Flipper |
| E_Stop_Loader_Status | BOOL | `DB0012_DBX00002.03` | "HMI_DB".E_STOP_LOADER_STATUS | FL E-Stop Loader |
| LB_2_Status | BOOL | `DB0012_DBX00003.01` | "HMI_DB".LIGHT_BARRIER_2_STATUS | FL Light Barrier 2 - B5.5 Conveyor 2 InFeed - Status Bit |
| LB_3_Status | BOOL | `DB0012_DBX00003.02` | "HMI_DB".LIGHT_BARRIER_3_STATUS | FL Light Barrier 3 - B6.0 Conveyor 2 Presence - Status Bit |
| LB_4_Status | BOOL | `DB0012_DBX00003.03` | "HMI_DB".LIGHT_BARRIER_4_STATUS | FL Light Barrier 4 - B6.1 Conveyor 2 Exit - Status Bit |
| LB_5_Status | BOOL | `DB0012_DBX00003.04` | "HMI_DB".LIGHT_BARRIER_5_STATUS | FL Light Barrier 5 - B6.2 Conveyor 3 InFeed - Status Bit |
| LB_6_Status | BOOL | `DB0012_DBX00003.05` | "HMI_DB".LIGHT_BARRIER_6_STATUS | FL Light Barrier 6 - B6.4 Conveyor 3 Exit - Status Bit |
| LB_B_Status | BOOL | `DB0012_DBX00003.06` | "HMI_DB".LIGHT_BARRIER_B_STATUS | FL Light Barrier B - B5.2 Elevator Limit - Status Bit |
| LB_A_Status | BOOL | `DB0012_DBX00003.07` | "HMI_DB".LIGHT_BARRIER_A_STATUS | FL Light Barrier A - B5.1 Elevator InFeed - Status Bit |
| AutoGen85 | BOOL | `DB0012_DBX00004.01` | "HMI_DB".BIT33 | FL Pusher 0 Motion |
| AutoGen86 | BOOL | `DB0012_DBX00004.00` | "HMI_DB".BIT32 | FL Pusher 0 Motion |
| AutoGen87 | BOOL | `DB0012_DBX00004.02` | "HMI_DB".BIT34 | FL Pusher 0 Motion |
| AutoGen88 | BOOL | `DB0012_DBX00004.03` | "HMI_DB".BIT35 | FL Pusher 0 Motion |
| AutoGen89 | BOOL | `DB0012_DBX00004.04` | "HMI_DB".BIT36 | FL Pusher 0 Motion |
| AutoGen90 | BOOL | `DB0012_DBX00004.05` | "HMI_DB".BIT37 | FL Pusher 0 Motion |
| Packetizer_Gate_Status | BOOL | `DB0012_DBX00001.07` | "HMI_DB".PACKETIZER_GATE_STATUS | FLS 2145 Packetizer Flap Gate - Status Bit |
| Init_PB | BOOL | `DB0012_DBX00000.06` | "HMI_DB".SERVICE_INIT_PB | FLS Service Initialisation PB |
| AutoGen93 | BOOL | `DB0012_DBX00008.01` | "HMI_DB".PUSHER_1_MOTOR_STATUS | FL Pusher 1 - Motor M42.6 Status Bit |
| AutoGen94 | BOOL | `DB0012_DBX00008.03` | "HMI_DB".CONVEYOR_2B_MOTOR_STATUS | FL Conv 2 Belt - Motor M43.4 Status Bit |
| AutoGen95 | BOOL | `DB0012_DBX00008.04` | "HMI_DB".CONVEYOR_2R_MOTOR_STATUS | FL Conv 2 Roller - Motor M43.5 Status Bit |
| AutoGen96 | BOOL | `DB0012_DBX00008.05` | "HMI_DB".CONVEYOR_3_MOTOR_STATUS | FL Conveyor 3 - Motor M44.0 Status Bit |
| AutoGen97 | CHANNEL | `DB0012_DBW00024` | "HMI_DB".word of BOOL bytes 24-25 (HMI_CONVEYOR_8_TEST_SSW ... LOADER_FING_SERVICE_SSW) |  |
| AutoGen120 | CHANNEL | `DB0012_DBW00030` | "HMI_DB".CONV_0_COLOR_WORD | WD Conveyor 0 - 2145 - Motor Status Color |
| AutoGen121 | CHANNEL | `DB0012_DBW00032` | "HMI_DB".ELEVATOR_COLOR_WORD | WD Elevator - Motor Status Color |
| AutoGen123 | CHANNEL | `DB0012_DBW00036` | "HMI_DB".CONV_1_COLOR_WORD | WD Conv 1 - Motor Status Color |
| HandFeed_Arrow_Status | BOOL | `DB0012_DBX00002.04` | "HMI_DB".HAND_FEED_ARROW_STATUS | FL Hand Feed Arrow |
| Elevator_Door_Status | BOOL | `DB0012_DBX00002.05` | "HMI_DB".ELEVATOR_DOOR_STATUS | FL Elevator Door |
| AutoGen127 | BOOL | `DB0012_DBX00007.06` | "HMI_DB".BIT62 | FL Pusher 2 Motion |
| AutoGen128 | CHANNEL | `DB0012_DBW00038` | "HMI_DB".CONV_2_BELT_COLOR_WORD | WD Conv 2 Belt - Motor Status Color |
| AutoGen129 | CHANNEL | `DB0012_DBW00040` | "HMI_DB".LIFT_ROLLER_2_COLOR_WORD | WD Lift 2 Roller - Actuator Status Color |
| AutoGen130 | CHANNEL | `DB0012_DBW00046` | "HMI_DB".CONV_4_COLOR_WORD | WD Conveyor 4 - Motor Status Color |
| AutoGen131 | CHANNEL | `DB0012_DBW00042` | "HMI_DB".CONV_2_ROLLER_COLOR_WORD | WD Conv 2 Roller - Motor Status Color |
| AutoGen132 | CHANNEL | `DB0012_DBW00048` | "HMI_DB".CONV_5_COLOR_WORD | WD Conveyor 5 - Motor Status Color |
| AutoGen133 | CHANNEL | `DB0012_DBW00044` | "HMI_DB".CONV_3_COLOR_WORD | WD Conveyor 3 - Motor Status Color |
| AutoGen134 | CHANNEL | `DB0012_DBW00050` | "HMI_DB".CONV_6_COLOR_WORD | WD Conveyor 6 - Motor Status Color |
| AutoGen135 | BOOL | `DB0012_DBX00004.06` | "HMI_DB".BIT38 | FL Pusher 0 Motion |
| AutoGen136 | BOOL | `DB0012_DBX00004.07` | "HMI_DB".BIT39 | FL Pusher 0 Motion |
| Flipper_Door_Status | BOOL | `DB0012_DBX00002.06` | "HMI_DB".FLIPPER_DOOR_STATUS | FL Flipper Door |
| AutoGen138 | CHANNEL | `DB0012_DBW00052` | "HMI_DB".CONV_7_COLOR_WORD | WD Conveyor 7 - Motor Status Color |
| AutoGen140 | CHANNEL | `DB0012_DBW00056` | "HMI_DB".CONV_8_COLOR_WORD | WD Conveyor 8 - Motor M46.4 Status Color |
| AutoGen142 | CHANNEL | `DB0012_DBW00060` | "HMI_DB".CONV_9_COLOR_WORD | WD Conveyor 9 - Motor M47.5 Status Color |
| AutoGen144 | CHANNEL | `DB0012_DBW00064` | "HMI_DB".CONV_10_COLOR_WORD | WD Conveyor 10 - Motor M48.0 Status Color |
| AutoGen145 | CHANNEL | `DB0012_DBW00066` | "HMI_DB".CONV_11_COLOR_WORD | WD Conveyor 11 - Motor M48.3 Status Color |
| AutoGen146 | CHANNEL | `DB0012_DBW00068` | "HMI_DB".CONV_12_COLOR_WORD | WD Conveyor 12 - Motor M48.6 Status Color |
| AutoGen149 | BOOL | `DB0012_DBX00011.01` | "HMI_DB".LIGHT_BARRIER_7_STATUS | FL Light Barrier 7 - B6.7 Conv 4 InFeed Sens - Status |
| AutoGen150 | BOOL | `DB0012_DBX00011.02` | "HMI_DB".LIGHT_BARRIER_8_STATUS | FL Light Barrier 8 - B7.0 Conv 4 Exit Sens - Status |
| AutoGen151 | BOOL | `DB0012_DBX00011.03` | "HMI_DB".LIGHT_BARRIER_9_STATUS | FL Light Barrier 9 - B7.1 Conv 5 Exit Sens - Status |
| AutoGen152 | BOOL | `DB0012_DBX00011.04` | "HMI_DB".LIGHT_BARRIER_10_STATUS | FL Light Barrier 10 - B7.2 Conv 6 Slow Sens - Status Bit |
| AutoGen153 | BOOL | `DB0012_DBX00011.05` | "HMI_DB".LIGHT_BARRIER_11_STATUS | FL Light Barrier 11 - B7.3 Conv 6 Exit Sens - Status Bit |
| AutoGen154 | BOOL | `DB0012_DBX00011.06` | "HMI_DB".LIGHT_BARRIER_12_STATUS | FL Light Barrier 12 - B7.4 Flipper InFeed Sens - Status Bit |
| AutoGen155 | BOOL | `DB0012_DBX00011.07` | "HMI_DB".LIGHT_BARRIER_13_STATUS | FL Light Barrier 13 - B8.2 Flipper Exit Sens - Status Bit |
| AutoGen156 | BOOL | `DB0012_DBX00012.00` | "HMI_DB".LIGHT_BARRIER_14_STATUS | FL Light Barrier 14 - B9.6 Conv 9 InFeed Sens - Status Bit |
| AutoGen157 | BOOL | `DB0012_DBX00012.01` | "HMI_DB".LIGHT_BARRIER_15_STATUS | FL Light Barrier 15 - B9.7 Conv 9 Packet Sens - Status Bit |
| AutoGen158 | BOOL | `DB0012_DBX00012.02` | "HMI_DB".LIGHT_BARRIER_16_STATUS | FL Light Barrier 16 - B10.3 Conv 10 Start Sens - Status Bit |
| AutoGen159 | BOOL | `DB0012_DBX00012.03` | "HMI_DB".LIGHT_BARRIER_17_STATUS | FL Light Barrier 17 - B10.4 Conv 10 InFeed Sens - Status Bit |
| AutoGen160 | BOOL | `DB0012_DBX00012.04` | "HMI_DB".LIGHT_BARRIER_18_STATUS | FL Light Barrier 18 - B10.5 Conv 10 Full Sens - Status Bit |
| AutoGen161 | BOOL | `DB0012_DBX00012.07` | "HMI_DB".LIGHT_BARRIER_21_STATUS | FL Light Barrier 21 - B11.0 Conv 12 Exit Sens - Status Bit- Status Bit |
| AutoGen162 | BOOL | `DB0012_DBX00012.06` | "HMI_DB".LIGHT_BARRIER_20_STATUS | FL Light Barrier 20 - B10.7 Conv 11 Exit Sens - Status Bit |
| AutoGen163 | BOOL | `DB0012_DBX00013.00` | "HMI_DB".LIGHT_BARRIER_22_STATUS | FL Light Barrier 22 - B11.1 Conv 13 Slow Sens - Status Bit |
| AutoGen164 | BOOL | `DB0012_DBX00013.01` | "HMI_DB".LIGHT_BARRIER_23_STATUS | FL Light Barrier 23 - B11.2 Conv 13 Exit Sens - Status Bit |
| AutoGen165 | BOOL | `DB0012_DBX00013.04` | "HMI_DB".LIGHT_BARRIER_26_STATUS | FL Light Barrier 26 - B15.4 Conv 21 Exit Sens - Status Bit |
| AutoGen166 | BOOL | `DB0012_DBX00013.05` | "HMI_DB".LIGHT_BARRIER_27_STATUS | FL Light Barrier 27 - B15.5 Conv 22 Exit Sens - Status Bit |
| AutoGen167 | BOOL | `DB0012_DBX00013.06` | "HMI_DB".LIGHT_BARRIER_28_STATUS | FL Light Barrier 28 - B15.6 Conv 23 Slow Sens - Status Bit |
| AutoGen168 | BOOL | `DB0012_DBX00013.07` | "HMI_DB".LIGHT_BARRIER_29_STATUS | FL Light Barrier 29 - B15.7 Conv 23 Exit Sens - Status Bit |
| AutoGen169 | BOOL | `DB0012_DBX00013.02` | "HMI_DB".LIGHT_BARRIER_24_STATUS | FL Light Barrier 24 - B12.3 Fingers Delivery Sens - Status Bit |
| AutoGen170 | BOOL | `DB0012_DBX00013.03` | "HMI_DB".LIGHT_BARRIER_25_STATUS | FL Light Barrier 25 - B13.0 Loader Empty Sens - Status Bit |
| AutoGen171 | CHANNEL | `DB0012_DBW00070` | "HMI_DB".CONV_13_COLOR_WORD | WD Conveyor 13 - Motor M49.0 Status Color |
| AutoGen172 | CHANNEL | `DB0012_DBW00072` | "HMI_DB".CONV_21_COLOR_WORD | WD Conveyor 21 - Motor M53.4 Status Color |
| AutoGen173 | CHANNEL | `DB0012_DBW00074` | "HMI_DB".CONV_22_COLOR_WORD | WD Conveyor 22 - Motor M53.6 Status Color |
| AutoGen174 | CHANNEL | `DB0012_DBW00076` | "HMI_DB".CONV_23_COLOR_WORD | WD Conveyor 23 - Motor M54.0 Status Color |
| AutoGen175 | BOOL | `DB0012_DBX00014.00` | "HMI_DB".LIGHT_BARRIER_30_STATUS | FL Light Barrier 30 - B35.2 Conv 0 InFeed Sens - Status Bit |
| AutoGen176 | BOOL | `DB0012_DBX00014.01` | "HMI_DB".LIGHT_BARRIER_31_STATUS | FL Light Barrier 31 - B35.3 Conv 0 Exit Sens - Status Bit |
| AutoGen177 | BOOL | `DB0012_DBX00014.02` | "HMI_DB".LIGHT_BARRIER_32_STATUS | FL Light Barrier 32 - B35.4 Conv 0 Length Sens - Status Bit |
| AutoGen178 | BOOL | `DB0012_DBX00014.03` | "HMI_DB".PROX_9_STATUS | FL Prox 9 - P8.5 TurnTable Rotation InFeed Slow - Status Bit |
| AutoGen179 | BOOL | `DB0012_DBX00014.04` | "HMI_DB".PROX_10_STATUS | FL Prox 10 - P8.6 TurnTable Rotation InFeed Stop - Status Bit |
| AutoGen180 | BOOL | `DB0012_DBX00014.06` | "HMI_DB".PROX_12_STATUS | FL Prox 12 - P9.3 TurnTable Rotation Exit Stop - Status Bit |
| AutoGen181 | BOOL | `DB0012_DBX00014.07` | "HMI_DB".PROX_13_STATUS | FL Prox 13 - P10.0 Pusher 2 Retract Sens - Status Bit |
| AutoGen182 | CHANNEL | `DB0012_DBW00090` | "HMI_DB".CONV_3_COUNT | WD Slat Conveyor 3 - Packet Count |
| AutoGen183 | CHANNEL | `DB0012_DBW00092` | "HMI_DB".CONV_4_COUNT | WD Collator Conveyor 4 - Packet Count |
| AutoGen184 | CHANNEL | `DB0012_DBW00094` | "HMI_DB".CONV_5_COUNT | WD Link Conveyor 5 - Packet Count |
| AutoGen185 | CHANNEL | `DB0012_DBW00096` | "HMI_DB".CONV_6_COUNT | WD Delivery Conveyor 6 - Packet Count |
| AutoGen186 | CHANNEL | `DB0012_DBW00098` | "HMI_DB".CONV_10_COUNT | WD Pivot Conveyor 10 - Packet Count |
| AutoGen187 | CHANNEL | `DB0012_DBW00100` | "HMI_DB".CONV_11_COUNT | WD Cumul Conveyor 11 - Packet Count |
| AutoGen188 | CHANNEL | `DB0012_DBW00102` | "HMI_DB".CONV_12_COUNT | WD Cumul Conveyor 12 - Packet Count |
| AutoGen189 | CHANNEL | `DB0012_DBW00104` | "HMI_DB".CONV_13_COUNT | WD Delivery Conveyor 13 - Packet Count |
| AutoGen190 | CHANNEL | `DB0012_DBW00106` | "HMI_DB".CONV_21_COUNT | WD Cumul Conveyor 21 - Packet Count |
| AutoGen191 | CHANNEL | `DB0012_DBW00108` | "HMI_DB".CONV_22_COUNT | WD Cumul Conveyor 22 - Packet Count |
| AutoGen192 | CHANNEL | `DB0012_DBW00110` | "HMI_DB".CONV_23_COUNT | WD Delivery Conveyor 23 - Packet Count |
| Loader_Door_Status | BOOL | `DB0012_DBX00002.07` | "HMI_DB".LOADER_DOOR_STATUS | FL Loader Door |
| AutoGen195 | BOOL | `DB0012_DBX00007.07` | "HMI_DB".CONVEYORS_CLEARING | FL Conveyors Clearing |
| AutoGen199 | BOOL | `DB0012_DBX00015.00` | "HMI_DB".PROX_14_STATUS | FL Prox 14 - P10.1 Pusher 2 Extend Sens - Status Bit |
| AutoGen200 | BOOL | `DB0012_DBX00015.01` | "HMI_DB".PROX_15_STATUS | FL Prox 15 - P15.0 Pivot 10 High Sens - Status Bit |
| AutoGen201 | BOOL | `DB0012_DBX00015.02` | "HMI_DB".PROX_16_STATUS | FL Prox 16 - P15.1 Pivot 10 Low Sens - Status Bit |
| AutoGen202 | BOOL | `DB0012_DBX00017.00` | "HMI_DB".TURNTABLE_DELIV_POSITION | FL TurnTable Delivery Position |
| AutoGen203 | BOOL | `DB0012_DBX00017.01` | "HMI_DB".TURNTABLE_REVERSE_ARROW | FL TurnTable Arrow Reverse Packet |
| AutoGen204 | BOOL | `DB0012_DBX00017.02` | "HMI_DB".TURNTABLE_DIR_SELECT_SW | FL TurnTable Direction Select SW |
| AutoGen205 | BOOL | `DB0012_DBX00015.03` | "HMI_DB".PROX_17_STATUS | FL Prox 17 - P13.2 Loader H Level Stop - Status Bit |
| AutoGen206 | BOOL | `DB0012_DBX00015.04` | "HMI_DB".PROX_18_STATUS | FL Prox 18 - P13.1 Loader H Level Slow - Status Bit |
| AutoGen207 | BOOL | `DB0012_DBX00015.05` | "HMI_DB".PROX_19_STATUS | FL Prox 19 - P11.4 Loader L Level Stop - Status Bit |
| AutoGen208 | BOOL | `DB0012_DBX00015.06` | "HMI_DB".PROX_20_STATUS | FL Prox 20 - P11.5 Loader L Level Slow - Status Bit |
| AutoGen211 | BOOL | `DB0012_DBX00015.07` | "HMI_DB".PROX_21_STATUS | FL Prox 21 - P11.6 Loader Slow Bot - Status Bit |
| AutoGen212 | BOOL | `DB0012_DBX00016.00` | "HMI_DB".PROX_22_STATUS | FL Prox 22 - P11.7 Loader Stop Bot - Status Bit |
| AutoGen213 | BOOL | `DB0012_DBX00016.01` | "HMI_DB".PROX_23_STATUS | FL Prox 23 - P12.0 Loader Finger Retract - Status Bit |
| AutoGen214 | BOOL | `DB0012_DBX00016.02` | "HMI_DB".PROX_24_STATUS | FL Prox 24 - P12.1 Loader Finger Extend - Status Bit |
| Feeder_Adj_Popup | BOOL | `DB0012_DBX00000.07` | "HMI_DB".ALL_SERVICE_ENABLE_SW | FLS All Services Enable Switch |
| AutoGen219 | BOOL | `DB0012_DBX00141.03` | "HMI_DB".CONV_8_INVERT_SELECT | FL TurnTable Conveyor 8 - Positioning Time - Display Selector Bit - INVERT |
| AutoGen225 | BOOL | `DB0012_DBX00143.01` | "HMI_DB".ELEVATOR_SERVICE_SW | FL Elevator / Pusher 1 - Service Enable |
| AutoGen227 | BOOL | `DB0012_DBX00143.02` | "HMI_DB".CONVEYOR_1_SERVICE_SW | FL Conveyor 1 - Service Enable Select - Screen 4 |
| AutoGen229 | BOOL | `DB0012_DBX00143.00` | "HMI_DB".CONVEYOR_0_SERVICE_SW | FL Conveyor 0 / Pusher 0 - Service Enable |
| AutoGen237 | BOOL | `DB0012_DBX00144.00` | "HMI_DB".CONVEYOR_7_SERVICE_SW | FL Conveyor 7 / Flipper - Service Enable Select - Screen 4 |
| AutoGen238 | BOOL | `DB0012_DBX00144.01` | "HMI_DB".CONVEYOR_8_SERVICE_SW | FL Conveyor 8 / TurnTable - Service Enable Select - Screen 4 |
| AutoGen239 | BOOL | `DB0012_DBX00144.02` | "HMI_DB".CONVEYOR_9_SERVICE_SW | FL Conveyor 9 / Pusher 2 - Service Enable Select - Screen 4 |
| AutoGen240 | BOOL | `DB0012_DBX00144.03` | "HMI_DB".CONVEYOR_10_SERVICE_SW | FL Conveyor 10 - Service Enable Select - Screen 4 |
| AutoGen241 | BOOL | `DB0012_DBX00144.04` | "HMI_DB".CONVEYOR_11_SERVICE_SW | FL Conveyors 11, 12, 13 - Service Enable Select - Screen 4 |
| AutoGen242 | BOOL | `DB0012_DBX00008.06` | "HMI_DB".CONVEYOR_4_MOTOR_STATUS | FL Conveyor 4 - Motor M44.3 Status Bit |
| AutoGen243 | BOOL | `DB0012_DBX00008.07` | "HMI_DB".CONVEYOR_5_MOTOR_STATUS | FL Conveyor 5 - Motor M45.0 Status Bit |
| AutoGen244 | BOOL | `DB0012_DBX00009.01` | "HMI_DB".CONVEYOR_7_MOTOR_STATUS | FL Conveyor 7 - Motor M45.6 Status Bit |
| AutoGen245 | BOOL | `DB0012_DBX00009.02` | "HMI_DB".FLIPPER_MOTOR_STATUS | FL Flipper Flip - Motor M46.0 Status Bit |
| AutoGen246 | BOOL | `DB0012_DBX00009.03` | "HMI_DB".CONVEYOR_8_MOTOR_STATUS | FL Conveyor 8 - Motor M46.4 Status Bit |
| AutoGen247 | BOOL | `DB0012_DBX00009.04` | "HMI_DB".TURNTABLE_MOTOR_STATUS | FL TurnTable - Motor M47.0 Status Bit |
| AutoGen248 | BOOL | `DB0012_DBX00009.05` | "HMI_DB".CONVEYOR_9_MOTOR_STATUS | FL Conveyor 9 - Motor M47.5 Status Bit |
| AutoGen249 | BOOL | `DB0012_DBX00009.06` | "HMI_DB".PUSHER_2_MOTOR_STATUS | FL Pusher 2 - Motor M47.6 Status Bit |
| AutoGen250 | BOOL | `DB0012_DBX00010.00` | "HMI_DB".CONVEYOR_11_MOTOR_STATUS | FL Conveyor 11 - Motor M48.3 Status Bit |
| AutoGen251 | BOOL | `DB0012_DBX00010.01` | "HMI_DB".CONVEYOR_12_MOTOR_STATUS | FL Conveyor 12 - Motor M48.6 Status Bit |
| AutoGen252 | BOOL | `DB0012_DBX00010.02` | "HMI_DB".CONVEYOR_13_MOTOR_STATUS | FL Conveyor 13 - Motor M49.0 Status Bit |
| AutoGen253 | BOOL | `DB0012_DBX00010.05` | "HMI_DB".CONVEYOR_23_MOTOR_STATUS | FL Conveyor 23 - Motor M54.0 Status Bit |
| AutoGen254 | BOOL | `DB0012_DBX00010.04` | "HMI_DB".CONVEYOR_22_MOTOR_STATUS | FL Conveyor 22 - Motor M53.4 Status Bit |
| AutoGen255 | BOOL | `DB0012_DBX00010.03` | "HMI_DB".CONVEYOR_21_MOTOR_STATUS | FL Conveyor 21 - Motor M53.2 Status Bit |
| AutoGen258 | BOOL | `DB0012_DBX00009.07` | "HMI_DB".CONVEYOR_10_MOTOR_STATUS | FL Conveyor 10 - Motor M48.0 Status Bit |
| AutoGen260 | BOOL | `DB0012_DBX00143.03` | "HMI_DB".CONVEYOR_2_SERVICE_SW | FL Conveyor 2 - Service Enable Select - Screen 4 |
| AutoGen269 | BOOL | `DB0012_DBX00018.00` | "HMI_DB".PROX_1_STATUS | FL Prox 1 - P4.0 Elevator Bottom Position - Status Bit |
| AutoGen270 | BOOL | `DB0012_DBX00018.01` | "HMI_DB".PROX_2_STATUS | FL Prox 2 - P4.1 Elevator SlowDown Bot - Status Bit |
| AutoGen271 | BOOL | `DB0012_DBX00018.02` | "HMI_DB".PROX_3_STATUS | FL Prox 3 - P4.2 Elevator SlowDown Top - Status Bit |
| AutoGen272 | BOOL | `DB0012_DBX00018.03` | "HMI_DB".PROX_4_STATUS | FL Prox 4 - P4.3 Elevator Top Position - Status Bit |
| AutoGen273 | BOOL | `DB0012_DBX00018.04` | "HMI_DB".PROX_5_STATUS | FL Prox 5 - P4.4 Pusher 1 Home - Status Bit |
| AutoGen274 | BOOL | `DB0012_DBX00018.06` | "HMI_DB".PROX_7_STATUS | FL Prox 7 - P8.0 Flipper Fingers Right Position - Status Bit |
| AutoGen275 | BOOL | `DB0012_DBX00018.07` | "HMI_DB".PROX_8_STATUS | FL Prox 8 - P8.1 Flipper Fingers Left Position - Status Bit |
| AutoGen276 | BOOL | `DB0012_DBX00019.01` | "HMI_DB".BIT153 | FL Loader Motion |
| AutoGen277 | BOOL | `DB0012_DBX00019.02` | "HMI_DB".BIT154 | FL Loader Motion |
| AutoGen278 | BOOL | `DB0012_DBX00019.03` | "HMI_DB".BIT155 | FL Loader Motion |
| AutoGen279 | BOOL | `DB0012_DBX00019.04` | "HMI_DB".BIT156 | FL Loader Motion |
| AutoGen280 | BOOL | `DB0012_DBX00019.05` | "HMI_DB".BIT157 | FL Loader Motion |
| AutoGen281 | BOOL | `DB0012_DBX00019.06` | "HMI_DB".BIT158 | FL Loader Motion |
| AutoGen282 | BOOL | `DB0012_DBX00019.07` | "HMI_DB".BIT159 | FL Loader Motion |
| AutoGen283 | BOOL | `DB0012_DBX00019.00` | "HMI_DB".BIT152 | FL Loader Motion |
| AutoGen285 | CHANNEL | `DB0012_DBW00078` | "HMI_DB".LOADER_LIFT_COLOR_WORD | WD Loader Lift - Motor M54.6 Status Color |
| AutoGen286 | BOOL | `DB0012_DBX00020.00` | "HMI_DB".SERVICE_SSW_MAIN | FL Service SW Main Screen |
| AutoGen287 | BOOL | `DB0012_DBX00020.01` | "HMI_DB".SERVICE_SSW_STATUS | FL Service SW Main Screen - Status |
| AutoGen288 | BOOL | `DB0012_DBX00020.03` | "HMI_DB".CLEARING_SSW_STATUS | FL Clearing SW Main Screen - Status |
| AutoGen289 | BOOL | `DB0012_DBX00020.02` | "HMI_DB".CLEARING_SSW_MAIN | FL Clearing SW Main Screen |
| AutoGen290 | BOOL | `DB0012_DBX00020.04` | "HMI_DB".MAN_FEED_SSW_MAIN | FL Hand Feed SW Main Screen |
| AutoGen291 | BOOL | `DB0012_DBX00020.07` | "HMI_DB".TURNTABLE_SSW_STATUS | FL Turn Table Select Main Screen - Status |
| AutoGen292 | BOOL | `DB0012_DBX00020.06` | "HMI_DB".TURNTABLE_SSW_MAIN | FL Turn Table Turn SW = 1:CCW - 0:CW Main Screen |
| AutoGen293 | BOOL | `DB0012_DBX00021.01` | "HMI_DB".FLIPPER_SSW_STATUS | FL Flipper SW Main Screen - Status |
| AutoGen294 | BOOL | `DB0012_DBX00021.00` | "HMI_DB".FLIPPER_SSW_MAIN | FL Flipper SW Main Screen |
| AutoGen295 | BOOL | `DB0012_DBX00021.03` | "HMI_DB".ROLLER_SSW_STATUS | FL Roller SW Main Screen - Status |
| AutoGen296 | BOOL | `DB0012_DBX00021.02` | "HMI_DB".ROLLER_SSW_MAIN | FL Roller SW Main Screen |
| AutoGen297 | BOOL | `DB0012_DBX00022.00` | "HMI_DB".HMI_PUSHER_0_TEST_SSW | FL Pusher 0 SW |
| AutoGen298 | BOOL | `DB0012_DBX00022.01` | "HMI_DB".HMI_ELEVATOR_SERVICE_SSW | FL Elevator Service SW |
| AutoGen299 | BOOL | `DB0012_DBX00022.02` | "HMI_DB".HMI_ELEVATOR_TEST_DN_SSW | FL Elevator DN PB |
| AutoGen300 | BOOL | `DB0012_DBX00022.03` | "HMI_DB".HMI_ELEVATOR_TEST_UP_SSW | FL Elevator UP PB |
| AutoGen301 | BOOL | `DB0012_DBX00022.04` | "HMI_DB".HMI_ROLLER_TEST_FWD_SSW | FL Roller FWD SW |
| AutoGen302 | BOOL | `DB0012_DBX00022.06` | "HMI_DB".HMI_PUSHER_1_TEST_SSW | FL Pusher 1 SW |
| AutoGen303 | BOOL | `DB0012_DBX00022.07` | "HMI_DB".HMI_CONVEYOR_1_TEST_SSW | FL Conv 1 SW |
| AutoGen304 | BOOL | `DB0012_DBX00023.00` | "HMI_DB".HMI_CONVEYOR_2B_TEST_SSW | FL Conv 2 Belt SW |
| AutoGen305 | BOOL | `DB0012_DBX00023.01` | "HMI_DB".HMI_CONVEYOR_2L_TEST_SSW | FL Conv 2 Lift SW |
| AutoGen306 | BOOL | `DB0012_DBX00023.02` | "HMI_DB".HMI_CONVEYOR_2R_TEST_SSW | FL Conv 2 Roller SW |
| AutoGen307 | BOOL | `DB0012_DBX00023.03` | "HMI_DB".HMI_CONVEYOR_3_TEST_SSW | FL Conv 3 SW |
| AutoGen308 | BOOL | `DB0012_DBX00023.04` | "HMI_DB".HMI_CONVEYOR_4_TEST_SSW | FL Conv 4 SW |
| AutoGen309 | BOOL | `DB0012_DBX00023.05` | "HMI_DB".HMI_CONVEYOR_5_TEST_SSW | FL Conv 5 SW |
| AutoGen310 | BOOL | `DB0012_DBX00023.06` | "HMI_DB".HMI_CONVEYOR_6_TEST_SSW | FL Conv 6 SW |
| AutoGen311 | BOOL | `DB0012_DBX00023.07` | "HMI_DB".HMI_CONVEYOR_7_TEST_SSW | FL Flipper Conv 7 SW |
| AutoGen312 | BOOL | `DB0012_DBX00024.00` | "HMI_DB".HMI_CONVEYOR_8_TEST_SSW | FL Turn Table Conv 8 SW |
| AutoGen313 | BOOL | `DB0012_DBX00024.01` | "HMI_DB".HMI_TURNTABLE_CCW_SSW | FL Turn Table / Conveyor CCW PB |
| AutoGen314 | BOOL | `DB0012_DBX00024.02` | "HMI_DB".HMI_TURNTABLE_CW_SSW | FL Turn Table / Conveyor CW PB |
| AutoGen315 | BOOL | `DB0012_DBX00024.03` | "HMI_DB".HMI_FLIPPER_SERVICE_SSW | FL Flipper Service SW |
| AutoGen316 | BOOL | `DB0012_DBX00024.04` | "HMI_DB".HMI_FLIPPER_FLIP_SSW | FL Flipper - Flip PB |
| AutoGen317 | BOOL | `DB0012_DBX00024.05` | "HMI_DB".HMI_CONVEYOR_9_TEST_SSW | FL Conv 9 SW |
| AutoGen318 | BOOL | `DB0012_DBX00024.06` | "HMI_DB".HMI_PUSHER_2_TEST_SSW | FL Pusher 2 SW |
| AutoGen319 | BOOL | `DB0012_DBX00024.07` | "HMI_DB".HMI_PIVOT_SERVICE_SSW | FL Conv 10 - Pivot Service SW |
| AutoGen320 | BOOL | `DB0012_DBX00025.00` | "HMI_DB".HMI_PIVOT_TEST_DN_SSW | FL Conv 10 - Pivot DN PB |
| AutoGen321 | BOOL | `DB0012_DBX00025.01` | "HMI_DB".HMI_PIVOT_TEST_UP_SSW | FL Conv 10 - Pivot UP PB |
| AutoGen324 | BOOL | `DB0012_DBX00025.04` | "HMI_DB".TURNTABLE_SERVICE_PBSHOW | FL TurnTable Service PB SHOW |
| AutoGen325 | BOOL | `DB0012_DBX00025.05` | "HMI_DB".TURNTABLE_SERVICE_SSW | FL TurnTable Service SW |
| AutoGen326 | BOOL | `DB0012_DBX00025.06` | "HMI_DB".HMI_CONVEYOR_10_TEST_SSW | FL Conv 10 - Conveyor SW |
| AutoGen327 | BOOL | `DB0012_DBX00025.07` | "HMI_DB".LOADER_FING_SERVICE_SSW | FL Loader Service SW - Fingers |
| AutoGen328 | BOOL | `DB0012_DBX00026.01` | "HMI_DB".LOADER_LIFT_TOP_PB | FL Loader Lift - TOP PB |
| AutoGen329 | BOOL | `DB0012_DBX00026.00` | "HMI_DB".LOADER_LIFT_SERVICE_SSW | FL Loader Service SW - Lift |
| AutoGen330 | BOOL | `DB0012_DBX00026.02` | "HMI_DB".LOADER_LIFT_UP_PB | FL Loader Lift - UP PB |
| AutoGen331 | BOOL | `DB0012_DBX00026.04` | "HMI_DB".FINGER_RETRACT_TEST_PB | FL Loader Fingers Retract PB |
| AutoGen332 | BOOL | `DB0012_DBX00026.05` | "HMI_DB".FINGER_EXTEND_TEST_PB | FL Loader Fingers Extend PB |
| AutoGen333 | BOOL | `DB0012_DBX00026.06` | "HMI_DB".FINGER_TILT_TEST_PB | FL Loader Fingers Tilt Down PB |
| AutoGen336 | BOOL | `DB0012_DBX00026.03` | "HMI_DB".LOADER_LIFT_DN_PB | FL Loader Lift - DOWN PB |
| AutoGen337 | CHANNEL | `DB0012_DBW00084` | "HMI_DB".HIGH_LEVEL_23_GRAPHIC | WD High Level Conveyor 23 |
| AutoGen338 | CHANNEL | `DB0012_DBW00086` | "HMI_DB".LOW_LEVEL_13_GRAPHIC | WD Low Level Conveyor 13 |
| AutoGen341 | BOOL | `DB0012_DBX00088.02` | "HMI_DB".PIVOT_GRAPHIC (bit 2 of byte 88) | WD Pivot Conveyor Graphic |
| AutoGen342 | BOOL | `DB0012_DBX00088.00` | "HMI_DB".PIVOT_GRAPHIC (bit 0 of byte 88) | WD Pivot Conveyor Graphic |
| AutoGen343 | BOOL | `DB0012_DBX00088.01` | "HMI_DB".PIVOT_GRAPHIC (bit 1 of byte 88) | WD Pivot Conveyor Graphic |
| AutoGen344 | BOOL | `DB0012_DBX00088.03` | "HMI_DB".PIVOT_GRAPHIC (bit 3 of byte 88) | WD Pivot Conveyor Graphic |
| AutoGen347 | BOOL | `DB0012_DBX00021.04` | "HMI_DB".ELEVATOR_ROUND_TRIP_SSW | FL Elevator - Round Trip PB |
| AutoGen351 | BOOL | `DB0012_DBX00021.06` | "HMI_DB".BIT174 |  |
| AutoGen354 | CHANNEL | `DB0012_DBW00112` | "HMI_DB".FLIPPER_CCW | WD Flipper Graphic CCW |
| AutoGen355 | CHANNEL | `DB0012_DBW00114` | "HMI_DB".FLIPPER_CW | WD Flipper Graphic CW |
| AutoGen357 | CHANNEL | `DB0012_DBW00120` | "HMI_DB".FLIPPER_COLOR | WD Flipper Color |
| AutoGen358 | CHANNEL | `DB0012_DBW00122` | "HMI_DB".FLIPPER_PACK_PRESENCE | WD Flipper - Packet Presence |
| AutoGen359 | CHANNEL | `DB0012_DBW00124` | "HMI_DB".TURNTABLE_PACK_PRESENCE | WD TurnTable - Packet Presence |
| AutoGen360 | CHANNEL | `DB0012_DBW00126` | "HMI_DB".ROLLER_PACK_PRESENCE | WD Pusher Roller - Packet Presence |
| AutoGen361 | CHANNEL | `DB0012_DBW00128` | "HMI_DB".PUSHER_PACK_PRESENCE | WD Pusher - Packet Presence |
| AutoGen366 | BOOL | `DB0012_DBX00027.00` | "HMI_DB".HMI_CONVEYOR_11_TEST_SSW | FL Conv 11 Test SW |
| AutoGen367 | BOOL | `DB0012_DBX00027.01` | "HMI_DB".HMI_CONVEYOR_12_TEST_SSW | FL Conv 12 Test SW |
| AutoGen368 | BOOL | `DB0012_DBX00027.02` | "HMI_DB".HMI_CONVEYOR_13_TEST_SSW | FL Conv 13 Test SW |
| AutoGen369 | BOOL | `DB0012_DBX00027.03` | "HMI_DB".HMI_CONVEYOR_21_TEST_SSW | FL Conv 21 Test SW |
| AutoGen370 | BOOL | `DB0012_DBX00027.04` | "HMI_DB".HMI_CONVEYOR_22_TEST_SSW | FL Conv 22 Test SW |
| AutoGen371 | BOOL | `DB0012_DBX00027.05` | "HMI_DB".HMI_CONVEYOR_23_TEST_SSW | FL Conv 23 Test SW |
| AutoGen372 | CHANNEL | `DB0012_DBW00152` | "HMI_DB".ACTUAL_HMI_SCREEN_NO | WD HMI Actual Display Screen |
| AutoGen373 | BOOL | `DB0012_DBX00026.07` | "HMI_DB".FINGER_BELT_TEST_SW | FL Loader Fingers Belt SW |
| AutoGen374 | CHANNEL | `DB0012_DBW00160` | "HMI_DB".CONV_7_POS_mS | WD Flipper Conveyor 7 - Positioning Time x10 [mS] |
| AutoGen375 | CHANNEL | `DB0012_DBW00162` | "HMI_DB".CONV_8_POS_FWD_mS | WD TurnTable Conveyor 8 - FWD Positioning Time x10 [mS] |
| AutoGen376 | CHANNEL | `DB0012_DBW00164` | "HMI_DB".CONV_8_POS_REV_mS | WD TurnTable Conveyor 8 - REV Positioning Time x10 [mS] |
| AutoGen377 | CHANNEL | `DB0012_DBW00166` | "HMI_DB".CONV_9_POS_mS | WD Pusher 2 Conveyor 9 - Positioning Time x10 [mS] |
| AutoGen378 | BOOL | `DB0012_DBX00144.07` | "HMI_DB".CTRL48 | FL Spare - Service Enable |
| AutoGen395 | BOOL | `DB0012_DBX00143.04` | "HMI_DB".CONVEYOR_3_SERVICE_SW | FL Conveyor 3 - Service Enable Select - Screen 4 |
| AutoGen396 | BOOL | `DB0012_DBX00143.05` | "HMI_DB".CONVEYOR_4_SERVICE_SW | FL Conveyor 4 - Service Enable Select - Screen 4 |
| AutoGen397 | BOOL | `DB0012_DBX00143.06` | "HMI_DB".CONVEYOR_5_SERVICE_SW | FL Conveyor 5 - Service Enable Select - Screen 4 |
| AutoGen398 | BOOL | `DB0012_DBX00143.07` | "HMI_DB".CONVEYOR_6_SERVICE_SW | FL Conveyor 6 - Service Enable Select - Screen 4 |
| AutoGen399 | BOOL | `DB0012_DBX00144.05` | "HMI_DB".CONVEYOR_21_SERVICE_SW | FL Conveyors 21, 22, 23 - Service Enable Select - Screen 4 |
| AutoGen400 | BOOL | `DB0012_DBX00144.06` | "HMI_DB".LOADER_SERVICE_ENABLE_SW | FL Loader - Service Enable |
| AutoGen403 | BOOL | `DB0012_DBX00011.00` | "HMI_DB".LOADER_BELT_MOTOR_STATUS | FL Loader Belt - Motor M51.0 Status Bit |
| AutoGen404 | BOOL | `DB0012_DBX00010.07` | "HMI_DB".LOADER_FING_MOTOR_STATUS | FL Loader Fingers - Motor M50.5 Status Bit |
| AutoGen405 | BOOL | `DB0012_DBX00010.06` | "HMI_DB".LOADER_LIFT_MOTOR_STATUS | FL Loader Lift - Motor M50.0 Status Bit |
| AutoGen406 | BOOL | `DB0012_DBX00027.06` | "HMI_DB".CONVEYOR_0_MOTOR_STATUS | FL Conveyor 0 - Motor M62.0 Status Bit |
| AutoGen407 | BOOL | `DB0012_DBX00027.07` | "HMI_DB".PUSHER_0_MOTOR_STATUS | FL Pusher 0 - Motor M62.2 Status Bit |
| AutoGen410 | BOOL | `DB0012_DBX00131.01` | "HMI_DB".SCREEN_CALL_1 | FL  HMI Call Screen 1 |
| AutoGen411 | BOOL | `DB0012_DBX00131.00` | "HMI_DB".SCREEN_CALL_0 | FL  HMI Call Screen 0 |
| AutoGen412 | BOOL | `DB0012_DBX00131.02` | "HMI_DB".SCREEN_CALL_2 | FL  HMI Call Screen 2 |
| AutoGen413 | BOOL | `DB0012_DBX00131.03` | "HMI_DB".SCREEN_CALL_3 | FL  HMI Call Screen 3 |
| AutoGen414 | BOOL | `DB0012_DBX00131.04` | "HMI_DB".SCREEN_CALL_4 | FL  HMI Call Screen 4 |
| AutoGen415 | BOOL | `DB0001_DBX00020.02` | "DB UTILITY".Pusher_1_Disable | Pusher 1 Disable |
| AutoGen416 | CHANNEL | `DB0001_DBW00020` | "DB UTILITY".word of BOOL bytes 20-21 (Pusher_0_Disable ... Conveyor_11_Disable) |  |
| AutoGen417 | BOOL | `DB0001_DBX00020.01` | "DB UTILITY".Elevator_Disable | Elevator Disable |
| AutoGen418 | BOOL | `DB0001_DBX00020.03` | "DB UTILITY".Conveyor_1_Disable | Conveyor 1 Disable |
| AutoGen419 | BOOL | `DB0001_DBX00020.04` | "DB UTILITY".Conveyor_2_Disable | Conveyor 2 Disable |
| AutoGen420 | BOOL | `DB0001_DBX00020.05` | "DB UTILITY".Conveyor_3_Disable | Conveyor 3 Disable |
| AutoGen421 | BOOL | `DB0001_DBX00022.05` | "DB UTILITY".Feeder_Lift_disable | Feeder Lift Disable |
| AutoGen422 | BOOL | `DB0001_DBX00022.04` | "DB UTILITY".Conveyor_23_Disable | Conveyor 23 Disable |
| AutoGen423 | BOOL | `DB0001_DBX00022.06` | "DB UTILITY".Feeder_Fingers_disable | Feeder Fingers Disable |
| AutoGen424 | BOOL | `DB0001_DBX00020.06` | "DB UTILITY".Conveyor_4_Disable | Conveyor 4 Disable |
| AutoGen425 | BOOL | `DB0001_DBX00020.07` | "DB UTILITY".Conveyor_5_Disable | Conveyor 5 Disable |
| AutoGen426 | BOOL | `DB0001_DBX00021.00` | "DB UTILITY".Conveyor_6_Disable | Conveyor 6 Disable |
| AutoGen427 | BOOL | `DB0001_DBX00021.01` | "DB UTILITY".Conveyor_7_Disable | Conveyor 7 Disable |
| AutoGen428 | BOOL | `DB0001_DBX00021.02` | "DB UTILITY".Conveyor_8_Disable | Conveyor 8 Disable |
| AutoGen429 | BOOL | `DB0001_DBX00021.03` | "DB UTILITY".Conveyor_9_Disable | Conveyor 9 Disable |
| AutoGen430 | BOOL | `DB0001_DBX00021.04` | "DB UTILITY".Pusher_2_Disable | Pusher 2 Disable |
| AutoGen431 | BOOL | `DB0001_DBX00021.05` | "DB UTILITY".Conveyor_10_Disable | Conveyor 10 Disable |
| AutoGen432 | BOOL | `DB0001_DBX00021.06` | "DB UTILITY".Pivot_Disable | Pivot Disable |
| AutoGen433 | BOOL | `DB0001_DBX00021.07` | "DB UTILITY".Conveyor_11_Disable | Conveyor 11 Disable |
| AutoGen434 | BOOL | `DB0001_DBX00022.00` | "DB UTILITY".Conveyor_12_Disable | Conveyor 12 Disable |
| AutoGen435 | BOOL | `DB0001_DBX00022.01` | "DB UTILITY".Conveyor_13_Disable | Conveyor 13 Disable |
| AutoGen436 | BOOL | `DB0001_DBX00022.02` | "DB UTILITY".Conveyor_21_Disable | Conveyor 21 Disable |
| AutoGen437 | BOOL | `DB0001_DBX00022.03` | "DB UTILITY".Conveyor_22_Disable | Conveyor 22 Disable |
| AutoGen438 | BOOL | `DB0001_DBX00020.00` | "DB UTILITY".Pusher_0_Disable | Pusher 0 Disable |
| AutoGen511 | CHANNEL | `DB0012_DBW00168` | "HMI_DB".WORD_PACKET_LENGTH | WD Actual Packet Length mm |
| AutoGen562 | CHANNEL | `DB0012_DBW00170` | "HMI_DB".DELAY_DISPLAY_7 | WD HMI Flipper 7 Delay Display |
