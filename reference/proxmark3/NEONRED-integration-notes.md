# NEONRED Proxmark3 schematic integration

Prepared 2026-10-10. Schematic only; existing NEONRED PCB and both savecopy documents are out of scope.

## Basis

- Local reference: `proxmark3.sch`, Eagle 6.4 XML, five sheets.
- Published reference location: https://github.com/Proxmark/proxmark3/blob/master/doc/proxmark3.sch
- MCU family datasheet: https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/6175s.pdf
- Hardware description: https://github.com/Proxmark/proxmark3/wiki/Hardware-Description

The prepared file retains reference wiring. `prepare-neonred.ps1` verifies all 620 explicit pin-to-net memberships against the original, accounting for renaming. This checks preparation, not EasyEDA conversion, physical operation, or electrical design correctness.

## Changes

- Prefix component references with PM3_ to avoid existing NEONRED designator collisions.
- Prefix internal signal and power net names with PM3_. Ground remains GND.
- Update the SAM7S64 symbol/model designation to AT91SAM7S512-AU, retaining the common 64-lead pin mapping.
- Add source, interface, and draft-status notes on all five sheets.
- Retain the USB device connector and its data/protection circuitry. Connect it to a Pi USB hub downstream port using a USB data cable. Pi GPIO pins are not USB data pins.
- Retain separate reference power rails; do not join PM3_3V3 to the LILYGO 3V3 supply.

## Required before release

- Audit EasyEDA import connectivity, multipart symbols, and package pin mappings.
- Resolve exact orderable parts and missing reference values, including both crystals.
- Review DNP/alternative population options; do not populate every alternative indiscriminately.
- Check USB power budget, regulator parts, and current requirements.
- Review legacy FPGA/ADC/analog component availability and supported firmware target.
- Verify LF/HF antenna design, tuning components, coil placement and metal/copper clearances.
- Complete footprints, ERC, layout, DRC, and physical tests in a separately authorized PCB stage.

This is a reference-based schematic draft, not a manufacturing release or a verified Proxmark3 Easy clone.
