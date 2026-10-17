# NEONRED LCSC and PCB order-readiness audit

Updated: 2026-10-15

## Current observed state

- The active EasyEDA project is `neonred`, PCB document `PCB_neonred`. The current board is configured as a **4-copper-layer PCB**. The live Design Manager showed **DRC Errors (0)** and **Nets (198/198)** during this review.
- A current 4-layer JSON export is [NEONRED-live-PCB-source-2026-10-15-4-layer-bridge-DRC0.json](../PCB/NEONRED-live-PCB-source-2026-10-15-4-layer-bridge-DRC0.json). This records the GND via/track bridge. The active live board remains the source of truth; confirm it has not changed since the export before generating fabrication files.
- The LCSC BOM page `BOM_neonred_PCB_neonred_2026-10-15` now shows **72 rows: 48 exact matches, 4 partial matches, and 20 unmatched**. The current page shows **0 items selected** and `$0.00` estimated total; nothing was added to cart or ordered.
- LCSC still flags duplicate items on lines **2, 3, 5, 7, 8, 10, 60, 61, and 72**. Resolve or intentionally consolidate these before treating the list as an orderable BOM.

## Supplier matches entered during this pass

These candidates were entered in the LCSC BOM and saved. “Exact” describes the catalog identity/package match only; it does **not** prove that the live PCB footprint, pin mapping, circuit design, or assembly process is validated.

| Part | LCSC candidate | Review note |
|---|---|---|
| 940 nm IR emitter | C55528, Vishay TSAL6200, 5 mm THT | The PCB D1 footprint is still a mismatch risk: its 10 mm pad spacing and 1.6 mm drills do not match the usual 2.54 mm LED lead pitch. Do not place for assembly until corrected. |
| Spartan-II FPGA | C1551453, XC2S30-5VQ100I, VQFP-100 | Device/package identity identified; imported Proxmark reference circuit is not yet validated as a buildable design. |
| Quad op amp | C184090, TI MCP6294-E/ST, TSSOP-14 | Catalog/package match; still verify circuit pin use and electrical requirements. |
| ADC | C2670433, TI TLC5540IPWR, TSSOP-24 | Catalog/package match; still verify the Proxmark reference implementation. |
| Analog switch | C553191, TI CD4066BPWR, TSSOP-14 | Catalog/package match; verify signal/power implementation. |
| Proxmark MCU | C2980232, Microchip AT91SAM7S512B-AU, LQFP-64 10×10 mm | 512 KB MCU variant identified; source schematic currently labels `AT91SAM7S64`, so the schematic/BOM discrepancy must be resolved before ordering. |
| Dual MOSFET | C5346816, UMW IRF7307TR, SOP-8 | Dual N/P-channel part with matching family and package; verify the actual board symbol/footprint pin mapping before assembly. |
| Hirose 4-position connector | C598157, MQ172X-4PA(31) | Live partial corrected to a 4-position catalog item; verify exact land pattern before order. |
| Shrouded 2x10 header | C9039, BOOMELE 2.54-2*10P | Live partial corrected to a 2x10 2.54 mm through-hole shrouded header; verify drill, shroud and orientation. |

## Why the remaining rows are not forced to a match

The unmatched list includes the owned LILYGO display board (line 1), a DNP entry (line 19), and grouped/merged rows whose source no longer identifies the exact purchasable device. Examples include diode/LED variants, a 100 µF capacitor without confirmed voltage and lead dimensions, a 3.3 V regulator with unresolved part/pin assignment, generic logic and reset parts, a relay, Mini-B connector, test points, ferrite bead, and crystals without the required electrical values. The exact row list currently reported by LCSC is 1, 19, 23–26, 29–31, 33, 35–36, 38–39, 57–58, 63–66.

The four remaining partials are not approved for order: a bare NRF24L01 IC offered against a complete radio-module row; an older Pi Zero W against the owned Pi Zero 2 W; a fuse offered against a 1x6 header (C37208 is a likely candidate but was not entered); and Panasonic EVQQ1D06M, whose lifecycle and footprint require verification. The 4-position connector and 2x10 header suggestions were replaced with better catalog identities this pass. Owned external modules should be excluded from the **purchase/assembly** BOM, while remaining documented in the system BOM. See the new [gap and external BOM](NEONRED_ORDER_GAP_BOM_2026-10-15.md) and [CSV](../PCB/NEONRED-order-gaps-and-external-BOM-2026-10-15.csv).

## Fabrication and assembly status

The live DRC/net count is a useful CAD check, not a fabrication or electrical sign-off. The board is **not ready to order as an assembled PCB** yet. Outstanding blockers:

1. Resolve duplicate BOM rows and separate external/owned modules, DNP entries, and actual board-mounted components.
2. Correct the 4 remaining partial matches and identify actual part numbers for the 20 unmatched rows; do not use package-only guesses for analog, RF, power, or protection devices.
3. Fix the D1 emitter footprint and verify Q1 transistor pad-to-pin mapping. The existing D1/Q1 concerns can cause non-fit or incorrect operation even with a clean DRC.
4. Resolve the `AT91SAM7S64` versus `AT91SAM7S512B-AU` discrepancy and verify the integrated Proxmark circuit, USB, coils/antenna network, tuning and firmware against a specific reference revision. The imported circuit remains unvalidated.
5. Verify 4-layer stack construction with the selected board house, then run its design-rule/DFM checks and inspect Gerbers/drills. The board export and current layer stack should be confirmed as the same revision before release.
6. Complete the power-source/current budget, regulator and protection review, USB VBUS/backfeed checks, thermal checks, and physical fit. A PCB DRC does not simulate or establish these.
7. Confirm which parts EasyEDA/LCSC can actually assemble. The BOM includes through-hole components and complete modules, which must not be assumed to be included in SMT assembly.

No parts were selected for checkout, no order was placed, and no manufacturing release files were generated as part of this review.

## References for the entered candidates

- [LCSC C55528, Vishay TSAL6200](https://www.lcsc.com/product-detail/C55528.html)
- [LCSC C1551453, XC2S30-5VQ100I](https://www.lcsc.com/product-detail/C1551453.html)
- [LCSC C184090, MCP6294-E/ST](https://www.lcsc.com/product-detail/C184090.html)
- [LCSC C2670433, TLC5540IPWR](https://www.lcsc.com/product-detail/C2670433.html)
- [LCSC C553191, CD4066BPWR](https://www.lcsc.com/product-detail/C553191.html)
- [LCSC C2980232, AT91SAM7S512B-AU](https://www.lcsc.com/product-detail/C2980232.html) and [Microchip AT91SAM7S512](https://www.microchip.com/en-us/product/at91sam7s512)
- [LCSC C5346816, UMW IRF7307TR](https://www.lcsc.com/product-detail/mosfets_umw-youtai-semiconductor-co-ltd-irf7307tr-umw_C5346816.html) and [UMW datasheet](https://www.umw-ic.com/pdf/IRF7307TR)
