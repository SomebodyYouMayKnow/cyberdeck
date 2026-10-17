# NEONRED live PCB, power, BOM, and PCBA-readiness audit

> Superseded for current EasyEDA layer/BOM state by [the Oct. 15 update](NEONRED_LCSC_AND_STACK_UPDATE_2026-10-15.md). This document remains the dated Oct. 14 snapshot; its two-layer-stack finding was addressed by configuring the active PCB as 16-layer, and its BOM match counts predate the latest upload.

Date: 2026-10-14
Active EasyEDA document: `PCB_neonred` in project `neonred`
Source checked: live PCB source download and live BOM export. Neither `savecopy` document was edited.

## Verdict

**This revision is not ready for fabrication or assembly.** EasyEDA currently reports **DRC Errors (0)** and **Nets (198/198)**. Those checks do not prove electrical behavior, power integrity, or that the generated fabrication data matches the configured stack.

The latest live export after the supplier updates is [NEONRED-live-PCB-source-2026-10-14-post-LCSC.json](../PCB/NEONRED-live-PCB-source-2026-10-14-post-LCSC.json). It contains 1,181 shapes and 170 footprints. The corresponding normalized BOM is [NEONRED-live-PCB-BOM-2026-10-14-post-LCSC.csv](../PCB/NEONRED-live-PCB-BOM-2026-10-14-post-LCSC.csv): 72 grouped lines representing 170 footprints. The part-by-part disposition is [NEONRED-assembly-BOM-review-2026-10-14.csv](../PCB/NEONRED-assembly-BOM-review-2026-10-14.csv).

## Findings

The board’s two nRF24 modules share `SPI_SCK`, `SPI_MOSI`, and `SPI_MISO`, while each has separate CE/CSN signals. Their exported supply pads are on `3V3` and `GND`. The IR receiver `U3` is mapped `1=IR_RX`, `2=GND`, `3=3V3`, consistent with the common TSOP382 function order, pending physical orientation check. The source also includes the encoder and navigation button nets.

The following block the design:

1. **Copper stack mismatch.** The live PCB source has 447 tracks on layer 1, 134 on layer 2, 60 on layer 34 (Inner14), and one on layer 21 (Inner1). Its GND copper areas are on layers 1, 2, and 21. The visible fabrication/order setup is two-layer. A two-layer order cannot fabricate the inner-layer copper as drawn. Either intentionally specify a qualified multilayer stack or remove/reroute all inner-layer geometry for a two-layer board, then export and inspect new Gerbers and drill files.

2. **Pi interface is not routed.** The PI1 footprint’s 40 numbered pads use isolated `PI1_n` nets. The board does not show a complete Pi-to-USB-HAT data connection, peripheral USB path, or validated Pi power feed. The module outline by itself does not make an electrical carrier interface.

3. **The Proxmark circuit is unverified.** 55 BOM groups are from an imported Proxmark reference circuit. Its exact hardware revision, reference design, part substitutions, FPGA/MCU packages, USB implementation, antenna coils/tuning, and power are not established. The project’s Oct. 9 goal document describes a complete removable Proxmark module, while this PCB contains a clone circuit. That scope conflict must be resolved. The lower-risk path described in the project goal is a mounted, tested Proxmark module connected over USB.

4. **Power source and distribution are not signed off.** The carrier does not have a verified complete power tree for the Pi, USB hub, and attached modules. The radio/IR `3V3` load is sourced from the LILYGO interface in this design, but the available regulator current margin and combined peak demand are not known. Branch protection, USB VBUS isolation, cable losses, track widths, and thermal limits have not been validated.

5. **Q1 remains electrically blocked.** Its PCB pad nets are `1=IR_BASE`, `2=IR_LED_K`, `3=GND`. The prior 2N2222A suggestion has a different pin order. Do not assign that part. Correct the symbol-to-footprint mapping, then calculate LED current and transistor drive for the intended pulse width/duty cycle.

6. **Footprint and mechanical verification remain.** Several footprints are draft/custom. The live `D1` IR LED footprint has two 1.6 mm drilled pads centered 10.0 mm apart, while the candidate Vishay TSAL6200 (LCSC C55528) specifies a nominal 2.54 mm lead pitch and 0.5 mm leads. It is therefore **not a fit** and is not assigned. Rebuild/re-route D1 with a verified through-hole IR LED footprint or select a real part whose drawing matches the existing pads. Also verify receiver orientation and case apertures, cap polarity and lead pitch, resistor drill sizes, button height, encoder drawing/pad map, all device clearances, and screws against manufacturer drawings or actual hardware. Live BOM rows for `MENU` and `BACK` appear to have the labels swapped. The PCB source contains four round mounting holes and a rectangular outline, but no explicit large board cutout object; the empty 2D area is not proven to be a physical cutout.

## Power estimate

This is a planning estimate, not a measurement or safe operating limit. Raspberry Pi guidance gives Zero-family models a recommended 5 V / 2.5 A supply; Raspberry Pi lists about 350 mA typical active current for Zero 2 W. LILYGO lists 90–230+ mA with Wi-Fi enabled. RTL-SDR Blog V4 lists 250–270 mA typical and its optional bias tee may add about 180 mA. ALFA’s official AWUS036ACS page does not state a current maximum; use roughly 0.5 A only as a conservative test allowance, not a vendor rating. Two PA/LNA nRF24 modules could add roughly 0.1–0.12 A each during transmit, depending on their exact board revision. An IR LED target around 20 mA is a provisional low-current design estimate only, after Q1/R2 are corrected.

Using Pi typical active current plus those estimates gives roughly **1.6 A at 5 V-equivalent** for the known active loads, or approximately **1.8 A** with the SDR bias tee enabled, before startup peaks, Proxmark, Chameleon, and conversion losses. This estimate has material uncertainty. Separately, size the Pi branch for its 2.5 A recommended supply and provide a protected peripheral branch. A **4–5 A total 5 V supply capacity** is a conservative starting design target for this full configuration, not a verified system draw. The Miady bank in the project notes is listed at 5 V / 2.4 A and is below the Pi’s 2.5 A recommendation by itself.

Waveshare lists the USB HUB HAT at 5 V and 65 × 30 mm; its product page does not specify a guaranteed combined USB-port current. The Wiki’s 3 A pogo-pin figure is a limit of that connection, not proof that the battery, cables, Pi, hub, and every device can safely provide that current together. Do not parallel two USB 5 V outputs. Measure the complete assembly on separate protected branches before relying on it.

## BOM and EasyEDA status

The review CSV has all 72 live BOM groups and gives a disposition for each. It separates carrier-board candidates from external modules and places the 55 Proxmark entries on hold. In the active EasyEDA PCB, C1/C2 and C5 now carry LCSC C507069, C3/C4 carry C134710, U3 carries C141632, and SW1 carries C143789. Live UI inspection confirms U3 has three 1.0 mm plated holes at 2.54 mm pitch; the earlier 0.5 mm-hole warning was incorrect. The TSOP38238 supplier match is mechanically plausible, but package orientation and assembly eligibility still need a final check. C3/C4 use 0.8 mm holes and 2 mm pitch; verify electrolytic polarity and exact lead clearance. C1/C2/C5 use 5.08 mm pitch and 0.5 mm drills; verify lead diameter. The EasyEDA handoff uploaded the live 72-group BOM to the signed-in LCSC account. The columns are now mapped and the BOM match list was generated: 3 exact, 7 partial, and 62 unmatched. Several partial results are demonstrably wrong-device/package substitutions; the list is not an approved parts list. No parts were added to cart and no order was submitted.

The current BOM has THT caps, IR parts, axial resistors, an encoder, and five through-hole buttons. JLCPCB supports selected THT/wave-solder assembly, but each exact part must be assembly-eligible and match footprint and placement; assigning an LCSC retail code alone does not select it for PCBA. The Pi, LILYGO, and radio modules are external assemblies and should not be mapped to bare ICs in the carrier PCBA BOM.

Q1 and the 55 Proxmark imported lines remain unassigned. C1/C2/C5 now have C507069 and C3/C4 have C134710 in the active PCB; U3 has C141632. Those supplier fields are not yet an approved assembly list: confirm drills/leads, capacitor polarity, receiver orientation, and current JLC assembly method. D1 is **not assigned**: candidate C55528 has 2.54 mm lead pitch, but D1's live pads are 10.0 mm apart with 1.6 mm drills. The C2845268 buttons remain candidates pending exact pad-map, height, and PCBA process verification. SW1 has exact C143789. Nothing was added to cart or ordered.

## Release path

1. Resolve whether Proxmark is a separate removable module or a validated, specific integrated design; remove the unverified clone if following the documented removable-module plan.
2. Decide on a real two-layer or specified multilayer stack and regenerate the source/Gerbers accordingly.
3. Complete the Pi, hub, USB, and power connections. Add appropriate branch protection and avoid VBUS backfeed. Check current-carrying copper against measured worst-case loads.
4. Correct Q1 and verify the IR driver, LED polarity, resistor values, and current.
5. Replace draft footprints and verify every component package, hole, edge clearance, silk, mounting location, and enclosure fit.
6. Clean the assembly BOM: exclude external modules and DNPs, select exact MPNs, verify JLC assembly availability including THT/wave options, and review the component-placement file.
7. Run fresh DRC and DFM checks, inspect all Gerber/drill layers, and bench-test power rails and modules before ordering.

## Sources

- [Raspberry Pi getting-started power guidance](https://www.raspberrypi.com/documentation/computers/getting-started.html) and [Pi hardware current table](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html).
- [LILYGO AMOLED-series current/pinout source](https://github.com/Xinyuan-LILYGO/LilyGo-AMOLED-Series).
- [RTL-SDR Blog V4 datasheet](https://www.rtl-sdr.com/wp-content/uploads/2024/12/RTLSDR_V4_Datasheet_V_1_0.pdf).
- [ALFA AWUS036ACS official product page](https://www.alfa.com.tw/products/awus036acs_1) (no maximum current listed).
- [Waveshare USB HUB HAT specifications](https://www.waveshare.com/product/raspberry-pi/hats/interface-power/usb-hub-hat.htm) and [USB HUB HAT Wiki](https://www.waveshare.com/wiki/USB_HUB_HAT_%28B%29).
- [Vishay TSAL6200 datasheet](https://www.vishay.com/docs/81010/tsal6200.pdf) and [Vishay TSOP382 datasheet](https://www.vishay.com/docs/82491/tsop382.pdf).
- LCSC candidates: [C507069 100 nF THT](https://www.lcsc.com/product-detail/C507069.html), [C55528 TSAL6200](https://www.lcsc.com/product-detail/C55528.html), [C141632 TSOP38238](https://www.lcsc.com/product-detail/C141632.html), [C134710 10 µF](https://item.szlcsc.com/146020.html), [C143789 Bourns encoder](https://www.lcsc.com/product-detail/C143789.html), [C2845268 button](https://www.lcsc.com/product-detail/tactile-switches_hctl-tc-6610-13-260g_C2845268.html).
- [JLCPCB PCBA FAQ](https://jlcpcb.com/help/article/pcb-assembly-faqs) describes selected THT/wave-solder parts; [EasyEDA Standard BOM guide](https://docs.easyeda.com/en/Schematic/Export-BOM/) describes the LCSC order-parts handoff.

## Signed-in LCSC matching run (October 14, 2026)

After the user signed in, the 72-row BOM was uploaded, its columns were mapped, and the LCSC match list was generated with the first component row included. The list reports **3 exact, 7 partial, and 62 unmatched**. It flags imported lines 60–61 as duplicate items. Catalog matching does not establish JLC assembly eligibility or manufacturing readiness.

- Exact text matches were Q1 (C20616319), SW1 (C143789), and U3 (C141632). Q1 is rejected because its lead order conflicts with the board pad nets. SW1's existing code was retained. U3's code is assigned to the active PCB_neonred. EasyEDA coordinates are in 10-mil units: the 10-unit pad spacing equals 2.54 mm, matching the Vishay pitch. The latest live PCB export instead shows 1.0 mm plated holes at 2.54 mm pitch, which is a plausible through-hole fit. Confirm receiver orientation and actual lead clearance before assembly; catalog footprint/assembly data alone does not verify the installed part.
- The seven partial suggestions were rejected: C3/C4 were offered a 0603 capacitor instead of through-hole; NRF24L01 a bare QFN IC instead of a complete module; PI1 a Pi Zero W instead of Zero 2 W; a Proxmark connector had an unverified contact count; two headers were offered duplicate fuses; and the imported Proxmark switch was matched to an SMD switch with an unverified land pattern.
- The other 62 rows had no automatic match. Most are generic THT descriptions, external modules, or components in the unverified Proxmark import. Do not use the LCSC auto-match list as a purchase- or assembly-ready BOM.

The latest live EasyEDA BOM with the current capacitor, U3 and SW1 supplier properties is [NEONRED-live-PCB-BOM-2026-10-14-post-LCSC.csv](../PCB/NEONRED-live-PCB-BOM-2026-10-14-post-LCSC.csv). The mapped LCSC result is saved in the account, but its seven partial suggestions include wrong package/device matches. I deselected all seven partial suggestions in LCSC; the live list now shows **0 items selected** and its add-to-cart action is disabled. Nothing was added to cart or submitted for purchase. Full assembly is still blocked by the unresolved PCB design and unmatched/held components.



### Verified catalog matches (Oct. 14)

- C507069 is a 100 nF, 50 V X7R, 5.08 mm pitch leaded capacitor; JLCPCB lists wave soldering and economic/standard PCBA. It is assigned to C1/C2/C5; check its leads against the footprint’s 0.5 mm drills.
- C134710 is 10 uF, 35 V radial, D5 x L7 mm, 2 mm lead spacing; pitch and body match C3/C4. The live footprint has 0.8 mm holes; confirm lead clearance and polarity.
- C55528 TSAL6200 is a 940 nm 5 mm IR LED with nominal 2.54 mm lead pitch and 0.5 mm leads. It does **not** fit exported D1 pads (10.0 mm pitch, 1.6 mm drills); do not assign it until D1's footprint is corrected and rerouted.
- C2845268 is a 6 x 6 mm, 13 mm high, four-pin through-hole SPST tactile switch, broadly matching the five navigation buttons; confirm exact pad pattern and case height.
- The active U3 assignment C141632 has three 1.0 mm plated holes at 2.54 mm pitch in the live PCB, which is a plausible mechanical fit. Confirm the receiver orientation against its data sheet and verify the selected assembly process.

These are supplier candidates, not a released assembly BOM. Live PCB parameters for C1/C2/C5, C3/C4 and U3 were updated; the fresh export and normalized BOM above contain those changes. The LCSC upload now exists in the signed-in account with columns mapped and match results generated. No cart or order was placed.
