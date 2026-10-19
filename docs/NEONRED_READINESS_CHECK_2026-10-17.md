# NEONRED PCB readiness check — 2026-10-17

## Decision

**Not ready to order, assemble, or power.** The live EasyEDA PCB was restored to its saved, DRC-clean baseline and saved successfully; a fresh live DRC reports **0 errors**. This is only a geometry-rule pass: Q1's board nets still do not match the selected transistor's physical pinout. Power capacity and physical fit also remain unverified. The screen was explicitly excluded from this review.

## Checks completed

- [x] Restored the reviewed `cyberdeck-completed` PCB source after the trial Q1 reroute introduced clearance faults; EasyEDA displayed **Saved successfully** for the restored revision.
- [x] Reran live EasyEDA DRC after saving: **0 errors**.
- [x] Confirmed the Design Manager reports **29/29 nets** and **36 components**.
- [x] Confirmed the active board outline is **210 × 110 mm** and uses **two copper layers**.
- [x] Confirmed four actual non-plated case-mount holes in the active source, each **3.2 mm diameter** for M3 clearance. These are drilled holes, not just drawing circles.
- [x] Verified SELECT is active-low on `ENC_SW`, in parallel with the rotary encoder push switch; encoder A is separate. Firmware cannot distinguish SELECT from the encoder push button.
- [x] Corrected the control-label layout: BACK and UP are on the upper row; MENU and DOWN are on the lower row; SELECT is beside its own switch; ENTER labels the encoder push. The display was not reviewed.
- [x] Reconciled the passives list: two discrete BSS138 MOSFETs are used instead of the redundant breakout; the five 100 nF capacitors are split by the PCB's 5.08 mm and 2.54 mm lead pitches.

## Issues still blocking release

1. **Q1 pinout is wrong for the selected transistor.** The saved board maps Q1 pad 1 to `IR_BASE`, pad 2 to `IR_LED_K`, and pad 3 to `GND`. The linked Diotec 2N2222A datasheet maps physical pins 1/2/3 to emitter/base/collector. Thus the board puts the IR base signal on the emitter, the LED cathode on the base, and ground on the collector. A trial remap/reroute created clearance violations, so it was discarded and the saved baseline restored. The IR driver must be rerouted to the selected part's actual E/B/C pins and pass DRC before Q1 is populated. Verify the LED current-limiting resistor and pulse current as part of that correction.
2. **Eleven footprints are still marked `DRAFT - VERIFY BEFORE FAB`:** five tactile switches, C9, D1, Q1, R5, R6, and U2. Confirm each exact part's pad pitch, body, height, polarity and orientation against its footprint before assembly.
3. **Power is not validated.** The board has `+5V_EXT` and `3V3_AUX` inputs, but the PCB source contains no copper pours/ground plane and no complete protected power supply. A zero-error DRC does not prove the Pi/HAT or peripherals can safely source the combined current. Confirm the power architecture, branch protection, wire/connector ratings, and regulator thermal/current margins; bench-measure the assembled loads before powering everything together.
4. **Mechanical fit is not confirmed.** The Chameleon and ALFA regions are reference outlines, and actual module/cable/antenna dimensions and enclosure clearances have not been checked. Verify the four case-hole positions against the printed case and check all standoffs, connectors, antenna swing, and cable bends physically.
5. **Screen excluded.** No screen fit, display wiring, or display compatibility confirmation is included.

## Artifacts

- Live-source snapshot: `PCB/PCB_cyberdeck-completed-live-DRC0-2026-10-17.json`
- Repair audit: `PCB/repair-audit-2026-10-17.json`
- Reconciled purchase BOM: `BOM_NEONRED_current_2026-10-17.csv`
- Prior Gerber/drill output: `outputs/Gerber_cyberdeck-completed_PCB_cyberdeck-completed_2026-10-17.zip`

The DRC result applies only to EasyEDA's configured geometry rules. A zero-error DRC does not validate a component's pinout, electrical behavior, power budget, fabrication footprint, or mechanical fit. The Gerber ZIP predates the final active save and must be regenerated after the Q1 correction and all release checks; do not use it to order this revision.
