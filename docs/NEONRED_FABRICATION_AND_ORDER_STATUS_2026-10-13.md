# NEONRED fabrication and one-click BOM status — 2026-10-13

## Verdict

**Not ready for fabrication or one-click parts ordering.** EasyEDA's live Design Manager showed 0 DRC errors and 198/198 nets, but the generated fabrication files conflict with the 2-layer board setup, and the BOM is incomplete. DRC success alone does not establish an electrically safe, mechanically verified design.

## Fresh live exports

- [PCB source JSON](../PCB/NEONRED-live-PCB-source-review-2026-10-13.json), exported from the live `PCB_neonred` document on 2026-10-13. It contains 1,181 shapes, including 170 component footprints.
- [PCB BOM](../PCB/NEONRED-live-PCB-BOM-2026-10-13.csv), exported from the live EasyEDA BOM dialog.
- [Gerber review ZIP](../PCB/NEONRED-live-Gerber-review-2026-10-13.zip), generated 2026-10-13. This is a review artifact, **not a release package**.

No electrical/placement change was made in EasyEDA during this review. The `savecopy` document was not edited.

## Blockers

1. **Copper-layer stack mismatch.** EasyEDA's fabrication preview reports a 2-layer board, 90 × 180 mm. The fresh source contains 60 tracks on layer ID 34 (Inner14), one track and a copper area on layer ID 21 (Inner1), in addition to TopLayer and BottomLayer. The Gerber ZIP contains non-empty `Gerber_InnerLayer1.G1` and `Gerber_InnerLayer14.G14`. A 2-layer fabrication order cannot consume those inner copper files. Making the board 16-layer just to preserve two used inner layers is not a suitable silent fix; the stack must be intentionally specified, or the inner-layer routes must be converted/rerouted to the intended manufacturable stack and rechecked.

2. **One-click BOM is still not order-ready.** The live BOM has 72 grouped rows / 170 footprints. The exported EasyEDA CSV has 70 rows with no supplier part number. After the user signed in, LCSC's match scan showed **3 exact matches, 7 partial matches, and 62 unmatched rows**. The partial candidates are not safe assignments: they include a 0603 ceramic part for a through-hole 10 µF capacitor, a bare nRF24L01 IC for a module/header footprint, a Pi Zero W instead of the owned Pi Zero 2 W, and unrelated connector/header/fuse/panel-entry/tact-switch parts. The Bourns encoder (C143789) and Vishay TSOP38238 receiver (C141632) match the named part, subject to footprint/pad review. A subsequent Q1 pad-net check confirmed the suggested HXY 2N2222A (C20616319) pin order conflicts with the board's pad mapping, so it must not be assigned. **No suggested matches were accepted, and no parts were added to cart or ordered.** The imported Proxmark section contributes 55 grouped rows and is not a verified, buildable Proxmark revision. Its FPGA/MCU/analog/RF BOM, antenna coils and tuning are unresolved; assigning generic matches by value/package would risk creating a misleading order list. Draft/verify-before-fab footprints also remain. The reviewed supplier candidates and holds are recorded in [the dated corrected BOM review](../PCB/NEONRED-corrected-BOM-review-2026-10-13.md).

3. **LCSC matching is accessible, but mostly unresolved.** The signed-in one-click BOM result is available in the LCSC project `BOM_neonred_PCB_neonred_2026-10-13`. Its current provisional total of $78.86 reflects the seven partial selections shown by LCSC; it is **not a reliable project cost** because those candidates do not match the uploaded packages/functions. The unmatched rows include the Proxmark block and many external-module or custom-footprint entries that should be excluded from the assembled carrier-board order or sourced from the correct module/vendor. No checkout or purchase was made.

4. **Electrical power and system completeness remain unverified.** The PCB does not provide a validated power tree for the Pi, USB hub and peripherals. Prior load planning indicated a provisional 4–5 A at 5 V target across separate protected branches, not a measured load. The Pi header pins are represented as isolated `PI1_*` nets on this carrier, and the integrated Proxmark power/USB/RF implementation has not been validated. Do not power the board or order it as a finished integrated design.

## What is needed to release fabrication files

- Resolve whether this is a 2-layer redesign or an intentionally specified multilayer board. Preferred route: keep the intended low-cost stack and reroute/remove internal-layer geometry only after reviewing those 61 traces and the Proxmark source.
- Confirm whether the integrated legacy Proxmark circuit is still in scope. If yes, verify its exact hardware revision, source schematic/BOM, full antenna coils and tuning before placing codes or claiming it works.
- Replace draft/unknown footprints with manufacturer footprints, confirm their pad sizes/pitch/polarity, then assign exact supplier part numbers. External modules (Pi, LILYGO, radio modules) should be clearly separated from parts actually assembled onto the carrier.
- Define the Pi/HAT/USB/peripheral power and ground tree, branch protection, connector wiring and measured current budget. Check trace widths against copper weight and actual current.
- Re-run DRC after the above changes; inspect all Gerber layers/drills and board outline at scale; then export a fresh release Gerber ZIP and BOM.
- Complete a reviewed source list with exact manufacturer numbers and matching footprints, then update EasyEDA component supplier fields. Re-run the LCSC handoff and confirm that the matched and unmatched rows reflect the actual carrier-board assembly. Stop before checkout/payment unless explicitly directed to order.

## References checked

- [LCSC FH CT4-0805B104K500PF3 / C507069](https://www.lcsc.com/product-detail/C507069.html): 100 nF, 50 V X7R, 5.08 mm through-hole pitch.
- [LCSC Panasonic EEA-GA1V100 / C1579616](https://www.lcsc.com/product-detail/C1579616.html): 10 µF, 35 V electrolytic, 5 × 7 mm body, 2 mm pitch.
- [LCSC Vishay TSOP38238 / C141632](https://www.lcsc.com/product-detail/C141632.html): SIP-3 2.54 mm IR receiver.
- [LCSC Vishay TSAL6200 / C55528](https://www.lcsc.com/product-detail/C55528.html): 940 nm IR LED.
