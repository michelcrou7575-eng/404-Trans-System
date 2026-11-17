# 404 Trans-System (TS): functional specification and redesign plan

**Status:** DRAFT v0.1 (2026-11-17), written from the PLC code review (`CODE_REVIEW.md`) and the operator answers. **Every line marked ❓ needs your confirmation or correction.**
**Assumptions:** same PLC (CPU 315-2 DP, STEP 7 Classic, STL), same I/O and symbol table, same two HMIs (LAUER for production, OMRON NS12 for service). **Hardwired safety (E-stops, guard doors, light curtain safety relays) is out of scope** and stays as it is.
**Way of working:** trials **between shifts** only. Every change is a small block download with a **fallback switch or the previous block kept for immediate rollback**.

---

## 1. Line overview (as built)

| Pos | Station | Block | Main sensors | Main actuators | Role |
|---|---|---|---|---|---|
| 1 | Conveyor 0 + Pusher 0 | FC1012 | B35.2 height, B35.3/B35.4 | K62.0/1 belt, K62.2/3 pusher | Takes packets from the 2145 tuber, height check / eject, feeds the elevator |
| 2 | Elevator + Pusher 1 | FC1016 | P4.0–P4.5 | Parker VFD A63.x, brake A56.2, K42.6/7 | Lifts the packet, Pusher 1 pushes it onto C1 |
| 3 | C1 belt | FC1018 | B5.4, B5.5 | A43.0/1 | Cross belt to C2 |
| 4 | C2 angle belt + rollers | FC1022 | B5.5, B6.0, B6.1 | K43.4 belt, Y43.6 lift, K43.5 rollers | Centres the packet, turns it 90°, feeds slat C3 |
| 5 | C3 slat | FC1024 | B6.2 in, B6.4 out, encoder FM350 ch0 | A44.0/1 | Spacing / feeding of collator C4 |
| 6 | C4 collator | FC1031 | B6.7 in, B7.0 out, encoder ch2/3 | A44.3/4/5 | **Collates packets lengthwise** until "full" (surface count), then **one complete transfer** to C5 |
| 7 | C5 link | FC1034 | B7.0 in, B7.1 end | A45.0/1 | Buffer, transfers to C6 (+ auto re-sync run) |
| 8 | C6 flip delivery | FC1038 | B7.2, B7.3 | A45.3/4 | Delivers packets one by one to the flipper |
| 9 | C7 flipper | FC1042 | B7.4, B8.2, P8.0/8.1 | A45.6/7 belt, K46.0/1 flip | Flips the packet (selectable) |
| 10 | C8 turntable | FC1048 | B8.2, B9.6, P8.5/8.6/9.2/9.3 | A46.4/5 belt, A47.0/1/2 turn | Turns the packet (direction selectable) and delivers to C9 |
| 11 | C9 + Pusher 2 | FC1050 | B9.6, B9.7, P10.0/10.1, B10.3 | K47.5 rollers, K47.6/7 pusher | Positions the packet, Pusher 2 pushes it sideways onto C10 |
| 12 | C10 pivot collator | FC1054 | B10.4 in, B10.5 full, B10.6 exit, encoder ch4/5, P15.0/15.1 | A48.0/1, K53.0/1 pivot | **Collates packets widthwise** until "full", pivots HIGH/LOW, **one complete transfer** to C21 or C11 |
| 13–15 L | C11 → C12 → C13 (low) | FC1058/62/66 | B10.7, B11.0, B11.1, B11.2 | A48.3/4, A48.6/7, A49.0/1/2 | Link, link, delivery to the feeder (level 1) |
| 13–15 H | C21 → C22 → C23 (high) | FC1078/82/86 | B15.4, B15.5, B15.6, B15.7 | A53.4/5, A53.6/7, A54.0/1/2 | Same, level 2 |
| 16 | Feeder lift + fingers | FC1074/1070 | P11.4–P11.7, P13.1/13.2, P12.0/12.1, B12.3, B13.0 | A50.0/1/2/3, K50.5/6, Y50.4/7, Y51.3, A51.0/1 | Takes the load from C13 or C23 and presents it to the operator / **bottomer** |

❓ Please correct roles, positions and anything missing (e.g. what the feeder delivers to, and where the bottomer is).

---

## 2. Operating rules (to keep)

1. **Complete transfers only:** a station sends its load **only when the receiver is empty**, and it sends **all** of it.
2. **Collators:** C4 collates lengthwise and C10 widthwise. A collator transfers when "full" (sensor or encoder surface count), or when called during clearing.
3. **Pivot C10** alternates between high (C21) and low (C11) after each transfer.
4. **Delivery** C13/C23 → feeder; the operator controls the feeder (S2.6 ON/OFF, S3.4 hold, …).
5. **Order change:** see §4.
6. **Service:** each station can be jogged from the OMRON HMI (service pages 1/2/3). The station upstream is disabled while a station is in service.

❓ Anything else operators rely on?

---

## 3. Modes (target)

| Mode | Who selects | What runs |
|---|---|---|
| **Auto** | Control voltage ON (`M0.3`) | All station sequences |
| **Order change** (today: "Clearing") | LAUER F4 (later the HMI) | Feeding of TS stopped; old order runs out; new order held at C10 until S3.2 |
| **Service** (per station) | OMRON service pages | That station jogs; neighbours are disabled |
| **Hand feed** | LAUER / OMRON | Conveyor 0 reverse / manual feeding |

One **mode manager** block owns these bits, and every station reads them. No more spread-out `M140.3` / `M152.x` / `M190.x` mixing.

---

## 4. Order change: target behaviour (replaces today's clearing chain)

**Today:** global "stage cleared" flags `M10.1`–`M10.6` with timers (`Timer 128`, `T33`, `Timer 56`/`57`/`58`/`109`), and a separate new-order chain `M7.4`–`M8.3`. Fragile: §14 of `CODE_REVIEW.md`.

**Target: order tracking.** Every station keeps a small **load record**:

| Field | Meaning |
|---|---|
| `Order` | 0 = empty, otherwise the order number (A, B, … as a running number) |
| `Count` | Packets on the station (maintained by the transfer handshake) |
| `State` | Empty / Filling / Full / Transferring / Fault / Service |

**Rules:**
1. A new packet entering the TS takes the **current order number**. The 2145 / Conveyor 0 hand-off assigns it.
2. On a transfer, the receiver's load record **takes the sender's order number and count**, and the sender becomes empty.
3. **Transfer allowed only if** the receiver is Empty, **or** (for collators) holds the **same order**.
4. **Operator "order change" (F4):** the current order is closed, and feeding of the TS stops until all stations upstream of C10 hold the old order or are empty.
   - Every station holding the old order keeps running it **downstream**. C4 and C10 transfer even when not full ("close order" forces the transfer).
   - TS feeding of the **new** order restarts **as soon as C1–C9 are empty of the old order**, which is what operators expect today.
   - **C10 may not collate a new-order packet while it holds old-order packets.** It must transfer them first. That makes the "packets left on C10" problem impossible.
   - C10 **holds** the new order until no station downstream (C11–C23, feeder) holds the old order, then **always** asks for **S3.2**. After S3.2 it continues with the new order.
5. Every wait has a **timeout with a named alarm** on both HMIs. Nothing switches off silently.

❓ How is an order identified today: only by the F4 moment, or is there an order number from the 2145 / bottomer?

---

## 5. Standard station block (target)

One **FB "TS_STATION"** with one instance DB per station (or one DB of instances). Every station gets the same behaviour:

- **Step chain:** Empty → Filling → Full → Transferring → Empty, plus Fault and Service.
- **Handshake** to its neighbours, all in the instance DB, with no free M bits:
  - `Ready_To_Receive` (I am empty)
  - `Request_Send` (I am full / order closed)
  - `Transfer_Run`
  - `Transfer_Done`
- **Counting** from the station's own in/out sensors with debounce and U-shape tolerance (FC8 v0.7 logic). The count moves with the load on transfer.
- **Timeouts** per step → alarm number (no silent register reset).
- **Interlocks:** reversing outputs always cross-locked; VFD ready (`M11.1`) gating; door / safety-relay states as enable inputs.
- **Station-specific parts** (pusher, pivot, flipper, turntable, elevator, collator surface counting) stay in small FCs called by, or calling, the standard FB.

---

## 6. HMI and alarms (target)

- One **HMI interface DB** per HMI (keep DB12 `HMI_DB` / DB22 `HMI DB NEW` layouts where possible, so the HMI projects change little).
- One **alarm word list**: every timeout and fault has a number and a text on both panels. Example: "C4 clearing timeout", "C10 not empty at order change", "S3.2 waiting".
- An **"Order change" status** on the HMI: which stations still hold the old order.

---

## 7. Migration plan: trials between shifts

Each trial: **one small download, done between shifts, with an immediate rollback** (a fallback switch bit, or the previous block kept as a copy in the project).

| Phase | What | Trial between shifts | Rollback |
|---|---|---|---|
| **0 (now)** | Fixed `CONVEYORS CLEARING` (FC1011): `T33_DN`, C10 proven empty, S3.2 always | Download **FC1011 only**, while clearing is **off** (`M10.0` = 0). Then run a clearing with **C4 empty** (see below) | Re-download the saved old FC1011 |
| 0b | FC1208 + FC8 counter (`M333.3`) | Set `M333.3` = 1, watch one C4 collate + transfer | `M333.3` = 0 |
| 1 | Specification agreed (this document) | none | none |
| 2 | Standard FB + order tracking, tested in **PLCSIM** with a simulated line | none (office) | none |
| 3 | One simple station (e.g. C12/C22 link) moved to the FB, with a switch old/new | 1 shift change per station | Switch back to the old FC |
| 4 | Other link/delivery stations, then C5/C6 | 1 per shift change | Switch |
| 5 | Collators C4/C10 + order change on the new logic | Planned trial at a real order change | Switch |
| 6 | Remove old FCs, final alarm/HMI cleanup | none | none |

**Phase 0 trial (FC1011), about 15 min:**
1. Save the current online FC1011 (upload it into a backup project) so you can roll back.
2. With clearing **off**, download the new FC1011.
3. With C4 **empty** and packets on C10, start a clearing (F4).
4. Watch in a VAT: `M10.2` → `M10.3` within ~20 s (not 30 s) → … → `M10.6` → `M8.4`/`M8.5` → the S3.2 lamp.
5. C10 must be **empty** before clearing ends.
6. If anything is wrong: re-download the old FC1011.

---

## 8. Open questions (needed before phase 2)

1. ❓ How long is the window between shifts (minutes)? Can conveyors run empty during it?
2. ❓ Order identity: only F4, or an order number from the 2145 / bottomer?
3. ❓ Conveyor lengths and speeds (C4, C10, links) and the packet length/width range.
4. ❓ Is a later move to S7-1500 / TIA planned? (It changes how the FB is written.)
5. ❓ Is the LAUER panel to be retired after the OMRON HMI is validated?
6. ❓ The missing block sources (FC2, FC3/5/9, OB35, OB100, FC245, DB2/3/10/12/14/22/50) are needed to finish the specification.
