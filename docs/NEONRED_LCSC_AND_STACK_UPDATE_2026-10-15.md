# NEONRED EasyEDA parts and stack update

> **Historical snapshot; superseded by [the 2026-10-15 LCSC and PCB order-readiness audit](NEONRED-LCSC-AND-PCB-ORDER-READINESS-2026-10-15.md).** This file records a prior 16-layer state and earlier LCSC match counts. The active PCB was later restored to four copper layers; use the linked audit and its 4-layer export for current status.

Date: 2026-10-15
Active EasyEDA project/document: `neonred` / `PCB_neonred`
The active project was edited. No `savecopy` document was opened or changed.

## Changes made

- Set the active board's copper-layer count to **16** in EasyEDA Layer Manager. The live routing uses Top (layer 1), Bottom (layer 2), Inner1 (layer 21), and Inner14 (layer 34). Leaving the board configured as 2-layer would omit routed copper from the fabrication stack. The 16-layer setting preserves the existing routes; it is a costly stack and must be included in any board quote. A lower-cost revision would move/reroute the Inner14 copper and then recheck the GND plane and vias.
- Saved the active EasyEDA board and exported a fresh EasyEDA JSON source: [NEONRED live PCB source, 16-layer stack](../PCB/NEONRED-live-PCB-source-2026-10-15-16-layer-stack.json).
- Ran EasyEDA DRC after the stack change: **0 DRC errors**; Design Manager shows **198/198 nets**.
- Exported the live 72-line grouped BOM with supplier fields: [NEONRED live EasyEDA BOM](../PCB/NEONRED-EasyEDA-live-BOM-2026-10-15-stack16.csv). It contains **38 populated supplier-part fields** and **34 blank**. Blanks are not filled with guesses where the device/package, fit, or module identity is unresolved.
- Created a purchase-only list with the **38 LCSC-sourced rows**: [filtered LCSC buy list](../PCB/NEONRED-LCSC-buy-list-filtered-2026-10-15.csv). It leaves out the owned/external LILYGO, Pi Zero 2 W, and complete NRF24L01 modules because they have no LCSC supplier assignment; they remain in the full design BOM for documentation.
- Consolidated repeated supplier codes into **33 unique catalog lines / 107 total units**, so five identical tactile switches and repeated capacitors are counted together: [consolidated buy list](../PCB/NEONRED-LCSC-buy-list-consolidated-2026-10-15.csv). The active EasyEDA BOM still lists the controls separately by their button labels.
- Sent the active BOM through EasyEDA’s **One-click Order Parts** flow to the signed-in LCSC account. The new LCSC match list reports 39 exact, 6 partial, and 27 unmatched rows. I cleared all automatically selected items; the page shows **0 selected**, and Add to Cart is disabled. No items were put in the cart and no order was submitted.
- The current uploaded list is [BOM_neonred_PCB_neonred_2026-10-14 in LCSC](https://www.lcsc.com/personalCenter/myProject/detail?id=319FB30C08CC28D743B552596026EA37). The owned modules are documented in the full BOM but are not in the consolidated buy list.

## Supplier-part fields retained in EasyEDA

Verified/value-and-package candidates include the Proxmark 0603/1210 passives, the five navigation switches (LCSC C2845268), the encoder (C143789), the TSOP38238 receiver (C141632), 100 nF through-hole capacitors (C507069), 10 µF radial capacitors (C134710), and the axial 1 kΩ/100 Ω resistors. Product codes and grouped designators are in the linked BOM.

Some matched items have purchase-quantity constraints: C507069 is currently backordered with a minimum/order multiple of 20, C134710 has a minimum/order multiple of 10, and the five C2845268 buttons are offered in multiples of 10. The BOM quantities are design quantities; the LCSC page will require pack multiples if those parts are purchased.

The automatic matcher also proposed **a bare Nordic NRF24L01 QFN IC** for each complete NRF24L01 module, and **a Raspberry Pi Zero W** for the owned Raspberry Pi Zero 2 W. Those are wrong substitutions and were left unselected. LILYGO and the Pi are external/owned modules, not LCSC assembly parts. D1 and Q1 remain without supplier assignment because the current footprints/pin mapping do not match the likely parts. Proxmark FPGA/MCU and custom/merged parts remain unmatched until their exact manufacturable variants and footprints are verified.

## Issues still visible in the live design

1. **The 16-layer stack is a configuration correction, not a low-cost redesign.** The existing board needs a board-house stackup matching the assigned inner layers. The 16-layer price and laminate construction have not been quoted.
2. **Pi/USB-HAT and system power interfaces remain incomplete or unverified.** A 0-error board DRC cannot validate the Pi connection, USB data path, 5 V distribution, source current, backfeed protection, cable loss, regulator margin, or thermal behavior.
3. **The integrated Proxmark circuit is still an imported, unvalidated design.** Exact variant/revision, substitutions, USB implementation, antenna coils/tuning, firmware, and power behavior need confirmation and bench testing.
4. **Q1 remains a pinout blocker.** Its board pad nets are `1=IR_BASE`, `2=IR_LED_K`, `3=GND`; the suggested 2N2222A part may not have that lead order. D1 still has 10 mm pad spacing and 1.6 mm drills, which do not fit the likely 2.54 mm-pitch 5 mm IR LEDs. Do not assemble those positions until the transistor mapping and LED footprint are corrected.
5. **Physical checks remain.** Confirm capacitor polarity/lead fit, receiver orientation, button height and pad layout, encoder layout, module clearances, antenna/coil clearance, mounting, and the apparent large 2D opening. The MENU/BACK BOM names appear swapped relative to designators and should be corrected before release.

## Next concrete steps

1. Get a quote for the 16-layer stack; if that is unacceptable, make a deliberate 4-layer reroute/remap revision and run DRC/airwire checks again.
2. Decide whether the Proxmark stays an integrated circuit or is replaced by a separate tested module; confirm all exact IC and coil part numbers before assigning the remaining PCBA parts.
3. Correct D1/Q1 footprints and the MENU/BACK labels, then export a new BOM and verify LCSC mappings again.
4. Complete the Pi/HAT/power wiring and check worst-case current and USB VBUS isolation.
5. Generate fabrication files only after the chosen layer stack, DFM, mechanical fit, and power checks are complete.

The live DRC is clean for the current CAD rules, but the open interface, power, component-fit, and Proxmark questions still need specific design/test work.
