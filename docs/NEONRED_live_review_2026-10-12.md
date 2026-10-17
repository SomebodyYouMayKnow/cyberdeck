# NEONRED live PCB review — 2026-10-12

**Verdict:** The control/radio portion is plausibly wired, but the complete cyberdeck is **not yet verified to work or safe to order/power**. EasyEDA reports 0 DRC errors under its current rules; this is a geometric check, not a complete electrical or power test.

## Evidence checked

- Re-exported the open `PCB_neonred` from EasyEDA to [`PCB/NEONRED-live-PCB-review-2026-10-12.json`](../PCB/NEONRED-live-PCB-review-2026-10-12.json). Its 1,181 shapes are identical to the 2026-10-11 DRC0 export: 170 footprints, 643 tracks, 334 vias, five copper areas. The live Design Manager displayed **DRC Errors (0)** and **Nets (198 / 198)**.
- The configured minimum track width is **0.203 mm** (0.7992 EasyEDA internal units). **522 of 643 track objects are below 0.254 mm**. Thus the 0-DRC result does not establish that all traces satisfy a 0.254 mm fabrication rule or can carry their actual peak currents. Ground and 3.3 V signal traces are as narrow as 0.203 and 0.254 mm, respectively; no thermal/current/voltage-drop calculation is embedded in DRC.
- All five copper areas are assigned **GND**. The added BottomLayer area (`gge70409`) covers the controls/Pi-to-Proxmark transition and overlaps the original Proxmark BottomLayer GND area. It is not a 3.3 V or 5 V feed. The ESP32 module A1 has five pads labelled GND. Its lower GND pads connect by existing GND tracks to the navigation buttons/encoder GND pads, which lie inside the added pour. This shared ground is intentional in principle and DRC shows no copper-to-other-net short. Its RF-return geometry still needs inspection in Gerbers and on hardware. The Pi footprint `PI1` has **no pad assigned to GND**: all 40 header pads are isolated `PI1_*` nets, so the pour does not connect the Pi through this carrier footprint. An external USB cable may share ground in the assembled system, but the board export cannot verify that cable.

## Static interface check

| Circuit | Exported pad/net finding | Assessment |
|---|---|---|
| Two nRF24L01 modules | Both have VCC on `3V3`, GND on `GND`, and shared `SPI_SCK`, `SPI_MOSI`, `SPI_MISO`; their CE/CSN nets are separate. | Logical connection is plausible for independent radios, including overlapping transmissions after separate configuration. **3.3 V supply capacity for PA/LNA variants is unverified.** The `3V3` rail comes from the LILYGO module rather than a separately rated peripheral regulator. |
| Encoder and navigation keys | A/B/switch and button nets have separate ESP32 inputs; common terminals connect to GND. | Plausible with firmware pull-ups and debounce; hardware/pin assignment and shaft/button mechanics need test. |
| IR receiver | `U3` has `IR_RX`, `GND`, and `3V3` pads. | Power/data nets are present. LED driver polarity/current and optical placement still need bench check. |
| Pi Zero 2 W | All 40 `PI1_*` header pads remain isolated from carrier nets. | No power/data/GND connection via this PCB footprint. Pi must be powered and USB-connected separately. |
| Integrated Proxmark reference | Mini-B `PROXSV1` exposes `USB_D+`, `USB_D-`, VBUS (`N$1`) and GND. Antenna connector `PROXSV2` carries `ANT_LO`/`ANT_HI`; its antenna coils/tuning are absent. | Imported legacy reference is **not a validated Proxmark build**. Complete LF/HF coils, exact revision/BOM, firmware/FPGA programming, RF tuning and Pi USB cable are still needed. |
| Power architecture | Proxmark `+3V3`, FPGA rail, and ESP32/radio `3V3` are distinct supply nets; GND is common. Pi/HAT, ALFA, SDR and Chameleon are not represented as a complete wired power tree. | No proof that one bank or the off-board HAT can power every load. Do not inject a second USB 5 V source into the HAT without a documented isolation design. |

## 5 V load planning calculation

This is a **supply-sizing estimate**, not measured current and not a sum of every device's recommended power-supply rating. The 5 V equivalents for 3.3 V devices assume 85% conversion efficiency; the present PCB does **not** implement that independent converter.

| Load | 5 V equivalent used | Basis |
|---|---:|---|
| Pi Zero 2 W | 0.35 A | Raspberry Pi's listed typical active board current; peaks can be higher. |
| Waveshare HAT FE1.1S hub controller | 0.10 A | Chip brief at four ports enabled; excludes USB peripherals and other HAT circuitry. |
| LILYGO T-Display-S3 AMOLED | 0.23 A | Vendor's 90–230+ mA Wi-Fi-on range; **230 mA is not a maximum**. |
| RTL-SDR V4L Lite | 0.27 A | Proxy from the predecessor V4 datasheet; the V4L current has not been independently verified. |
| ALFA AWUS036ACS | 0.50 A | Planning reservation only; ALFA does not publish a reliable maximum in the located product specs. |
| Proxmark USB circuit | 0.50 A | Conservative USB full-configuration allowance from the Proxmark reference; actual board current unmeasured. |
| Chameleon over USB/charging | 0.50 A | Conservative reservation only; omit this branch if it runs independently on battery/Bluetooth. |
| Two PA/LNA radios | 0.23 A | Placeholder: 2 × 0.15 A at 3.3 V, converted to 5 V at 85%. **Verify exact radio modules' TX pulse currents.** |
| IR transmit | 0.02 A | Placeholder averaged/rounded 5 V equivalent; verify pulse current and duty cycle. |
| **Provisional running allowance** | **2.70 A / 13.5 W** | Includes substantial assumed values, excludes startup peaks, cables, extra HAT circuitry, SDR bias tee and charger load. |

**Planning target:** choose a protected power system with roughly **4–5 A of simultaneous 5 V output (20–25 W)** across properly isolated branches, with a Pi branch capable of its vendor-recommended input and a separately rated USB-peripheral branch. This is headroom, not predicted normal draw. The old Miady 5 V/2.4 A bank rating is below this estimate. The plain Waveshare 4-port USB HUB HAT lists 5 V operation but does not guarantee the aggregate downstream current needed here. Its published setup attaches the HAT to the Pi GPIO connector as well as USB; when mounting it beside the Pi, verify how the HAT receives 5 V and GND. A micro-USB link alone is not proof that the four ports can supply all devices.

## EasyEDA “Order Parts” status

The live **PCB BOM** export is [`PCB/NEONRED-live-PCB-BOM-2026-10-12.csv`](../PCB/NEONRED-live-PCB-BOM-2026-10-12.csv): **72 grouped rows covering 170 footprints; only two rows have supplier codes** (`C1/C2: C19355` and `SW1: C143789`). The `C19355` listing could not be confirmed in the current LCSC search, so treat it as unverified. EasyEDA's library search did not return the exact known 10 µF Panasonic listing by LCSC code. I did **not** populate unsupported numbers or change the live supplier metadata.

The annotated [`PCB/NEONRED-order-parts-crosswalk-2026-10-12.csv`](../PCB/NEONRED-order-parts-crosswalk-2026-10-12.csv) records verified catalog **candidates**, still requiring footprint/pinout review: 100 nF 5.08 mm C507069, 10 µF C1579616, IR LED C55528, IR receiver C141632, and the existing encoder C143789. Of the 72 groups, **55 are the unvalidated imported Proxmark section**, **3 are externally purchased modules**, and **8 more are unassigned**. No one-click LCSC purchase can legitimately resolve all 170 parts until every Proxmark component is specified and checked; complete boards such as the LILYGO and Pi are purchased outside this PCB assembly BOM. The separate purchase list now uses a 5.08 mm 100 nF candidate because the former 2.54 mm KEMET lead spacing did not match the live `C1/C2/C5` footprints.

## References

- [EasyEDA copper area and GND-net behavior](https://docs.easyeda.com/en/PCB/Copper-Pour/index.html)
- [EasyEDA BOM and LCSC assignment behavior](https://docs.easyeda.com/en/Schematic/Export-BOM/)
- [Raspberry Pi computer power table](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html)
- [LILYGO AMOLED series current table and pinout](https://github.com/Xinyuan-LILYGO/LilyGo-AMOLED-Series)
- [Waveshare USB HUB HAT product/setup](https://www.waveshare.com/product/iot-communication/wired-comm-converter/usb-hub-hat.htm)
- [FE1.1S hub controller brief](https://files.waveshare.com/upload/4/4d/FE1.1s_Product_Brief_%28Rev._1.1%29.pdf)
- [RTL-SDR V4 datasheet used as V4L load proxy](https://www.rtl-sdr.com/wp-content/uploads/2024/12/RTLSDR_V4_Datasheet_V_1_0.pdf)
- [RTL-SDR V4L product](https://www.rtl-sdr.com/product/rtl-sdr-blog-v4l-lite-r828s-rtl2832u-1ppm-tcxo-sma-software-defined-radio-dongle-only/)
- [ALFA AWUS036ACS manufacturer specifications](https://www.alfa.com.tw/products/awus036acs_1)
- [Original Proxmark hardware/power description](https://github.com/Proxmark/proxmark3/wiki/Hardware%20Description)
- [Waveshare plain HAT installation](https://www.waveshare.com/wiki/USB_HUB_HAT)
- [LCSC 100 nF 5.08 mm candidate](https://www.lcsc.com/product-detail/C507069.html)
