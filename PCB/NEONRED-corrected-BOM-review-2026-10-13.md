# NEONRED corrected BOM review — 2026-10-13

## Result

The current live board BOM has 72 grouped rows representing 170 footprints. The full exported BOM remains [NEONRED-live-PCB-BOM-2026-10-13.csv](NEONRED-live-PCB-BOM-2026-10-13.csv); its earlier supplier crosswalk is [NEONRED-order-parts-crosswalk-2026-10-12.csv](NEONRED-order-parts-crosswalk-2026-10-12.csv). This review adds candidate catalog matches for the carrier-board items in [NEONRED-corrected-BOM-candidates-2026-10-13.csv](NEONRED-corrected-BOM-candidates-2026-10-13.csv).

**The BOM is more accurate, but is still not ready for one-click ordering.** These are candidates pending footprint and electrical checks. No EasyEDA supplier fields were changed, no candidate was accepted in LCSC, and nothing was added to a cart.

## Carrier-board candidates

| Function / refdes | Proposed order part | Review |
|---|---|---|
| 100 nF bypass, C1/C2/C5 (3 total) | FH CT4-0805B104K500PF3, LCSC C507069 | Through-hole, 100 nF X7R 50 V, 5.08 mm pitch. Verify the body's dimensions and PCB drill before assignment. [LCSC listing](https://www.lcsc.com/product-detail/Multilayer-Ceramic-Capacitors-MLCC-Leaded_FH-Guangdong-Fenghua-Advanced-Tech-CT4-0805B104K500PF3_C507069.html) |
| 940 nm emitter, D1 | Vishay TSAL6200, LCSC C55528 | 5 mm through-hole emitter; check pad polarity and that the LED faces out through the intended side opening. [LCSC listing](https://www.lcsc.com/product-detail/C55528.html), [Vishay datasheet](https://www.vishay.com/docs/81010/tsal6200.pdf) |
| 1 kΩ axial resistor, R1 | VO CR1/4W-1K±5%-ST52, LCSC C2894660 | 250 mW, 2.7 × 6.2 mm body. Listed in 100-piece multiples; board needs one. The board footprint is marked draft and has a 7.62 mm pitch, so verify its drill before assignment. [LCSC listing](https://www.lcsc.com/product-detail/C2894660.html) |
| 100 Ω axial resistor, R2 | VO CR1/4W-100Ω±5%-ST52, LCSC C2894648 | 250 mW, 2.7 × 6.2 mm body. Same MOQ and draft-drill concern as R1. Recheck pulse current through D1 and transistor drive before validating this value. [LCSC listing](https://www.lcsc.com/product-detail/C2894648.html) |
| IR receiver, U3 | Vishay TSOP38238, LCSC C141632 | Correct 38 kHz receiver candidate. Datasheet pin order is 1=OUT, 2=GND, 3=VS; map those functions to the PCB pads and confirm the enclosure opening. [LCSC listing](https://www.lcsc.com/product-detail/C141632.html), [Vishay datasheet](https://www.vishay.com/docs/82491/tsop382.pdf) |
| 10 µF capacitors, C3/C4 (2 total) | Lelon SJA100M1VBK-0507, LCSC C134710 | 10 µF, 35 V radial, 5 × 7 mm body and 2 mm pitch, matching the source model. LCSC listed it as an in-stock alternative (MOQ 10; price shown about $0.0503). Panasonic EEA-GA1V100 C1579616 has the same geometry but is out of stock. Confirm exact listing and capacitor polarity before assignment. [Lelon datasheet / listing](https://item.szlcsc.com/146020.html), [Panasonic listing](https://www.lcsc.com/product-detail/C1579616.html) |
| Encoder, SW1 | Bourns PEC11R-4015F-S0024, LCSC C143789 | Exact MPN match; still compare the full mechanical drawing and pad mapping with the actual board footprint. [LCSC listing](https://www.lcsc.com/product-detail/C143789.html) |
| Five THT buttons, MENU/BACK/UP/DOWN/ENTER | HCTL TC-6610-13-260G, LCSC C2845268 | 6 × 6 mm THT, 4.5 × 6.5 mm pin pitch matches the board footprint pitch; 13 mm actuator height needs case/travel review. LCSC MOQ is 10 while the board uses 5. [LCSC listing](https://www.lcsc.com/product-detail/tactile-switches_hctl-tc-6610-13-260g_C2845268.html) |

The live BOM's ID 68/69 switch text appears reversed: it names designator MENU as “BACK button” and designator BACK as “MENU button.” The candidate file preserves both live values and flags the mismatch. Confirm which physical switch should be menu/back, then correct the BOM labels or refdes in EasyEDA.

## Must remain blocked

- **Q1 is not orderable from the current footprint/net assignment.** The PCB nets are pad 1 = IR_BASE, pad 2 = IR_LED_K, pad 3 = GND. The LCSC-suggested HXY 2N2222A C20616319 pin order is 1=E, 2=B, 3=C, which does not match. Do not use that match. Correct the schematic/footprint mapping first, then choose a transistor whose verified pinout and current rating suit the IR pulse load. [Suggested 2N2222A datasheet](https://datasheet.lcsc.com/lcsc/2410121838_HXY-MOSFET-2N2222A_C20616319.pdf)
- **Proxmark rows 1–55 remain design hold.** They are grouped parts from an imported legacy reference circuit. The exact Proxmark revision, verified schematic, RF coil geometry/tuning, and buildability have not been established. Do not turn these generic values/packages into supplier assignments yet.
- **Pi, LILYGO board, and nRF24 breakout modules** are complete external modules rather than carrier-board assembly parts. Record the exact owned/selected board revisions and source them separately; do not match their outline footprints to bare ICs. The LCSC false partials included a Pi Zero W for the Pi Zero 2 W and a bare nRF24 IC for a module footprint.
- **The footprint and schematic checks are not complete.** Candidate part numbers do not repair draft footprints, verify the IR LED net/current design, or establish a safe board power design. The PCB fabrication report still has a copper-stack mismatch and other release blockers; see [NEONRED fabrication and order status](../docs/NEONRED_FABRICATION_AND_ORDER_STATUS_2026-10-13.md).

## Sourced package facts

- C507069 is listed as 100 nF X7R 50 V leaded, 5.08 mm pitch: [LCSC listing](https://www.lcsc.com/product-detail/Multilayer-Ceramic-Capacitors-MLCC-Leaded_FH-Guangdong-Fenghua-Advanced-Tech-CT4-0805B104K500PF3_C507069.html).
- C134710 is Lelon SJA100M1VBK-0507, 10 µF 35 V in the 5 × 7 mm radial body family: [LCSC part listing](https://item.szlcsc.com/146020.html), [manufacturer datasheet](https://datasheet.lcsc.com/lcsc/2501141801_Lelon-SJA100M1VBK-0507_C134710.pdf). Its 2 mm lead pitch and body must match the board's capacitor footprint; retain the current polarity check.
- C2845268 is a 6 × 6 mm four-pin THT switch with 13 mm height; the five-switch build quantity is below the listed MOQ 10: [LCSC listing](https://www.lcsc.com/product-detail/tactile-switches_hctl-tc-6610-13-260g_C2845268.html).
- Vishay's current receiver data sheet gives TSOP382 pinning as 1=OUT, 2=GND, 3=VS and dimensions 5.0 × 6.95 × 4.8 mm: [Vishay data sheet](https://www.vishay.com/docs/82491/tsop382.pdf).
- The 1 kΩ and 100 Ω resistors are listed as 250 mW through-hole, 2.7 × 6.2 mm body, with a 100-piece ordering multiple: [C2894660](https://www.lcsc.com/product-detail/C2894660.html), [C2894648](https://www.lcsc.com/product-detail/C2894648.html).
