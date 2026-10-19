# NEONRED actions and verification status — 2026-10-18

> **Superseded for PCB fabrication status by [NEONRED_READINESS_CHECK_2026-10-18.md](NEONRED_READINESS_CHECK_2026-10-18.md).** A live EasyEDA DRC and fresh Gerber export were completed after this older status was drafted. Firmware, physical-power, and bench-test items below remain open.

This report replaces conflicting older summaries for the current `cyberdeck-completed` revision. It records work completed from the saved files and identifies the checks that require the actual modules or EasyEDA session.

## Result

**The PCB is not yet cleared for power-on or a final “ready to work” claim.** The saved release snapshot has a recorded zero-error configured DRC and a valid two-layer Gerber archive, but the selected INIU bank cannot guarantee enough simultaneous output for the full system, the proposed external protection/wiring is not present on the board, and no assembled hardware has been bench-tested. A bare-board prototype can be ordered only as an unpowered prototype; this is not an assembled or operating-system sign-off.

## 1. Parts and power plan

- [x] Reconciled the current board scope from the 2026-10-18 PCB export: Pi Zero 2 W, LILYGO T-Display-S3 AMOLED, CardKB, rotary encoder and navigation switches, onboard IR, two nRF24L01 modules, Waveshare four-port USB HAT, external Chameleon Ultra SE3, and the previously selected HDMI screen.
- [x] Confirmed the digital design’s auxiliary connector: JP4 pin 1 `+5V_EXT`, pin 2 GND, pin 3 `3V3_AUX`, pin 4 GND.
- [x] Updated the live Google BOM row 33 and the local current BOM mirrors to label the $29.99 INIU 20,000 mAh bank **not suitable for full-system power**.
- [ ] Verify the exact revision/model printed on each owned board and the INIU bank label. Saved project files do not prove what is physically in hand.
- [ ] Choose a replacement supply after measuring the complete load. As a conservative planning estimate, target at least **30 W of guaranteed simultaneous output** with an independently regulated Pi branch rated for 5 V / 2.5 A or better and a separately protected auxiliary branch. The exact branch capacities still need measurements.

The INIU manufacturer specification gives the BI-B5 5 V / 3 A (15 W) total when multiple outputs are active. Raspberry Pi recommends 5 V / 2.5 A for Zero models, which is 12.5 W by itself; that leaves only 2.5 W of idealized headroom from the shared 15 W ceiling for the other branch, while the Pi USB hub and attached devices also draw from the Pi branch. That is not enough guaranteed margin for this design. INIU's [B5 product specifications](https://iniushop.com/collections/portable-fast-charging-series/products/iniu-megapower-20000mah-portable-charger) list the shared multi-output limit; Raspberry Pi's [official power guidance](https://www.raspberrypi.com/documentation/computers/getting-started.html) gives the Zero-model recommendation.

## 2. Safe wiring

- [x] Documented the intended split: intact USB cable from the battery to Pi `PWR IN`; a separate protected regulated supply for the LILYGO/JP4 auxiliary branch; external 3.3 V regulator output to JP4 pins 3/4.
- [ ] Build the fused auxiliary harness and verify polarity/voltage/current at every connector before attaching modules. The PCB has no input fuse, reverse-polarity protection, 5 V converter, 3.3 V converter, or high-current Pi path.
- [ ] Select the fuse only after load and harness measurements. It must protect the wire/connector while tolerating measured peaks; the correct rating is not established yet.
- [ ] Verify HAT and USB-device current on the Pi branch. Do not add a second 5 V source to the USB HAT upstream VBUS.

**Do not cut the battery USB cable and solder its +/− wires to JP4.** JP4 is not a battery input: it includes both 5 V and 3.3 V pins and has no onboard protection. Keep the bank sealed and use its intact USB cable into the Pi. Use a separate, correctly regulated and fused lead for JP4. Do not power the Pi from the LILYGO board or carrier traces.

## 3. Saved PCB and fabrication-file checks

- [x] Parsed the latest saved PCB export, [PCB_PCB_cyberdeck-completed_2026-10-18.json](../PCB/PCB_PCB_cyberdeck-completed_2026-10-18.json): 36 footprints, 29 named nets, 151 track segments, 9 vias, 4 drilled holes, and two copper layers.
- [x] Confirmed all 11 footprints carrying footprint-status annotations in the export have no `DRAFT`/`VERIFY BEFORE FAB` flag. The dated EasyEDA review records those 11 as checked against candidate parts; this is still a document check, not inspection of purchased parts.
- [x] Read the dated live EasyEDA audit, which records **DRC Errors (0)** and **29/29 nets** for its saved board snapshot. The saved export and the audit are consistent in component/net/layer counts.
- [x] Verified the latest Gerber ZIP with the ZIP integrity checker (`testzip` returned no corrupt member). It contains top/bottom copper, top/bottom solder mask, top silkscreen, paste, outline, plated/non-plated drill files and the order note. The Gerber header identifies a 210 × 110 mm board outline and two copper layers.
- [ ] Rerun DRC and export Gerbers from the *same* currently open EasyEDA revision. EasyEDA was not available as an open app during this pass, so the recorded DRC was not rerun live. The Gerber was generated a few minutes before the saved JSON export; although their recorded board counts match, regenerate both together before placing an order.
- [ ] Reconcile the saved schematic with the board in EasyEDA. The separately saved Option 2 power schematic is a candidate and is not proof that the live schematic, board, and Gerber are synchronized.

The Gerber is a valid manufacturing archive, but archive validity plus a clean geometry DRC does not prove correct electrical function or safe supply capacity.

## 4. Bench testing

- [ ] With no modules attached, inspect for solder bridges and measure resistance between each power rail and GND.
- [ ] Use a current-limited bench supply to validate +5V_EXT and 3V3_AUX polarity and voltage before connecting electronics.
- [ ] Connect one module at a time: LILYGO, CardKB/level shifter, each radio, then IR receiver/transmitter. Measure idle/transmit peaks and regulator temperature.
- [ ] Test the Pi and HAT separately, then enumerate and load-test each USB peripheral.
- [ ] Measure both power branches together under worst expected use and verify voltage stays in spec through startup and radio/IR transmit bursts.
- [ ] Only after those checks, run a combined system test and estimate runtime from measured average power. A 20,000 mAh bank stores about 74 Wh at cell voltage before conversion loss; five hours would require average system input well below 15 W, so five-hour operation is not established.

These checks cannot be completed without the physical modules, a current-limited bench supply, a multimeter, and preferably a USB power meter/oscilloscope.

## 5. Firmware and controls

- [x] Compared the saved PCB signal nets with `Firmware/esp32/include/cyberdeck_pins.h`: GPIO2/3 encoder, GPIO42 shared encoder/SELECT, GPIO43–46 navigation, GPIO12/11/13 shared radio SPI, separate radio CE/CSN, GPIO39 IR RX, and GPIO40 IR TX align with the exported connector nets.
- [x] Fixed a firmware/documentation mismatch: added CardKB I²C polling at address `0x5F` on GPIO1/GPIO41, reporting printable characters and special key codes over serial. M5Stack documents that one-byte I²C interface and address in its [official CardKB example](https://github.com/m5stack/M5Stack/blob/master/examples/Unit/CardKB/CardKB.ino).
- [x] Python firmware/bridge files pass Python bytecode syntax compilation.
- [ ] Compile the ESP32 firmware with PlatformIO. PlatformIO is not installed in this workspace, so C++ compilation could not be run here.
- [ ] Flash and test serial `PING`/`STATUS`, CardKB, all controls, IR receive/transmit, and each radio separately. No physical firmware test has occurred.
- [ ] Implement Linux keyboard injection and the finished AMOLED menu only after deciding the intended UI behavior; current firmware emits key/button events but does not yet provide those user-facing features.

## Changes made during this pass

- The live Google Sheet row 33 now marks the selected INIU bank as unsuitable for the complete system and explains its shared 15 W output limit. The existing price remains visible as a comparison; the current subtotal is therefore **not a final buy total** until the bank is replaced.
- Updated the local current BOM CSV mirrors to show the same rejection.
- Replaced stale root and PCB README claims with the actual `cyberdeck-completed` revision and current power warning.
- Rewrote the Option 2 power note to distinguish the saved candidate schematic from the live design.
- Added CardKB polling to the ESP32 firmware and brought its support/protocol notes into agreement.

No hardware was ordered, powered, or physically measured. No live EasyEDA board edit was made in this pass.
