# Cyberdeck project summary

Updated: **2026-10-09** (America/Los_Angeles). The current goal is recorded in [NEONRED_FINAL_VERSION_2026-10-09.md](NEONRED_FINAL_VERSION_2026-10-09.md). It supersedes the older HDMI-based description below: the current version has **no separate HDMI display**, and proposes a removable Proxmark3 instrument, one RTL-SDR Blog V4 with external radar-band downconverters, passive Flock You experimentation, a separately flashed ESP32 Marauder mode, and an external ESP32 antenna only if the exact LILYGO revision supports it. These additions are not yet reflected in the saved EasyEDA project or verified on hardware. Sections below preserve prior design history; where they conflict with the new goal, treat them as historical rather than fabrication instructions. The live EasyEDA editor was not available in the computer session, so no new EasyEDA screenshot, schematic, PCB, or DRC claim is made.

The earlier revision's specific power arrangement below is historical and is **not the current requested design**. Retain its electrical notes only as record of the previous revision.

## Final project vision and inspiration

**NEONRED** is intended to become a compact, repairable clamshell cyberdeck: a portable Linux computer and electronics workbench that the user designs, builds, programs, and documents from the carrier PCB through the finished 3D-printed case. The Raspberry Pi Zero 2 W is the main Linux computer and drives the HDMI display. The LILYGO ESP32-S3 AMOLED is the always-available control interface for the CardKB keyboard, rotary encoder, IR hardware, and low-power radio modules. A separately mounted Waveshare USB HUB HAT expands the Pi, while the Chameleon Ultra SE3, ALFA dual-band Wi-Fi adapter, display, battery bank, and folding-antenna arrangement make the finished unit self-contained.

The intended final form is a laptop-like case: keyboard in the base; Pi, HAT, Chameleon, and protected wiring below it; an HDMI display in the lid; and a lid window that exposes the base-mounted LILYGO display when the deck is closed. It should be maintainable, with screws, standoffs, service access, cable routing, and replaceable modules rather than permanently buried parts.

### Intended, authorized uses

- Linux development, portable programming, diagnostics, and display/keyboard experimentation.
- ESP32 firmware development; I2C keyboard and encoder control; IR learning and replay for the user's own remotes.
- NFC/RFID work with the user's own tags, cards, and lab equipment through the Chameleon.
- Wi-Fi, Bluetooth, and nRF24 experimentation limited to the user's own equipment, networks, or an authorized test environment; the project must not interfere with other people's radio communications or networks.
- Learning the complete hardware-development cycle: circuit and PCB design, enclosure CAD, 3D printing, embedded firmware, Linux integration, wiring, physical assembly, debugging, and documentation.

### Recovered inspiration record

The earlier wiring chat records that the user shared **two Instagram cyberdeck projects** as visual inspiration, along with a Reddit cyberdeck/radio-project reference. The recovered Instagram references are [post DSUnpaNAXFA](https://www.instagram.com/p/DSUnpaNAXFA/) and [post Dcdjywps34d](https://www.instagram.com/p/Dcdjywps34d/). The design direction recovered from that discussion is a compact, feature-dense, hands-on cyberdeck with a keyboard, multiple displays, portable power, radio hardware, IR capability, visible electronics, and a repairable custom enclosure. The external sources are inspiration and historical research only; they are not approved wiring, firmware, or test procedures.

## Mechanical enclosure revision 1 (2026-10-03)

An editable mechanical enclosure design now exists at [Cyberdeck_Enclosure.scad](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/cad/Cyberdeck_Enclosure.scad), with a companion [layout drawing](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/cad/Cyberdeck_layout.svg) and [physical validation checklist](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/cad/MECHANICAL_VALIDATION.md). It models a removable service tray, 42 mm base, lid/display cavity, keyboard frame, ESP32 cradle, Pi/HAT support posts, an under-tray Chameleon sled, cable guides, IR/encoder/switch openings, battery hooks and generic antenna pivots.

The HAT's published 65 x 30 mm footprint, 58 x 23 mm hole pattern and the saved 51.8 x 8 mm PCB header slot are incorporated. The Chameleon cannot fit beside the HAT under the CardKB at the same height, so the current model gives it a separate under-tray bay. Mated plug dimensions, real cable bend radii, actual Chameleon dimensions and RFID performance inside the case are unverified. Print the existing 1:1 mounting template and complete the validation checklist before manufacturing either the case or PCB.

The current saved EasyEDA schematic and PCB contain **21 components, 132 electrical pins, 17 functional nets, 77 connected pins and 55 intentional NC pins**. Native exports agree pin-for-pin, all 17 functional nets pass geometric continuity checks, and EasyEDA reports **0 DRC errors**. Its **72/72** native net counter includes the 55 isolated NC pad nets. These checks do not establish actual load capacity, temperature, RF performance or assembled fit.

The carrier remains **190 × 110 mm with R5 corners**. Keyboard/frame guides, the case-mounted I2C encoder connection, HAT cutout and module mounting positions remain. The two obsolete LM73100 support holes are removed. Fingerprint reader, extra microSD and custom USB expansion remain removed. The Pi's native boot-card slot is unchanged. User-added NEONRED lettering is preserved.

## Current files

- [schematic-simple-power-native.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/schematic-simple-power-native.json) and [pcb-simple-power-native.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/pcb-simple-power-native.json) are the current saved native authority.
- [wiring-map-simple-power.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/wiring-map-simple-power.json) and [wiring-map-simple-power.txt](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/wiring-map-simple-power.txt) contain every current pin.
- [cyberdeck-bom-updated.xlsx](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/cyberdeck-bom-updated.xlsx) and [live Google Sheet](https://docs.google.com/spreadsheets/d/16lRwI5R3pBksWb1bjXYjF_alQrG_2C0rFS-AZ5qpXIg/edit).
- [simple-power-native-verification.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/simple-power-native-verification.json), [simple-power-routing-audit-native.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/simple-power-routing-audit-native.json) and [simple-power-native-drc.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/simple-power-native-drc.json) record verification.
- [simple-power-mounting-template.pdf](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/simple-power-mounting-template.pdf) is the current 1:1 mounting template; print at actual size and check its 100 mm calibration before use. [simple-power-mounting-template-audit.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/simple-power-mounting-template-audit.json) binds it to the saved PCB.

Older power-controls files describe the rejected distributor and are historical. Do not manufacture them or use their pinout for this revision.

## Historical: previous simple power arrangement (superseded 2026-10-06)

- Power the LILYGO through its own intact USB-C cable and the Pi through its own PWR IN connection. The Pi supplies its separately mounted Waveshare HAT through a proper USB host/data cable. Do not independently feed HAT 5 V as well.
- Power the HDMI display externally; confirm its exact 5 V connection against the actual display. The selected older HDMI/SPI-touch module must not be assumed to have a USB power socket. Chameleon can receive power through its normal USB connection; do not connect a second power feed simultaneously.
- One external regulated USB 5 V source supplies CardKB and the input of an assembled **Pololu D24V10F3 #2830**. The regulator's 3.3 V output supplies the radios and IR through JP2. The regulator is wired externally, insulated and mechanically secured.
- **JP2: 1 = +5V_EXT, 2 = GND, 3 = 3V3_AUX, 4 = GND.** ESP3V3 is a separate rail. All grounds are common; never join either regulator output to the other. LILYGO VSYS stays NC.
- The inline USB on/off switch affects the peripheral supply only. It is not a deck-wide power switch or a Pi shutdown button. Halt Linux before removing Pi power.

A USB bank's current rating is its maximum available output, not current forced through the board. Actual load and faults determine current. Individual main-device cables keep their combined load off the carrier, but a bank's total rating still applies across its ports. The recorded Miady AS-TPB21 bank rating is 5 V / 2.4 A total; confirm the physical label. No claim is made that all devices fit one bank's budget.

The LILYGO RT9080 regulator's 600 mA rating includes its own ESP32/display load, so high-current radio/IR peripherals are not assigned to it. The external Pololu's nominal 1 A output is also conditional on operating conditions. Measure actual radio/IR peak demand, voltage drop and temperature before fabrication approval. Wider peripheral traces reduce drop; they are not a current limiter or proof against shorts.

**Power-state convention:** direct SPI/IR connections and the BSS138 I2C module do not provide complete power-off isolation. Use the connected system with both ESP and peripheral supplies present. Disconnect affected signal harnesses before operating/programming one domain alone. Do not leave an unpowered module driven through its GPIO protection paths. This is an operating constraint of the intentionally simplified circuit.

## Through-hole assembly and keyboard interface

There are no loose SMD parts to solder on the carrier. R1–R4 are axial 10 kΩ resistors. C1/C2/C5/C7 are 100 nF through-hole ceramic capacitors; C3/C4/C6/C8 are 10 µF through-hole electrolytics. Electrolytic pad 1 is positive and pad 2 is GND. Check real lead pitch and body clearance against the selected footprints.

The preassembled **Adafruit #757 BSS138 level-shifter module** replaces Q1/Q2 and R5–R8. Only through-hole headers and a harness need soldering. It has built-in pullups. Its physical mounting footprint is not guessed on the carrier: JP3 is a generic 1×8, 2.54 mm harness connector.

| JP3 pin | Net | Connection on assembled #757 |
|---|---|---|
| 1 | GND | GND |
| 2 | ESP3V3 | LV |
| 3 | +5V_EXT | HV |
| 4 | SDA_LV | A1 |
| 5 | KB_SDA | B1 |
| 6 | SCL_LV | A2 |
| 7 | KB_SCL | B2 |
| 8 | GND | Other GND |

Adafruit channel names A1/A2 here are not LILYGO reference A1. Leave unused level-shifter channels unconnected. CardKB still receives regulated 5 V. Start I2C at 100 kHz and check pullups/rise time with the actual module and cables.

**JP8 encoder:** 1 GND, 2 ESP3V3, 3 SDA_LV, 4 SCL_LV. The case-mounted Adafruit5880 module is assembled; default address 0x36 differs from CardKB's 0x5F. Its shaft/panel/knob fit remains to measure.

Removed: LM73100 carrier distributor, carrier fuse, power-output pigtail pads, bare translator ICs, added 0603 resistors/capacitors and AUX_OE_N. GPIO2 is NC again. The external regulator is retained only for peripheral power.

## Firmware pins

| Function | ESP32 GPIO |
|---|---|
| Shared radio SCK / MOSI / MISO | 12 / 11 / 13 |
| Radio1 CSN / CE | 10 / 14 |
| Radio2 CSN / CE | 15 / 16 |
| CardKB and encoder SDA / SCL | 1 / 41 |
| IR receive / transmit | 39 / 40 |
| Externally unused GPIO | 2, 3, 42, 43, 44, 45, 46 |

Set both radio CSN pins HIGH, both CE pins LOW and IR transmit LOW before using the peripherals. The wiring supports two independently configured nRF24L01+ radios: shared SPI SCK/MOSI/MISO (GPIO 12/11/13), with separate CSN/CE pairs (Radio 1 GPIO 10/14; Radio 2 GPIO 15/16). Firmware must serialize SPI transactions and select one radio at a time to configure it and load its TX FIFO. To transmit concurrently, configure each radio to a different RF channel, preload both TX FIFOs, then assert both CE pins nearly together; the radios transmit autonomously after that, so SPI can be reused. A single GPIO write cannot drive both CE pins because they are separate ESP32 outputs, though their start times can be kept very close. This is a firmware operation; no extra connection between the radios is needed. Start with well-separated channels within the locally permitted 2.4 GHz band (for example RF_CH 5 and 75), use compatible air data rates/packet settings at each receiver, and test for mutual desensitization/interference with the actual antennas and transmit power. Simultaneous operation is not yet hardware-tested. No translator-enable GPIO is required. Firmware, CardKB-to-Pi forwarding, encoder actions, HDMI/touch and Linux setup still require integration.

## Enclosure concept approved for documentation

The enclosure opens like a small laptop. In the open working position, the keyboard is nearest the user and the hinge is at the rear. Closing the lid covers the keyboard and main display while leaving the smaller LILYGO screen visible through a dedicated window.

![User enclosure concept with folding side antennas](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/enclosure-concept.png)

The picture establishes the basic arrangement. The latest user correction takes precedence: keep the Pi between keyboard and ESP32, but mount the HAT separately under the keyboard beside the Pi, using screws and a micro-USB data link. Chameleon and loose wiring also remain planned under the keyboard; fit these together rather than assuming each has the whole space. Carrier-mounted components must still stay outside the keyboard footprint. The center Wi-Fi antenna was requested in text. Retainers, isolation, access panels, cable channels and the complete enclosure remain unmodeled and unvalidated.

### Lid and displays

- Mount the selected Waveshare 3.5-inch HDMI screen inside the lid, mainly on the left and center. Its display faces inward toward the user when the case is open.
- Recess its rear controller, brackets, and wiring into the lid. Leave clearance so closing the case does not press on the CardKB keys or either screen.
- Put a rectangular viewing opening on the right of the lid. Align it to the base-mounted LILYGO AMOLED in the fully closed position, accounting for the hinge motion and lid thickness.
- The LILYGO remains fixed in the base; opening the lid moves the window away and exposes the small screen directly.
- A clear protective insert over the window is an option. Its material, opening dimensions, and screen clearance remain to be selected.

### Base surface and service access

- Place the CardKB keyboard across the left and center of the base.
- Place the LILYGO on the right, long axis front to back and screen upward. Keep the Pi parallel to it between keyboard and LILYGO, on its own standoffs. The retained HAT has four matching carrier mounts under the keyboard beside the Pi. Select spacer height and confirm connector orientation with the keyboard, Chameleon, carrier and cables assembled.
- Use a removable top mounting panel, with independent supports for the keyboard and LILYGO. Keep the LILYGO USB connection and buttons accessible.
- Put the custom carrier PCB below the keyboard on insulated mounting spacers. Provide a removable bottom cover for access to wiring, screws, connectors, and replacement parts.
- Determine base depth from the actual separate Pi and HAT mounting heights, keyboard, Chameleon, headers, connectors, carrier and spacers. The old stacked Pi/HAT assumption no longer determines the case depth; no final case height is established.

### Internal organization

| Area | Proposed contents and access |
|---|---|
| Below the keyboard | Separately screwed HAT beside the Pi, Chameleon SE3 Ultra and extra wiring, above a carrier area free of carrier-mounted components. Their combined footprint, connector access, insulation and vertical clearances must be measured. |
| Between keyboard and ESP32 | Raspberry Pi Zero 2, long axis front to back and parallel to ESP32, on its four existing supports. The HAT mounts separately under the keyboard at X20–85/Y62.5–92.5. Its body is 25 mm from the Pi body guide; this does not prove clearance for mated plugs and cable bends. |
| Rear left and rear right | The two external 2.4 GHz radio modules, near their corresponding case-mounted antenna connections. |
| Rear center | ALFA Wi-Fi adapter planning bay, X62–142/Y1–31 mm (80 × 30 mm); adapter, USB/pigtail and antenna fit remain unverified. |
| Near the peripheral cable entry | JP2 receives external regulated 5 V and 3.3 V. The assembled regulator and inline USB switch are wired externally and insulated. Main-device USB power bypasses the carrier. |
| Chameleon access | Removable cradle below the keyboard; maintain USB/service access and test RFID/NFC operation in the proposed stack. |
| Left case side | IR receiver/emitter on a separate, wired module, with its optical faces through the case side. JP1 is only the carrier cable header. |
| Around the perimeter | Secured USB, power, and signal cables, kept clear of mounting screws, panel edges, and moving parts. |

### Three folding antennas

- **Left and right pair:** One articulated antenna near each rear side corner. When stored, they fold forward along the sides, parallel to the closed box. When deployed, they swing outward away from the enclosure.
- These side antennas correspond to the two nRF24L01+ PA/LNA modules. The user called them the Bluetooth antennas; electrically they are **2.4 GHz radio antennas**. The nRF24 modules use Enhanced ShockBurst. Bluetooth LE functions use the ESP32-S3/Pi Bluetooth hardware; Classic Bluetooth support depends on the confirmed Pi hardware/software. These are not interchangeable antenna connections.
- **Center antenna:** A single dual-band 2.4/5 GHz Wi-Fi antenna at the rear center, connected to the ALFA AWUS036ACS. It should fold for storage and raise for use. Its joint and complete movement must clear the hinge and the lid in every position.
- Secure the antenna connectors to the enclosure so antenna movement does not load the PCB directly. Select matching connectors/pigtails after identifying the actual radio modules and antenna fittings. The ALFA has one RP-SMA female antenna connector.
- Keep the side antenna movement clear of the user's hands, lid, battery, hooks, and cables. The three antenna locations describe the mechanical concept; RF performance and coexistence have not been measured.

### Battery and hinge wiring

- Hold the external power bank with hooks/clips on the left side, toward the lower/front area, leaving the left rear antenna pivot and folding path clear.
- Main devices use individual external power cables. Budget each power bank separately, provide access to its ports, and never parallel their 5 V outputs.
- Check that the mounted battery's weight does not make the unit unstable while typing or opening the lid.
- Run HDMI and display-power cables through a protected channel beside the hinge, with a controlled flex loop and strain relief. Select the actual cable and connector arrangement before fixing hinge geometry.
- Use secured cable paths so closing the lid cannot pinch wires. Verify the full opening/closing movement with the battery and all antennas installed.


## Mounts and physical constraints

| Part | Recorded size / allowance |
|---|---|
| LILYGO T-Display-S3 AMOLED, original/basic | 1.91-inch display; visible area 44.22 × 19.8 mm. Manufacturer module figure 60 × 25.5 × 10 mm before added headers. Confirm the owned revision. |
| CardKB v1.1 | Drawing 84 × 54 mm; catalog 88 × 54 × 5 mm. Reserve 88 × 54 × 6.3 mm plus its cable, and measure the actual board. |
| Raspberry Pi Zero 2 | Nominal 65 × 30 mm; cable and spacer envelopes are additional. |
| Waveshare USB HUB HAT SKU12694 | 65 × 30 mm, four USB ports, no Ethernet. |
| Waveshare HDMI LCD SKU12824 | 3.5-inch, 480 × 320; nominal module outline 85.01 × 56.41 mm. Complete plug depth and independent power connection need confirmation. |
| ALFA AWUS036ACS | Manufacturer nominal 55 × 25 × 10 mm; reserve 80 × 30 mm for planning, with plugged-in fit still unverified. |

The 84 × 54 mm CardKB body guide is X10–94/Y43–97; the larger 88 × 54 mm reserve remains X8–96/Y43–97. No carrier-mounted resistors, capacitors or other components belong beneath it. Four Ø3.2 mm printed-frame mounts are at (5,38), (99,38), (5,105), (99,105) mm. The keyboard's direct screw locations are unknown; do not use these as CardKB drill coordinates.

The owned Waveshare USB HUB HAT SKU12694 is the 65 × 30 mm, four-USB model without Ethernet. It is screwed separately under the keyboard, beside the Pi, not stacked on the Pi. HAT mounts are (23.5,66), (81.5,66), (23.5,89), (81.5,89) mm, Ø3.2 on a 58 × 23 mm pattern. The rounded header cutout is 51.8 × 8 mm R1 at X26.6–78.4/Y85–93. This remains a planning clearance envelope: measure the actual underside housing and plugged-in USB cable before manufacture. HAT3/HAT4 supports, screw heads and washers must be ≤5.5 mm outside diameter.

The four Pi Ø2.75 mm mounting holes remain at (113.698,35.579), (136.698,35.579), (113.698,93.579), (136.698,93.579) mm. Pi body guide is X110–140/Y32–97. All 40 carrier Pi contacts are electrically NC. The LILYGO remains screen-up on the right with front USB access; its four frame holes are (153,32), (186,32), (153,98), (186,98) mm, Ø3.2. These are cradle/frame supports, not claimed direct LILYGO holes.

The rear-center ALFA bay X62–142/Y1–31 (80 × 30 mm) stays reserved. IR remains the only connector/module function at the left side, with the actual optical module wired to the case wall. The total carrier mount count is 20, including the four non-plated Pi mounting pads. Insulating spacers/washers are required on both faces at metal-fastener contact areas; electrical DRC does not validate screw-head contact with copper.

Keyboard, HAT, Chameleon, cable bends, USB plugs and spacers must be checked together. The slot alone does not establish flush HAT mounting or enough keyboard height. The clamshell, frame, hinge, window and antenna pivots remain mechanical design work.

## BOM and readiness

The current BOM preserves the user's ELEGOO kit status as Optional and avoids double-counting included parts. Totals below include priced rows only, excluding TBD parts, fabrication, shipping/tax and enclosure work. Main power cables stay intact; only the separate peripheral supply uses a verified USB 5 V wire connection.

Selected: $188.59 | If needed: $30.27 | Combined: $218.86 | Optional: $69.48

Before ordering: verify actual regulator/radio/IR loads and power sequencing, capacitor/connector lead dimensions, module orientations, insulated mounting and the full keyboard/HAT/Chameleon stack. Native DRC0 is not certification against wiring errors, shorts or overheating. No new Gerbers are approved by these checks.

## Sources for electrical choices

- [LILYGO schematic](https://github.com/Xinyuan-LilyGO/T-Display-S3-AMOLED/blob/main/schematic/T-DISPLAY-S3-AMOLED.pdf), [RT9080 datasheet](https://www.richtek.com/assets/product_file/RT9080/DS9080-09.pdf).
- [Pololu D24V10F3](https://www.pololu.com/product/2830), [Adafruit757](https://www.adafruit.com/product/757), [Adafruit IR guide](https://learn.adafruit.com/adafruit-infrared-ir-remote-transceiver?view=all).

## Current simplified complete electrical pin appendix

Native-export verified. GPIO names and carrier pad numbers are distinct. NC means no external carrier connection. Four mechanical Pi pads are excluded.

| Reference | Part | Pin | Pin name | Net |
|---|---|---|---|---|
| A1 | ESP32-S3-AMOLED-1.91 | 1 | 3V3 | ESP3V3 |
| A1 | ESP32-S3-AMOLED-1.91 | 2 | 01 | SDA_LV |
| A1 | ESP32-S3-AMOLED-1.91 | 3 | 02 | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 4 | 03 | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 5 | 10 | RADIO1_CSN |
| A1 | ESP32-S3-AMOLED-1.91 | 6 | 11 | RADIO_MOSI |
| A1 | ESP32-S3-AMOLED-1.91 | 7 | 12 | RADIO_SCK |
| A1 | ESP32-S3-AMOLED-1.91 | 8 | 13 | RADIO_MISO |
| A1 | ESP32-S3-AMOLED-1.91 | 9 | 14 | RADIO1_CE |
| A1 | ESP32-S3-AMOLED-1.91 | 10 | 15 | RADIO2_CSN |
| A1 | ESP32-S3-AMOLED-1.91 | 11 | GND | GND |
| A1 | ESP32-S3-AMOLED-1.91 | 12 | VSYS | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 13 | VSYS | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 14 | 16 | RADIO2_CE |
| A1 | ESP32-S3-AMOLED-1.91 | 15 | 39 | IR_RX |
| A1 | ESP32-S3-AMOLED-1.91 | 16 | 3V3 | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 17 | 3V3 | ESP3V3 |
| A1 | ESP32-S3-AMOLED-1.91 | 18 | GND | GND |
| A1 | ESP32-S3-AMOLED-1.91 | 19 | GND | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 20 | 40 | IR_TX |
| A1 | ESP32-S3-AMOLED-1.91 | 21 | 41 | SCL_LV |
| A1 | ESP32-S3-AMOLED-1.91 | 22 | 42 | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 23 | 43 | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 24 | 44 | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 25 | 45 | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 26 | 46 | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 27 | GND | NC |
| A1 | ESP32-S3-AMOLED-1.91 | 28 | GND | NC |
| C1 | 100nF | 1 | 1 | 3V3_AUX |
| C1 | 100nF | 2 | 2 | GND |
| C2 | 100nF | 1 | 1 | 3V3_AUX |
| C2 | 100nF | 2 | 2 | GND |
| C3 | 10uF | 1 | 1 | 3V3_AUX |
| C3 | 10uF | 2 | 2 | GND |
| C4 | 10uF | 1 | 1 | 3V3_AUX |
| C4 | 10uF | 2 | 2 | GND |
| C5 | 100nF | 1 | 1 | +5V_EXT |
| C5 | 100nF | 2 | 2 | GND |
| C6 | 10uF | 1 | 1 | +5V_EXT |
| C6 | 10uF | 2 | 2 | GND |
| C7 | 100nF | 1 | 1 | 3V3_AUX |
| C7 | 100nF | 2 | 2 | GND |
| C8 | 10uF | 1 | 1 | 3V3_AUX |
| C8 | 10uF | 2 | 2 | GND |
| IC1 | NRF24L01 | 1 | GND | GND |
| IC1 | NRF24L01 | 2 | VCC | 3V3_AUX |
| IC1 | NRF24L01 | 3 | CE | RADIO1_CE |
| IC1 | NRF24L01 | 4 | CSN | RADIO1_CSN |
| IC1 | NRF24L01 | 5 | SCK | RADIO_SCK |
| IC1 | NRF24L01 | 6 | MOSI | RADIO_MOSI |
| IC1 | NRF24L01 | 7 | MISO | RADIO_MISO |
| IC1 | NRF24L01 | 8 | IRQ | NC |
| IC2 | NRF24L01 | 1 | GND | GND |
| IC2 | NRF24L01 | 2 | VCC | 3V3_AUX |
| IC2 | NRF24L01 | 3 | CE | RADIO2_CE |
| IC2 | NRF24L01 | 4 | CSN | RADIO2_CSN |
| IC2 | NRF24L01 | 5 | SCK | RADIO_SCK |
| IC2 | NRF24L01 | 6 | MOSI | RADIO_MOSI |
| IC2 | NRF24L01 | 7 | MISO | RADIO_MISO |
| IC2 | NRF24L01 | 8 | IRQ | NC |
| JP1 | Adafruit 5990 IR RX/TX module | 1 | IRout | IR_TX |
| JP1 | Adafruit 5990 IR RX/TX module | 2 | IRin | IR_RX |
| JP1 | Adafruit 5990 IR RX/TX module | 3 | GND | GND |
| JP1 | Adafruit 5990 IR RX/TX module | 4 | VIN | 3V3_AUX |
| JP2 | REGULATED POWER INPUT | 1 | +5V_EXT | +5V_EXT |
| JP2 | REGULATED POWER INPUT | 2 | GND | GND |
| JP2 | REGULATED POWER INPUT | 3 | 3V3_AUX | 3V3_AUX |
| JP2 | REGULATED POWER INPUT | 4 | GND | GND |
| JP3 | WIRED ADAFRUIT 757 I2C SHIFTER | 1 | GND | GND |
| JP3 | WIRED ADAFRUIT 757 I2C SHIFTER | 2 | LV | ESP3V3 |
| JP3 | WIRED ADAFRUIT 757 I2C SHIFTER | 3 | HV | +5V_EXT |
| JP3 | WIRED ADAFRUIT 757 I2C SHIFTER | 4 | A1 SDA | SDA_LV |
| JP3 | WIRED ADAFRUIT 757 I2C SHIFTER | 5 | B1 SDA | KB_SDA |
| JP3 | WIRED ADAFRUIT 757 I2C SHIFTER | 6 | A2 SCL | SCL_LV |
| JP3 | WIRED ADAFRUIT 757 I2C SHIFTER | 7 | B2 SCL | KB_SCL |
| JP3 | WIRED ADAFRUIT 757 I2C SHIFTER | 8 | GND | GND |
| JP8 | WIRED ADAFRUIT 5880 ENCODER | 1 | GND | GND |
| JP8 | WIRED ADAFRUIT 5880 ENCODER | 2 | 3V3 | ESP3V3 |
| JP8 | WIRED ADAFRUIT 5880 ENCODER | 3 | SDA | SDA_LV |
| JP8 | WIRED ADAFRUIT 5880 ENCODER | 4 | SCL | SCL_LV |
| PI1 | Raspberry Pi Zero 2 W | 1 | 3V3 | NC |
| PI1 | Raspberry Pi Zero 2 W | 2 | 5V | NC |
| PI1 | Raspberry Pi Zero 2 W | 3 | GPIO2 sda | NC |
| PI1 | Raspberry Pi Zero 2 W | 4 | 5V | NC |
| PI1 | Raspberry Pi Zero 2 W | 5 | GPIO3 scl | NC |
| PI1 | Raspberry Pi Zero 2 W | 6 | GND | NC |
| PI1 | Raspberry Pi Zero 2 W | 7 | GPIO4 | NC |
| PI1 | Raspberry Pi Zero 2 W | 8 | tx GPIO14 | NC |
| PI1 | Raspberry Pi Zero 2 W | 9 | GND | NC |
| PI1 | Raspberry Pi Zero 2 W | 10 | rx GPIO15 | NC |
| PI1 | Raspberry Pi Zero 2 W | 11 | GPIO17 | NC |
| PI1 | Raspberry Pi Zero 2 W | 12 | pwm0 GPIO18 | NC |
| PI1 | Raspberry Pi Zero 2 W | 13 | GPIO27 | NC |
| PI1 | Raspberry Pi Zero 2 W | 14 | GND | NC |
| PI1 | Raspberry Pi Zero 2 W | 15 | GPIO22 | NC |
| PI1 | Raspberry Pi Zero 2 W | 16 | GPIO23 | NC |
| PI1 | Raspberry Pi Zero 2 W | 17 | 3V3 | NC |
| PI1 | Raspberry Pi Zero 2 W | 18 | GPIO24 | NC |
| PI1 | Raspberry Pi Zero 2 W | 19 | GPIO10 mosi | NC |
| PI1 | Raspberry Pi Zero 2 W | 20 | GND | NC |
| PI1 | Raspberry Pi Zero 2 W | 21 | GPIO9 miso | NC |
| PI1 | Raspberry Pi Zero 2 W | 22 | GPIO25 | NC |
| PI1 | Raspberry Pi Zero 2 W | 23 | GPIO11 sck | NC |
| PI1 | Raspberry Pi Zero 2 W | 24 | cs0 GPIO8 | NC |
| PI1 | Raspberry Pi Zero 2 W | 25 | GND | NC |
| PI1 | Raspberry Pi Zero 2 W | 26 | cs1 GPIO7 | NC |
| PI1 | Raspberry Pi Zero 2 W | 27 | eeprom sda | NC |
| PI1 | Raspberry Pi Zero 2 W | 28 | eeprom scl | NC |
| PI1 | Raspberry Pi Zero 2 W | 29 | GPIO5 | NC |
| PI1 | Raspberry Pi Zero 2 W | 30 | GND | NC |
| PI1 | Raspberry Pi Zero 2 W | 31 | GPIO6 | NC |
| PI1 | Raspberry Pi Zero 2 W | 32 | pwm0 GPIO12 | NC |
| PI1 | Raspberry Pi Zero 2 W | 33 | GPIO13 pwm1 | NC |
| PI1 | Raspberry Pi Zero 2 W | 34 | GND | NC |
| PI1 | Raspberry Pi Zero 2 W | 35 | GPIO19 pwm1 | NC |
| PI1 | Raspberry Pi Zero 2 W | 36 | GPIO16 | NC |
| PI1 | Raspberry Pi Zero 2 W | 37 | GPIO26 | NC |
| PI1 | Raspberry Pi Zero 2 W | 38 | GPIO20 | NC |
| PI1 | Raspberry Pi Zero 2 W | 39 | GND | NC |
| PI1 | Raspberry Pi Zero 2 W | 40 | GPIO21 | NC |
| R1 | 10k | 1 | 1 | RADIO1_CSN |
| R1 | 10k | 2 | 2 | 3V3_AUX |
| R2 | 10k | 1 | 1 | RADIO1_CE |
| R2 | 10k | 2 | 2 | GND |
| R3 | 10k | 1 | 1 | RADIO2_CSN |
| R3 | 10k | 2 | 2 | 3V3_AUX |
| R4 | 10k | 1 | 1 | RADIO2_CE |
| R4 | 10k | 2 | 2 | GND |
| U1 | CardKB Module | 1 | GND | GND |
| U1 | CardKB Module | 2 | VCC | +5V_EXT |
| U1 | CardKB Module | 3 | SDA | KB_SDA |
| U1 | CardKB Module | 4 | SCL | KB_SCL |

## Current source hashes

- `outputs/schematic-simple-power-native.json`: `1861b7872267eff313ba5267874894d55dfa8f3b06d74e385273eb774742225c`
- `outputs/pcb-simple-power-native.json`: `14c6ba430bfcb49659fa3ca9d57fee9c3092dd0da13f206e33ee1388b886b47c`
- `work/simple-peripherals-component-map.json`: `58d2b779711a2a97318d4067444a9b429520f63a5a96270ed082f26117d4516f`


**ARCHIVE ONLY: every pin table below is historical. Use the current simplified table above.**

## Historical removed power-distribution revision — superseded by simplified power

Authoritative mapping verified against the saved native schematic and PCB exports. Every electrical pin is listed; NC is explicit. Pi mechanical pads and mounting holes are not electrical pins. Native export hashes: `schematic-power-controls-native.json` SHA256 `c6dd9f6371514cf68ee9e741c188a929ef288a5cd1dccff107ef14cf852d8e13`; `pcb-power-controls-native.json` SHA256 `b4796bb77268608138cc8b267f974186b767fe223fdead7ee2df95f0b2418739`; `cyberdeck-bom-updated.xlsx` SHA256 `9cc962a5175b6ab825eb978ec275115109c2573b792e384497ee6c337922aa92`.

| Component | Pin | Symbol pin name | Current net |
|---|---|---|---|
| A1 | 1 | 3V3 | ESP3V3 |
| A1 | 2 | 01 | SDA_LV |
| A1 | 3 | 02 | AUX_OE_N |
| A1 | 4 | 03 | NC |
| A1 | 5 | 10 | ESP_RADIO1_CSN |
| A1 | 6 | 11 | ESP_RADIO_MOSI |
| A1 | 7 | 12 | ESP_RADIO_SCK |
| A1 | 8 | 13 | ESP_RADIO_MISO |
| A1 | 9 | 14 | ESP_RADIO1_CE |
| A1 | 10 | 15 | ESP_RADIO2_CSN |
| A1 | 11 | GND | GND |
| A1 | 12 | VSYS | NC |
| A1 | 13 | VSYS | NC |
| A1 | 14 | 16 | ESP_RADIO2_CE |
| A1 | 15 | 39 | ESP_IR_RX |
| A1 | 16 | 3V3 | NC |
| A1 | 17 | 3V3 | ESP3V3 |
| A1 | 18 | GND | GND |
| A1 | 19 | GND | NC |
| A1 | 20 | 40 | ESP_IR_TX |
| A1 | 21 | 41 | SCL_LV |
| A1 | 22 | 42 | NC |
| A1 | 23 | 43 | NC |
| A1 | 24 | 44 | NC |
| A1 | 25 | 45 | NC |
| A1 | 26 | 46 | NC |
| A1 | 27 | GND | NC |
| A1 | 28 | GND | NC |
| C1 | 1 | 1 | 3V3_AUX |
| C1 | 2 | 2 | GND |
| C2 | 1 | 1 | 3V3_AUX |
| C2 | 2 | 2 | GND |
| C3 | 1 | 1 | 3V3_AUX |
| C3 | 2 | 2 | GND |
| C4 | 1 | 1 | 3V3_AUX |
| C4 | 2 | 2 | GND |
| C5 | 1 | 1 | 5V_SW |
| C5 | 2 | 2 | GND |
| C6 | 1 | 1 | 5V_SW |
| C6 | 2 | 2 | GND |
| C7 | 1 | 1 | 3V3_AUX |
| C7 | 2 | 2 | GND |
| C8 | 1 | 1 | 3V3_AUX |
| C8 | 2 | 2 | GND |
| C9 | 1 | 1 | ESP3V3 |
| C9 | 2 | 2 | GND |
| C10 | 1 | 1 | 5V_SW |
| C10 | 2 | 2 | GND |
| C11 | 1 | 1 | ESP3V3 |
| C11 | 2 | 2 | GND |
| C12 | 1 | 1 | 3V3_AUX |
| C12 | 2 | 2 | GND |
| C13 | 1 | 1 | ESP3V3 |
| C13 | 2 | 2 | GND |
| C14 | 1 | 1 | 3V3_AUX |
| C14 | 2 | 2 | GND |
| F1 | 1 | IN | BANK5V |
| F1 | 2 | OUT | 5V_FUSED |
| IC1 | 1 | GND | GND |
| IC1 | 2 | VCC | 3V3_AUX |
| IC1 | 3 | CE | RADIO1_CE |
| IC1 | 4 | CSN | RADIO1_CSN |
| IC1 | 5 | SCK | RADIO_SCK |
| IC1 | 6 | MOSI | RADIO_MOSI |
| IC1 | 7 | MISO | RADIO_MISO |
| IC1 | 8 | IRQ | NC |
| IC2 | 1 | GND | GND |
| IC2 | 2 | VCC | 3V3_AUX |
| IC2 | 3 | CE | RADIO2_CE |
| IC2 | 4 | CSN | RADIO2_CSN |
| IC2 | 5 | SCK | RADIO_SCK |
| IC2 | 6 | MOSI | RADIO_MOSI |
| IC2 | 7 | MISO | RADIO_MISO |
| IC2 | 8 | IRQ | NC |
| IC3 | 1 | VOUT | 5V_SW |
| IC3 | 2 | IMON | NC |
| IC3 | 3 | DVDT | NC |
| IC3 | 4 | PGTH | NC |
| IC3 | 5 | PGOOD | NC |
| IC3 | 6 | OVLO | NC |
| IC3 | 7 | EN_UVLO | MASTER_UVLO |
| IC3 | 8 | GND | GND |
| IC3 | 9 | VIN | 5V_FUSED |
| IC4 | 1 | PG | NC |
| IC4 | 2 | SHDN | NC |
| IC4 | 3 | VIN | 5V_SW |
| IC4 | 4 | GND | GND |
| IC4 | 5 | VOUT | 3V3_AUX |
| IC5 | 1 | VCCA | ESP3V3 |
| IC5 | 2 | SCLA | SCL_LV |
| IC5 | 3 | SDAA | SDA_LV |
| IC5 | 4 | GND | GND |
| IC5 | 5 | EN | 5V_SW |
| IC5 | 6 | SDAB | KB_SDA |
| IC5 | 7 | SCLB | KB_SCL |
| IC5 | 8 | VCCB | 5V_SW |
| IC6 | 1 | VCCA | ESP3V3 |
| IC6 | 2 | DIR | ESP3V3 |
| IC6 | 3 | A1 | ESP_RADIO_SCK |
| IC6 | 4 | A2 | ESP_RADIO_MOSI |
| IC6 | 5 | A3 | ESP_RADIO1_CSN |
| IC6 | 6 | A4 | ESP_RADIO1_CE |
| IC6 | 7 | A5 | ESP_RADIO2_CSN |
| IC6 | 8 | A6 | ESP_RADIO2_CE |
| IC6 | 9 | A7 | ESP_IR_TX |
| IC6 | 10 | A8 | GND |
| IC6 | 11 | GND | GND |
| IC6 | 12 | GND | GND |
| IC6 | 13 | GND | GND |
| IC6 | 14 | B8 | GND |
| IC6 | 15 | B7 | IR_TX |
| IC6 | 16 | B6 | RADIO2_CE |
| IC6 | 17 | B5 | RADIO2_CSN |
| IC6 | 18 | B4 | RADIO1_CE |
| IC6 | 19 | B3 | RADIO1_CSN |
| IC6 | 20 | B2 | RADIO_MOSI |
| IC6 | 21 | B1 | RADIO_SCK |
| IC6 | 22 | /OE | AUX_OE_N |
| IC6 | 23 | VCCB | 3V3_AUX |
| IC6 | 24 | VCCB | 3V3_AUX |
| IC7 | 1 | VCCA | ESP3V3 |
| IC7 | 2 | A1 | ESP_RADIO_MISO |
| IC7 | 3 | A2 | ESP_IR_RX |
| IC7 | 4 | GND | GND |
| IC7 | 5 | DIR | GND |
| IC7 | 6 | B2 | IR_RX |
| IC7 | 7 | B1 | RADIO_MISO |
| IC7 | 8 | VCCB | 3V3_AUX |
| JP1 | 1 | IRout | IR_TX |
| JP1 | 2 | IRin | IR_RX |
| JP1 | 3 | GND | GND |
| JP1 | 4 | VIN | 3V3_AUX |
| JP2 | 1 | BANK5V | BANK5V |
| JP2 | 2 | GND | GND |
| JP3 | 1 | 5V | 5V_SW |
| JP3 | 2 | GND | GND |
| JP4 | 1 | 5V | 5V_SW |
| JP4 | 2 | GND | GND |
| JP5 | 1 | 5V | 5V_SW |
| JP5 | 2 | GND | GND |
| JP6 | 1 | 5V | 5V_SW |
| JP6 | 2 | GND | GND |
| JP7 | 1 | UVLO | MASTER_UVLO |
| JP7 | 2 | GND | GND |
| JP8 | 1 | GND | GND |
| JP8 | 2 | 3V3 | ESP3V3 |
| JP8 | 3 | SDA | SDA_LV |
| JP8 | 4 | SCL | SCL_LV |
| PI1 | 1 | 3V3 | NC |
| PI1 | 2 | 5V | NC |
| PI1 | 3 | GPIO2 sda | NC |
| PI1 | 4 | 5V | NC |
| PI1 | 5 | GPIO3 scl | NC |
| PI1 | 6 | GND | NC |
| PI1 | 7 | GPIO4 | NC |
| PI1 | 8 | tx GPIO14 | NC |
| PI1 | 9 | GND | NC |
| PI1 | 10 | rx GPIO15 | NC |
| PI1 | 11 | GPIO17 | NC |
| PI1 | 12 | pwm0 GPIO18 | NC |
| PI1 | 13 | GPIO27 | NC |
| PI1 | 14 | GND | NC |
| PI1 | 15 | GPIO22 | NC |
| PI1 | 16 | GPIO23 | NC |
| PI1 | 17 | 3V3 | NC |
| PI1 | 18 | GPIO24 | NC |
| PI1 | 19 | GPIO10 mosi | NC |
| PI1 | 20 | GND | NC |
| PI1 | 21 | GPIO9 miso | NC |
| PI1 | 22 | GPIO25 | NC |
| PI1 | 23 | GPIO11 sck | NC |
| PI1 | 24 | cs0 GPIO8 | NC |
| PI1 | 25 | GND | NC |
| PI1 | 26 | cs1 GPIO7 | NC |
| PI1 | 27 | eeprom sda | NC |
| PI1 | 28 | eeprom scl | NC |
| PI1 | 29 | GPIO5 | NC |
| PI1 | 30 | GND | NC |
| PI1 | 31 | GPIO6 | NC |
| PI1 | 32 | pwm0 GPIO12 | NC |
| PI1 | 33 | GPIO13 pwm1 | NC |
| PI1 | 34 | GND | NC |
| PI1 | 35 | GPIO19 pwm1 | NC |
| PI1 | 36 | GPIO16 | NC |
| PI1 | 37 | GPIO26 | NC |
| PI1 | 38 | GPIO20 | NC |
| PI1 | 39 | GND | NC |
| PI1 | 40 | GPIO21 | NC |
| R1 | 1 | 1 | RADIO1_CSN |
| R1 | 2 | 2 | 3V3_AUX |
| R2 | 1 | 1 | RADIO1_CE |
| R2 | 2 | 2 | GND |
| R3 | 1 | 1 | RADIO2_CSN |
| R3 | 2 | 2 | 3V3_AUX |
| R4 | 1 | 1 | RADIO2_CE |
| R4 | 2 | 2 | GND |
| R5 | 1 | 1 | SDA_LV |
| R5 | 2 | 2 | ESP3V3 |
| R6 | 1 | 1 | SCL_LV |
| R6 | 2 | 2 | ESP3V3 |
| R7 | 1 | 1 | KB_SDA |
| R7 | 2 | 2 | 5V_SW |
| R8 | 1 | 1 | KB_SCL |
| R8 | 2 | 2 | 5V_SW |
| R9 | 1 | 1 | AUX_OE_N |
| R9 | 2 | 2 | ESP3V3 |
| R10 | 1 | 1 | ESP_RADIO1_CSN |
| R10 | 2 | 2 | ESP3V3 |
| R11 | 1 | 1 | ESP_RADIO2_CSN |
| R11 | 2 | 2 | ESP3V3 |
| R12 | 1 | 1 | ESP_RADIO1_CE |
| R12 | 2 | 2 | GND |
| R13 | 1 | 1 | ESP_RADIO2_CE |
| R13 | 2 | 2 | GND |
| R14 | 1 | 1 | ESP_RADIO_SCK |
| R14 | 2 | 2 | GND |
| R15 | 1 | 1 | ESP_RADIO_MOSI |
| R15 | 2 | 2 | GND |
| R16 | 1 | 1 | ESP_IR_TX |
| R16 | 2 | 2 | GND |
| R17 | 1 | 1 | RADIO_MISO |
| R17 | 2 | 2 | GND |
| R18 | 1 | 1 | RADIO_SCK |
| R18 | 2 | 2 | GND |
| R19 | 1 | 1 | RADIO_MOSI |
| R19 | 2 | 2 | GND |
| U1 | 1 | GND | GND |
| U1 | 2 | VCC | 5V_SW |
| U1 | 3 | SDA | KB_SDA |
| U1 | 4 | SCL | KB_SCL |


## Superseded archive — all material below is historical

**Every heading and pin/net table below belongs to an earlier revision and is superseded by the230-pin appendix above. Some original headings retain the word “Current” because their complete source text is preserved verbatim; they are not current wiring or purchase instructions.** In particular, older Q1/Q2, JP2four-pin, fingerprint, microSD and custom-hub assignments must not overwrite this revision.

Historical pin-appendix source byte count: **75211**; SHA-256 **e519fa7af981226692ba270bb2709cf6fdb1fd0beaf8f09a520b1c005cbdfa0d**. All bytes from the previous summary's first134-pin appendix through its final custom-expansion table are retained unchanged below.

### Archived purchasing history

### Historical canceled custom-expansion cost snapshot

The following values belong only to the superseded custom-expansion BOM. Its preserved workbook is in [the local expansion archive](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/archive-usb-expansion-2026-10-01/cyberdeck-bom-usb-expansion.xlsx); do not use these historical totals for the retained HAT-based design:

| Category | Priced subtotal |
|---|---:|
| Selected | $253.87 |
| If needed | $35.59 |
| Selected + if needed | $289.46 |
| Optional | $53.75 |
| All priced lines | $343.21 |

**Thirty TBD-price lines are excluded from these sums.** These figures are not a complete build cost and exclude shipping/tax, unpriced parts, PCB fabrication/assembly and unfinished enclosure work. Purchasing lines may group several schematic components; the 52 added BOM lines cover the expansion purchases and are not a count of schematic parts. That canceled design had 133 added components, including DNP options. Do not treat all component-map entries as populated purchases or the original capacitor kit as coverage for the new SMD decoupling network. These canceled-expansion cost snapshots must not be combined with the restored current BOM totals above.

### Historical September 30 BOM revisions before USB expansion

**Historical purchasing record only. The reader, its included cable and JP3 interface described below are now removed; do not order or wire them for the current design.**

At the Fingerprint2 revision, the [Google Sheets BOM](https://docs.google.com/spreadsheets/d/16lRwI5R3pBksWb1bjXYjF_alQrG_2C0rFS-AZ5qpXIg/edit) has been saved and its numeric totals verified:

| Category | Recorded total |
|---|---:|
| Selected | $184.28 |
| If needed | $30.27 |
| Selected + if needed | $214.55 |
| Optional | $58.74 |
| All listed parts | $273.29 |

These historical Fingerprint2-era totals preceded the current $11.50 reader removal; they are not the current totals. The historical purchasing notes remain for context; prices were not refreshed and exclude shipping and tax.

September 30 purchasing revision: the [Avrest YPT M2.5 standoff assortment, 365 pieces, B0FPMC9917](https://www.amazon.com/dp/B0FPMC9917), verified at **$9.99**, is now its own **Selected** item in BOM row 34 for the Pi/HAT. Its cost was removed from the previous optional box bundle in row 30, so at that stage the all-parts total remained **$261.79**, before the Fingerprint2 addition below. The EEEEE M3 kit remains a separate Selected item in row 31 for the carrier and retaining frames. The required Pi/HAT and frame spacer heights remain pending physical stack measurements.

- Added one **Selected** [M5Stack Unit Fingerprint2 (A-K323CP), SKU U203](https://shop.m5stack.com/products/fingerprint-2-unit-a-k323cp) in **BOM row 35** at the verified official price of **$11.50**. The unit includes one **20 cm HY2.0-4P Grove cable**; no extra cable was added. The previous IR item moved from row 35 to **row 36**. This addition increases Selected by $11.50 to **$184.28** and all listed parts to **$273.29**.

- Fingerprint2 electrical integration is saved in **revision 3**: JP3 supplies **5V**, common ground and **3.3V-logic UART at 115200 baud, 8N1**, with approximately **40 mA** active load. **GPIO43 (ESP TX) and GPIO44 (ESP RX) are assigned**, and JP3 is placed vertically at X151.5/Y65 mm, pin 1 at the top through pin 4 at the bottom. Assembly requires **one four-pin 2.54 mm carrier header at JP3 and one compatible Grove-to-header adapter or wired harness** for the included cable; these are assembly requirements, with no newly verified price or additional purchase included in the totals. Reader case mounting, cutout, cable fit and firmware remain pending. CardKB remains selected and wired as documented.

- Added one [EEEEE M3 standoff assortment, B0FBMFBQHQ](https://www.amazon.com/dp/B0FBMFBQHQ), recorded price **$9.99**: 208 pieces, including 6/10/15/20 mm standoffs. Use for the carrier's Ø3.2 mm mounting holes and retaining frames. It contains no M2.5 hardware; the Pi uses the separate M2.5 kit already listed. Required spacer heights and screw-head/hex-body fit within the 6 mm reserves remain unverified. Availability of 10 mm spacers does not establish the correct stack height.

- The listed ELEGOO kit already covers the required capacitors: **four 100nF** for C1/C2/C5/C7 from its ten supplied, and **four 10uF** for C3/C4/C6/C8 from its five supplied. **100uF capacitors were not required** by the original 26-component schematic. This kit-coverage statement does not cover the expansion's additional capacitors or their packages.

- Replacement options, only if needed: four [KEMET C315C104K5R5TA](https://www.digikey.com/en/products/detail/kemet/C315C104K5R5TA/12701330) at the recorded BOM price of $0.79 each ($3.16), 100nF/50V/X7R with 2.54 mm lead pitch; and four [Panasonic EEA-GA1V100](https://www.digikey.com/en/products/detail/panasonic-industry/EEA-GA1V100/2504583) at the recorded BOM price of $0.34 each ($1.36), 10uF/35V/105°C with 2.00 mm pitch and maximum Ø5.5 × 8 mm body including tolerances. Check actual body clearance before assembly. Polarized capacitors use positive pad 1 and GND pad 2. These optional replacement prices are already included in the updated **If needed** total; do not add them again.

The purchasing update itself did not change the circuit. The subsequently authorized Fingerprint2 integration is now saved as electrical revision 3, with JP3 and two UART nets; the costs shown in this subsection are historical.


### Archived coordinate snapshot (superseded)

### Retained original component coordinates

These are LIB origins, not body centers. Angles are clockwise relative to the original unrotated electrical snapshot. The v3 plan uses incremental movement from the already-corrected live backup; A1 is not mirrored again and Pi is not rotated again.

| Ref | Origin X (mm) | Origin Y (mm) | Clockwise orientation from original footprint |
| --- | --- | --- | --- |
| A1 | 182.5 | 37 | 0° |
| PI1 | 110.028 | 31.984 | 90° |
| IC1 | 30.028 | 22.303 | -90° |
| IC2 | 159.972 | 18.707 | 90° |
| U1 | 85 | 33 | 0° |
| JP1 | 6 | 55 | -90° |
| JP2 | 48 | 27 | 0° |
| Q1 | 70 | 34 | 0° |
| Q2 | 70 | 39 | 0° |
| C1 | 28.757 | 32 | -90° |
| C2 | 161.243 | 10.2 | 90° |
| C3 | 36.5 | 32 | 0° |
| C4 | 151.5 | 10.5 | 0° |
| C5 | 80 | 33 | 90° |
| C6 | 80 | 39 | 0° |
| C7 | 14 | 39 | 90° |
| C8 | 21 | 39 | 0° |
| R1 | 36 | 20 | -90° |
| R2 | 40 | 20 | -90° |
| R3 | 153 | 22 | -90° |
| R4 | 149 | 22 | -90° |
| R5 | 48.5 | 34 | 0° |
| R6 | 48.5 | 39 | 0° |
| R7 | 60.5 | 34 | 180° |
| R8 | 60.5 | 39 | 180° |

The historical grouped-layout verification checked the original 25 components, 134 electrical pin/net identities, four Pi mounting pads, 12 native NPTH holes, placement reserves, screw clearances and visible artwork. Revision 3 verification checks the new 26-component/138-electrical-pin schematic and PCB, the JP3 addition and preservation of existing geometry and holes. Those historical audits predate the user's newer tracks/vias. They establish the recorded baseline geometry and connectivity, not the current routing status, completed enclosure fit, RF performance, power design or fabrication readiness.



## Current reader-free complete electrical pin appendix

All 134 electrical pins are listed. Physical pad numbers differ from GPIO numbers. The four Pi mounting pads are excluded.

| Component | Pin | Symbol pin name | Current net |
|---|---|---|---|
| A1 | 1 | 3V3 | ESP3V3 |
| A1 | 2 | 01 | SDA_LV |
| A1 | 3 | 02 | NC |
| A1 | 4 | 03 | NC |
| A1 | 5 | 10 | RADIO1_CSN |
| A1 | 6 | 11 | RADIO_MOSI |
| A1 | 7 | 12 | RADIO_SCK |
| A1 | 8 | 13 | RADIO_MISO |
| A1 | 9 | 14 | RADIO1_CE |
| A1 | 10 | 15 | RADIO2_CSN |
| A1 | 11 | GND | GND |
| A1 | 12 | VSYS | NC |
| A1 | 13 | VSYS | NC |
| A1 | 14 | 16 | RADIO2_CE |
| A1 | 15 | 39 | IR_RX |
| A1 | 16 | 3V3 | NC |
| A1 | 17 | 3V3 | ESP3V3 |
| A1 | 18 | GND | GND |
| A1 | 19 | GND | NC |
| A1 | 20 | 40 | IR_TX |
| A1 | 21 | 41 | SCL_LV |
| A1 | 22 | 42 | NC |
| A1 | 23 | 43 | NC |
| A1 | 24 | 44 | NC |
| A1 | 25 | 45 | NC |
| A1 | 26 | 46 | NC |
| A1 | 27 | GND | NC |
| A1 | 28 | GND | NC |
| C1 | 1 | 1 | 3V3_AUX |
| C1 | 2 | 2 | GND |
| C2 | 1 | 1 | 3V3_AUX |
| C2 | 2 | 2 | GND |
| C3 | 1 | 1 | 3V3_AUX |
| C3 | 2 | 2 | GND |
| C4 | 1 | 1 | 3V3_AUX |
| C4 | 2 | 2 | GND |
| C5 | 1 | 1 | +5V_EXT |
| C5 | 2 | 2 | GND |
| C6 | 1 | 1 | +5V_EXT |
| C6 | 2 | 2 | GND |
| C7 | 1 | 1 | 3V3_AUX |
| C7 | 2 | 2 | GND |
| C8 | 1 | 1 | 3V3_AUX |
| C8 | 2 | 2 | GND |
| IC1 | 1 | GND | GND |
| IC1 | 2 | VCC | 3V3_AUX |
| IC1 | 3 | CE | RADIO1_CE |
| IC1 | 4 | CSN | RADIO1_CSN |
| IC1 | 5 | SCK | RADIO_SCK |
| IC1 | 6 | MOSI | RADIO_MOSI |
| IC1 | 7 | MISO | RADIO_MISO |
| IC1 | 8 | IRQ | NC |
| IC2 | 1 | GND | GND |
| IC2 | 2 | VCC | 3V3_AUX |
| IC2 | 3 | CE | RADIO2_CE |
| IC2 | 4 | CSN | RADIO2_CSN |
| IC2 | 5 | SCK | RADIO_SCK |
| IC2 | 6 | MOSI | RADIO_MOSI |
| IC2 | 7 | MISO | RADIO_MISO |
| IC2 | 8 | IRQ | NC |
| JP1 | 1 | IRout | IR_TX |
| JP1 | 2 | IRin | IR_RX |
| JP1 | 3 | GND | GND |
| JP1 | 4 | VIN | 3V3_AUX |
| JP2 | 1 | +5V_EXT | +5V_EXT |
| JP2 | 2 | GND | GND |
| JP2 | 3 | 3V3_AUX | 3V3_AUX |
| JP2 | 4 | GND | GND |
| PI1 | 1 | 3V3 | NC |
| PI1 | 2 | 5V | NC |
| PI1 | 3 | GPIO2 sda | NC |
| PI1 | 4 | 5V | NC |
| PI1 | 5 | GPIO3 scl | NC |
| PI1 | 6 | GND | NC |
| PI1 | 7 | GPIO4 | NC |
| PI1 | 8 | tx GPIO14 | NC |
| PI1 | 9 | GND | NC |
| PI1 | 10 | rx GPIO15 | NC |
| PI1 | 11 | GPIO17 | NC |
| PI1 | 12 | pwm0 GPIO18 | NC |
| PI1 | 13 | GPIO27 | NC |
| PI1 | 14 | GND | NC |
| PI1 | 15 | GPIO22 | NC |
| PI1 | 16 | GPIO23 | NC |
| PI1 | 17 | 3V3 | NC |
| PI1 | 18 | GPIO24 | NC |
| PI1 | 19 | GPIO10 mosi | NC |
| PI1 | 20 | GND | NC |
| PI1 | 21 | GPIO9 miso | NC |
| PI1 | 22 | GPIO25 | NC |
| PI1 | 23 | GPIO11 sck | NC |
| PI1 | 24 | cs0 GPIO8 | NC |
| PI1 | 25 | GND | NC |
| PI1 | 26 | cs1 GPIO7 | NC |
| PI1 | 27 | eeprom sda | NC |
| PI1 | 28 | eeprom scl | NC |
| PI1 | 29 | GPIO5 | NC |
| PI1 | 30 | GND | NC |
| PI1 | 31 | GPIO6 | NC |
| PI1 | 32 | pwm0 GPIO12 | NC |
| PI1 | 33 | GPIO13 pwm1 | NC |
| PI1 | 34 | GND | NC |
| PI1 | 35 | GPIO19 pwm1 | NC |
| PI1 | 36 | GPIO16 | NC |
| PI1 | 37 | GPIO26 | NC |
| PI1 | 38 | GPIO20 | NC |
| PI1 | 39 | GND | NC |
| PI1 | 40 | GPIO21 | NC |
| Q1 | 1 | G | ESP3V3 |
| Q1 | 2 | S | SDA_LV |
| Q1 | 3 | D | KB_SDA |
| Q2 | 1 | G | ESP3V3 |
| Q2 | 2 | S | SCL_LV |
| Q2 | 3 | D | KB_SCL |
| R1 | 1 | 1 | RADIO1_CSN |
| R1 | 2 | 2 | 3V3_AUX |
| R2 | 1 | 1 | RADIO1_CE |
| R2 | 2 | 2 | GND |
| R3 | 1 | 1 | RADIO2_CSN |
| R3 | 2 | 2 | 3V3_AUX |
| R4 | 1 | 1 | RADIO2_CE |
| R4 | 2 | 2 | GND |
| R5 | 1 | 1 | SDA_LV |
| R5 | 2 | 2 | ESP3V3 |
| R6 | 1 | 1 | SCL_LV |
| R6 | 2 | 2 | ESP3V3 |
| R7 | 1 | 1 | KB_SDA |
| R7 | 2 | 2 | +5V_EXT |
| R8 | 1 | 1 | KB_SCL |
| R8 | 2 | 2 | +5V_EXT |
| U1 | 1 | GND | GND |
| U1 | 2 | VCC | +5V_EXT |
| U1 | 3 | SDA | KB_SDA |
| U1 | 4 | SCL | KB_SCL |

## Historical removed Fingerprint2 revision — superseded October 1, 2026

The following 138-pin table belongs to the removed reader interface. JP3, its UART nets and its mechanical extension are not active. GPIO43/44 are NC in the current 134-pin table above. All later appendices below are also historical.



This table contains all 138 electrical pins after microSD removal. GPIO numbers and physical pad numbers differ. All 40 Pi pins are externally NC in this carrier. Four Pi mechanical pads are excluded.

| Component | Pin | Symbol pin name | Current net |
|---|---|---|---|
| A1 | 1 | 3V3 | ESP3V3 |
| A1 | 2 | 01 | SDA_LV |
| A1 | 3 | 02 | NC |
| A1 | 4 | 03 | NC |
| A1 | 5 | 10 | RADIO1_CSN |
| A1 | 6 | 11 | RADIO_MOSI |
| A1 | 7 | 12 | RADIO_SCK |
| A1 | 8 | 13 | RADIO_MISO |
| A1 | 9 | 14 | RADIO1_CE |
| A1 | 10 | 15 | RADIO2_CSN |
| A1 | 11 | GND | GND |
| A1 | 12 | VSYS | NC |
| A1 | 13 | VSYS | NC |
| A1 | 14 | 16 | RADIO2_CE |
| A1 | 15 | 39 | IR_RX |
| A1 | 16 | 3V3 | NC |
| A1 | 17 | 3V3 | ESP3V3 |
| A1 | 18 | GND | GND |
| A1 | 19 | GND | NC |
| A1 | 20 | 40 | IR_TX |
| A1 | 21 | 41 | SCL_LV |
| A1 | 22 | 42 | NC |
| A1 | 23 | 43 | FP_UART_TX |
| A1 | 24 | 44 | FP_UART_RX |
| A1 | 25 | 45 | NC |
| A1 | 26 | 46 | NC |
| A1 | 27 | GND | NC |
| A1 | 28 | GND | NC |
| C1 | 1 | 1 | 3V3_AUX |
| C1 | 2 | 2 | GND |
| C2 | 1 | 1 | 3V3_AUX |
| C2 | 2 | 2 | GND |
| C3 | 1 | 1 | 3V3_AUX |
| C3 | 2 | 2 | GND |
| C4 | 1 | 1 | 3V3_AUX |
| C4 | 2 | 2 | GND |
| C5 | 1 | 1 | +5V_EXT |
| C5 | 2 | 2 | GND |
| C6 | 1 | 1 | +5V_EXT |
| C6 | 2 | 2 | GND |
| C7 | 1 | 1 | 3V3_AUX |
| C7 | 2 | 2 | GND |
| C8 | 1 | 1 | 3V3_AUX |
| C8 | 2 | 2 | GND |
| IC1 | 1 | GND | GND |
| IC1 | 2 | VCC | 3V3_AUX |
| IC1 | 3 | CE | RADIO1_CE |
| IC1 | 4 | CSN | RADIO1_CSN |
| IC1 | 5 | SCK | RADIO_SCK |
| IC1 | 6 | MOSI | RADIO_MOSI |
| IC1 | 7 | MISO | RADIO_MISO |
| IC1 | 8 | IRQ | NC |
| IC2 | 1 | GND | GND |
| IC2 | 2 | VCC | 3V3_AUX |
| IC2 | 3 | CE | RADIO2_CE |
| IC2 | 4 | CSN | RADIO2_CSN |
| IC2 | 5 | SCK | RADIO_SCK |
| IC2 | 6 | MOSI | RADIO_MOSI |
| IC2 | 7 | MISO | RADIO_MISO |
| IC2 | 8 | IRQ | NC |
| JP1 | 1 | IRout | IR_TX |
| JP1 | 2 | IRin | IR_RX |
| JP1 | 3 | GND | GND |
| JP1 | 4 | VIN | 3V3_AUX |
| JP2 | 1 | +5V_EXT | +5V_EXT |
| JP2 | 2 | GND | GND |
| JP2 | 3 | 3V3_AUX | 3V3_AUX |
| JP2 | 4 | GND | GND |
| JP3 | 1 | FP_UART_RX | FP_UART_RX |
| JP3 | 2 | FP_UART_TX | FP_UART_TX |
| JP3 | 3 | +5V_EXT | +5V_EXT |
| JP3 | 4 | GND | GND |
| PI1 | 1 | 3V3 | NC |
| PI1 | 2 | 5V | NC |
| PI1 | 3 | GPIO2 sda | NC |
| PI1 | 4 | 5V | NC |
| PI1 | 5 | GPIO3 scl | NC |
| PI1 | 6 | GND | NC |
| PI1 | 7 | GPIO4 | NC |
| PI1 | 8 | tx GPIO14 | NC |
| PI1 | 9 | GND | NC |
| PI1 | 10 | rx GPIO15 | NC |
| PI1 | 11 | GPIO17 | NC |
| PI1 | 12 | pwm0 GPIO18 | NC |
| PI1 | 13 | GPIO27 | NC |
| PI1 | 14 | GND | NC |
| PI1 | 15 | GPIO22 | NC |
| PI1 | 16 | GPIO23 | NC |
| PI1 | 17 | 3V3 | NC |
| PI1 | 18 | GPIO24 | NC |
| PI1 | 19 | GPIO10 mosi | NC |
| PI1 | 20 | GND | NC |
| PI1 | 21 | GPIO9 miso | NC |
| PI1 | 22 | GPIO25 | NC |
| PI1 | 23 | GPIO11 sck | NC |
| PI1 | 24 | cs0 GPIO8 | NC |
| PI1 | 25 | GND | NC |
| PI1 | 26 | cs1 GPIO7 | NC |
| PI1 | 27 | eeprom sda | NC |
| PI1 | 28 | eeprom scl | NC |
| PI1 | 29 | GPIO5 | NC |
| PI1 | 30 | GND | NC |
| PI1 | 31 | GPIO6 | NC |
| PI1 | 32 | pwm0 GPIO12 | NC |
| PI1 | 33 | GPIO13 pwm1 | NC |
| PI1 | 34 | GND | NC |
| PI1 | 35 | GPIO19 pwm1 | NC |
| PI1 | 36 | GPIO16 | NC |
| PI1 | 37 | GPIO26 | NC |
| PI1 | 38 | GPIO20 | NC |
| PI1 | 39 | GND | NC |
| PI1 | 40 | GPIO21 | NC |
| Q1 | 1 | G | ESP3V3 |
| Q1 | 2 | S | SDA_LV |
| Q1 | 3 | D | KB_SDA |
| Q2 | 1 | G | ESP3V3 |
| Q2 | 2 | S | SCL_LV |
| Q2 | 3 | D | KB_SCL |
| R1 | 1 | 1 | RADIO1_CSN |
| R1 | 2 | 2 | 3V3_AUX |
| R2 | 1 | 1 | RADIO1_CE |
| R2 | 2 | 2 | GND |
| R3 | 1 | 1 | RADIO2_CSN |
| R3 | 2 | 2 | 3V3_AUX |
| R4 | 1 | 1 | RADIO2_CE |
| R4 | 2 | 2 | GND |
| R5 | 1 | 1 | SDA_LV |
| R5 | 2 | 2 | ESP3V3 |
| R6 | 1 | 1 | SCL_LV |
| R6 | 2 | 2 | ESP3V3 |
| R7 | 1 | 1 | KB_SDA |
| R7 | 2 | 2 | +5V_EXT |
| R8 | 1 | 1 | KB_SCL |
| R8 | 2 | 2 | +5V_EXT |
| U1 | 1 | GND | GND |
| U1 | 2 | VCC | +5V_EXT |
| U1 | 3 | SDA | KB_SDA |
| U1 | 4 | SCL | KB_SCL |

## Historical removed Pi SPI1 microSD revision 4 — superseded October 1, 2026

The user explicitly removed this addition and requested no USB substitute. The following 187 rows document the removed circuit only. Its J1/U2/D1/R9–R16/C9–C12, eight Pi assignments, regulator, extra card, software overlay and added copper are not part of the active design. The circuit had a verified saved schematic and a reviewed routed candidate; it was never released for fabrication. The Fingerprint2 mechanical space/holes are retained independently.

| Component | Pin | Symbol pin name | Superseded net |
|---|---|---|---|
| A1 | 1 | 3V3 | ESP3V3 |
| A1 | 2 | 01 | SDA_LV |
| A1 | 3 | 02 | NC |
| A1 | 4 | 03 | NC |
| A1 | 5 | 10 | RADIO1_CSN |
| A1 | 6 | 11 | RADIO_MOSI |
| A1 | 7 | 12 | RADIO_SCK |
| A1 | 8 | 13 | RADIO_MISO |
| A1 | 9 | 14 | RADIO1_CE |
| A1 | 10 | 15 | RADIO2_CSN |
| A1 | 11 | GND | GND |
| A1 | 12 | VSYS | NC |
| A1 | 13 | VSYS | NC |
| A1 | 14 | 16 | RADIO2_CE |
| A1 | 15 | 39 | IR_RX |
| A1 | 16 | 3V3 | NC |
| A1 | 17 | 3V3 | ESP3V3 |
| A1 | 18 | GND | GND |
| A1 | 19 | GND | NC |
| A1 | 20 | 40 | IR_TX |
| A1 | 21 | 41 | SCL_LV |
| A1 | 22 | 42 | NC |
| A1 | 23 | 43 | FP_UART_TX |
| A1 | 24 | 44 | FP_UART_RX |
| A1 | 25 | 45 | NC |
| A1 | 26 | 46 | NC |
| A1 | 27 | GND | NC |
| A1 | 28 | GND | NC |
| C1 | 1 | 1 | 3V3_AUX |
| C1 | 2 | 2 | GND |
| C2 | 1 | 1 | 3V3_AUX |
| C2 | 2 | 2 | GND |
| C3 | 1 | 1 | 3V3_AUX |
| C3 | 2 | 2 | GND |
| C4 | 1 | 1 | 3V3_AUX |
| C4 | 2 | 2 | GND |
| C5 | 1 | 1 | +5V_EXT |
| C5 | 2 | 2 | GND |
| C6 | 1 | 1 | +5V_EXT |
| C6 | 2 | 2 | GND |
| C7 | 1 | 1 | 3V3_AUX |
| C7 | 2 | 2 | GND |
| C8 | 1 | 1 | 3V3_AUX |
| C8 | 2 | 2 | GND |
| C9 | 1 | 1 | PI_5V |
| C9 | 2 | 2 | GND |
| C10 | 1 | 1 | SD_3V3 |
| C10 | 2 | 2 | GND |
| C11 | 1 | 1 | SD_3V3 |
| C11 | 2 | 2 | GND |
| C12 | 1 | 1 | SD_3V3 |
| C12 | 2 | 2 | GND |
| D1 | 1 | IO1 | SD_DAT2 |
| D1 | 2 | IO2 | SD_CS_N |
| D1 | 3 | IO3 | SD_MOSI |
| D1 | 4 | GND | GND |
| D1 | 5 | IO4 | SD_CLK |
| D1 | 6 | IO5 | SD_MISO |
| D1 | 7 | IO6 | SD_DAT1 |
| D1 | 8 | VCC | SD_3V3 |
| IC1 | 1 | GND | GND |
| IC1 | 2 | VCC | 3V3_AUX |
| IC1 | 3 | CE | RADIO1_CE |
| IC1 | 4 | CSN | RADIO1_CSN |
| IC1 | 5 | SCK | RADIO_SCK |
| IC1 | 6 | MOSI | RADIO_MOSI |
| IC1 | 7 | MISO | RADIO_MISO |
| IC1 | 8 | IRQ | NC |
| IC2 | 1 | GND | GND |
| IC2 | 2 | VCC | 3V3_AUX |
| IC2 | 3 | CE | RADIO2_CE |
| IC2 | 4 | CSN | RADIO2_CSN |
| IC2 | 5 | SCK | RADIO_SCK |
| IC2 | 6 | MOSI | RADIO_MOSI |
| IC2 | 7 | MISO | RADIO_MISO |
| IC2 | 8 | IRQ | NC |
| J1 | 1 | DAT2 | SD_DAT2 |
| J1 | 2 | DAT3 / CS_N | SD_CS_N |
| J1 | 3 | CMD / MOSI | SD_MOSI |
| J1 | 4 | VDD | SD_3V3 |
| J1 | 5 | CLK | SD_CLK |
| J1 | 6 | VSS | GND |
| J1 | 7 | DAT0 / MISO | SD_MISO |
| J1 | 8 | DAT1 | SD_DAT1 |
| J1 | A | CD switch A | SD_CD_N |
| J1 | B | CD switch B | GND |
| J1 | SHELL | SHIELD | GND |
| JP1 | 1 | IRout | IR_TX |
| JP1 | 2 | IRin | IR_RX |
| JP1 | 3 | GND | GND |
| JP1 | 4 | VIN | 3V3_AUX |
| JP2 | 1 | +5V_EXT | +5V_EXT |
| JP2 | 2 | GND | GND |
| JP2 | 3 | 3V3_AUX | 3V3_AUX |
| JP2 | 4 | GND | GND |
| JP3 | 1 | FP_UART_RX | FP_UART_RX |
| JP3 | 2 | FP_UART_TX | FP_UART_TX |
| JP3 | 3 | +5V_EXT | +5V_EXT |
| JP3 | 4 | GND | GND |
| PI1 | 1 | 3V3 | PI_3V3 |
| PI1 | 2 | 5V | PI_5V |
| PI1 | 3 | GPIO2 sda | NC |
| PI1 | 4 | 5V | NC |
| PI1 | 5 | GPIO3 scl | NC |
| PI1 | 6 | GND | GND |
| PI1 | 7 | GPIO4 | NC |
| PI1 | 8 | tx GPIO14 | NC |
| PI1 | 9 | GND | NC |
| PI1 | 10 | rx GPIO15 | NC |
| PI1 | 11 | GPIO17 | NC |
| PI1 | 12 | pwm0 GPIO18 | SD_CS_N |
| PI1 | 13 | GPIO27 | NC |
| PI1 | 14 | GND | NC |
| PI1 | 15 | GPIO22 | NC |
| PI1 | 16 | GPIO23 | NC |
| PI1 | 17 | 3V3 | NC |
| PI1 | 18 | GPIO24 | NC |
| PI1 | 19 | GPIO10 mosi | NC |
| PI1 | 20 | GND | NC |
| PI1 | 21 | GPIO9 miso | NC |
| PI1 | 22 | GPIO25 | NC |
| PI1 | 23 | GPIO11 sck | NC |
| PI1 | 24 | cs0 GPIO8 | NC |
| PI1 | 25 | GND | NC |
| PI1 | 26 | cs1 GPIO7 | NC |
| PI1 | 27 | eeprom sda | NC |
| PI1 | 28 | eeprom scl | NC |
| PI1 | 29 | GPIO5 | NC |
| PI1 | 30 | GND | NC |
| PI1 | 31 | GPIO6 | NC |
| PI1 | 32 | pwm0 GPIO12 | NC |
| PI1 | 33 | GPIO13 pwm1 | NC |
| PI1 | 34 | GND | NC |
| PI1 | 35 | GPIO19 pwm1 | SD_MISO |
| PI1 | 36 | GPIO16 | SD_CD_N |
| PI1 | 37 | GPIO26 | NC |
| PI1 | 38 | GPIO20 | SD_MOSI |
| PI1 | 39 | GND | NC |
| PI1 | 40 | GPIO21 | SD_CLK_SRC |
| Q1 | 1 | G | ESP3V3 |
| Q1 | 2 | S | SDA_LV |
| Q1 | 3 | D | KB_SDA |
| Q2 | 1 | G | ESP3V3 |
| Q2 | 2 | S | SCL_LV |
| Q2 | 3 | D | KB_SCL |
| R1 | 1 | 1 | RADIO1_CSN |
| R1 | 2 | 2 | 3V3_AUX |
| R2 | 1 | 1 | RADIO1_CE |
| R2 | 2 | 2 | GND |
| R3 | 1 | 1 | RADIO2_CSN |
| R3 | 2 | 2 | 3V3_AUX |
| R4 | 1 | 1 | RADIO2_CE |
| R4 | 2 | 2 | GND |
| R5 | 1 | 1 | SDA_LV |
| R5 | 2 | 2 | ESP3V3 |
| R6 | 1 | 1 | SCL_LV |
| R6 | 2 | 2 | ESP3V3 |
| R7 | 1 | 1 | KB_SDA |
| R7 | 2 | 2 | +5V_EXT |
| R8 | 1 | 1 | KB_SCL |
| R8 | 2 | 2 | +5V_EXT |
| R9 | 1 | 1 | SD_3V3 |
| R9 | 2 | 2 | SD_MOSI |
| R10 | 1 | 1 | SD_3V3 |
| R10 | 2 | 2 | SD_MISO |
| R11 | 1 | 1 | SD_3V3 |
| R11 | 2 | 2 | SD_DAT1 |
| R12 | 1 | 1 | SD_3V3 |
| R12 | 2 | 2 | SD_DAT2 |
| R13 | 1 | 1 | SD_3V3 |
| R13 | 2 | 2 | SD_CS_N |
| R14 | 1 | 1 | PI_3V3 |
| R14 | 2 | 2 | SD_CD_N |
| R15 | 1 | 1 | PI_3V3 |
| R15 | 2 | 2 | GND |
| R16 | 1 | 1 | SD_CLK_SRC |
| R16 | 2 | 2 | SD_CLK |
| U1 | 1 | GND | GND |
| U1 | 2 | VCC | +5V_EXT |
| U1 | 3 | SDA | KB_SDA |
| U1 | 4 | SCL | KB_SCL |
| U2 | 1 | IN | PI_5V |
| U2 | 2 | OUT 3.3V | SD_3V3 |
| U2 | 3 | GND | GND |
| U2 | 4 | NR (NC) | NC |
| U2 | 5 | EN | PI_3V3 |
| U2 | 6 | TAB / GND | GND |

The following older appendices are unchanged historical records. Current wiring is the 138-pin table above.

## Historical revision 3 electrical design and complete PCB pin appendix

**Historical scope:** the retained text below describes the pre-expansion revision 3 exports. The new 486-pin appendix and four Pi overrides at the end take precedence for the expansion schematic. The fresh PCB backup separately preserves the user's later tracks/vias.


Snapshot documented on 2026-09-30 from project `cyberdeck-completed`, `Sheet_1`, corrected wiring revision 3 including Fingerprint2 via JP3. This describes the saved exports, not later live edits and not a finished enclosure layout.

Sources: [wiring-map-fingerprint.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/wiring-map-fingerprint.json), [schematic-fingerprint.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/schematic-fingerprint.json), [pcb-fingerprint.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/pcb-fingerprint.json), [fingerprint-verification.json](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/fingerprint-verification.json). The schematic and PCB file hashes were checked against the final PASS report; the schematic graph, wiring map, PCB pads and all 138 appendix pin rows were also matched while publishing this summary.

Verified inventory: **26 components; 138 electrical symbol/footprint pins; 85 connected pins on 19 connected nets; 53 externally unconnected pins.** The PCB additionally contains four existing, unconnected non-plated Pi mounting-hole pad records, making **142 physical PAD records**. Those four holes and the 12 native carrier NPTH holes are not additional schematic pins. No reader mounting holes were added.

### Numbering and interpretation

- **A1 pin numbers are symbol/footprint pad numbers, not ESP32 GPIO numbers.** For example, A1 pin 2 is GPIO1, A1 pin 7 is GPIO12, and A1 pin 21 is GPIO41. The A1 table expands numerical symbol labels to identify their GPIO meaning.
- Each table lists the saved symbol/footprint pad number. Compatibility with the actual purchased modules, header orientation and physical dimensions still needs hardware verification.
- `Connected` means an external schematic net is defined. `Unconnected` means no external schematic connection; the PCB assigns a unique singleton name such as `A1_12` or `PI1_1`. These names are not shared nets or proof of electrical isolation inside a module. Module-internal power/ground connections are outside this netlist.
- Polarized capacitors C3/C4/C6/C8 use design pin 1 as positive and pin 2 as negative. Verify actual part markings and footprint orientation. Ceramic C1/C2/C5/C7 are nonpolar.
- JP1 follows the Adafruit module 2.54mm header numbering: 1 IRout, 2 IRin, 3 GND, 4 VIN. Its footprint is not the module's JST socket. JP2 uses its own distinct numbering: 1 +5V_EXT, 2 GND, 3 3V3_AUX, 4 GND.

### Component values and assigned footprints

| Ref | Saved value/model | Assigned footprint | Electrical pins | Function |
| --- | --- | --- | --- | --- |
| A1 | ESP32-S3-AMOLED-1.91 | T-DISPLAY S3 AMOLED | 28 | ESP32-S3 AMOLED module / peripheral controller |
| PI1 | PI ZERO2 WDADAD | RASPBERRY-PIZERO-W | 40 | Raspberry Pi placeholder; all 40 pins externally unwired |
| IC1 | NRF24L01 | NRF24L01 | 8 | Radio 1; shared SPI2, independent CSN/CE |
| IC2 | NRF24L01 | NRF24L01 | 8 | Radio 2; shared SPI2, independent CSN/CE |
| U1 | CardKB Module | NXW-04K | 4 | CardKB connector; external 5V and translated I2C |
| JP1 | Adafruit 5990 IR RX/TX module | HDR-1X4T/2.54/10X2_J9 | 4 | IR module carrier header; Adafruit 0.1in header numbering |
| JP2 | REGULATED POWER INPUT | HDR-1X4T/2.54/10X2_J9 | 4 | External regulated 5V/3.3V input; no regulators implemented |
| JP3 | FINGERPRINT2 UART HEADER | HDR-1X4T/2.54/10X2_J9 | 4 | Fingerprint2 carrier header; 5V, 3.3V UART; Grove adapter/harness required |
| Q1 | BSS138 | BSS138 | 3 | SDA level translator; G1/S2/D3 |
| Q2 | BSS138 | BSS138 | 3 | SCL level translator; G1/S2/D3 |
| C1 | 100nF | CERAMIC CAPACITOR 100NF 50V | 2 | Radio 1 local ceramic bypass |
| C2 | 100nF | CERAMIC CAPACITOR 100NF 50V | 2 | Radio 2 local ceramic bypass |
| C3 | 10uF | CAPACITOR 10UF TH FP | 2 | Radio 1 local polarized bulk capacitor |
| C4 | 10uF | CAPACITOR 10UF TH FP | 2 | Radio 2 local polarized bulk capacitor |
| C5 | 100nF | CERAMIC CAPACITOR 100NF 50V | 2 | CardKB 5V local ceramic bypass |
| C6 | 10uF | CAPACITOR 10UF TH FP | 2 | CardKB 5V local polarized bulk capacitor |
| C7 | 100nF | CERAMIC CAPACITOR 100NF 50V | 2 | IR AUX 3.3V local ceramic bypass |
| C8 | 10uF | CAPACITOR 10UF TH FP | 2 | IR AUX 3.3V local polarized bulk capacitor |
| R1 | 10k | R_AXIAL-0.3 | 2 | Radio 1 CSN pull-up to 3V3_AUX |
| R2 | 10k | R_AXIAL-0.3 | 2 | Radio 1 CE pull-down to GND |
| R3 | 10k | R_AXIAL-0.3 | 2 | Radio 2 CSN pull-up to 3V3_AUX |
| R4 | 10k | R_AXIAL-0.3 | 2 | Radio 2 CE pull-down to GND |
| R5 | 4.7k | R_AXIAL-0.3 | 2 | SDA_LV pull-up to ESP3V3 |
| R6 | 4.7k | R_AXIAL-0.3 | 2 | SCL_LV pull-up to ESP3V3 |
| R7 | 10k | R_AXIAL-0.3 | 2 | KB_SDA pull-up to +5V_EXT |
| R8 | 10k | R_AXIAL-0.3 | 2 | KB_SCL pull-up to +5V_EXT |

Footprint names are saved library assignments, not dimensional validation. The misleading supplier/manufacturer purchasing fields on C1/C2 were cleared; their intended value remains 100nF. Do not restore the old 47pF/3kV/C19375 purchasing metadata. Q1/Q2 use the corrected G1/S2/D3 mapping.

### All 19 connected nets

| Net | Endpoints | Count |
| --- | --- | --- |
| ESP3V3 | A1.1 (3V3), A1.17 (3V3), Q1.1 (G), Q2.1 (G), R5.2 (2), R6.2 (2) | 6 |
| +5V_EXT | JP2.1 (+5V_EXT), U1.2 (VCC), R7.2 (2), R8.2 (2), C5.1 (1), C6.1 (1), JP3.3 (+5V_EXT) | 7 |
| 3V3_AUX | JP2.3 (3V3_AUX), IC1.2 (VCC), IC2.2 (VCC), JP1.4 (VIN), R1.2 (2), R3.2 (2), C1.1 (1), C2.1 (1), C3.1 (1), C4.1 (1), C7.1 (1), C8.1 (1) | 12 |
| GND | A1.11 (GND), A1.18 (GND), JP2.2 (GND), JP2.4 (GND), IC1.1 (GND), IC2.1 (GND), U1.1 (GND), JP1.3 (GND), R2.2 (2), R4.2 (2), C1.2 (2), C2.2 (2), C3.2 (2), C4.2 (2), C5.2 (2), C6.2 (2), C7.2 (2), C8.2 (2), JP3.4 (GND) | 19 |
| RADIO_SCK | A1.7 (12), IC1.5 (SCK), IC2.5 (SCK) | 3 |
| RADIO_MOSI | A1.6 (11), IC1.6 (MOSI), IC2.6 (MOSI) | 3 |
| RADIO_MISO | A1.8 (13), IC1.7 (MISO), IC2.7 (MISO) | 3 |
| RADIO1_CSN | A1.5 (10), IC1.4 (CSN), R1.1 (1) | 3 |
| RADIO1_CE | A1.9 (14), IC1.3 (CE), R2.1 (1) | 3 |
| RADIO2_CSN | A1.10 (15), IC2.4 (CSN), R3.1 (1) | 3 |
| RADIO2_CE | A1.14 (16), IC2.3 (CE), R4.1 (1) | 3 |
| SDA_LV | A1.2 (01), Q1.2 (S), R5.1 (1) | 3 |
| SCL_LV | A1.21 (41), Q2.2 (S), R6.1 (1) | 3 |
| KB_SDA | Q1.3 (D), R7.1 (1), U1.3 (SDA) | 3 |
| KB_SCL | Q2.3 (D), R8.1 (1), U1.4 (SCL) | 3 |
| IR_RX | A1.15 (39), JP1.2 (IRin) | 2 |
| IR_TX | A1.20 (40), JP1.1 (IRout) | 2 |
| FP_UART_TX | A1.23 (43), JP3.2 (FP_UART_TX) | 2 |
| FP_UART_RX | A1.24 (44), JP3.1 (FP_UART_RX) | 2 |

Supply boundaries: ESP3V3 is sourced from the LILYGO 3.3V rail and serves the I2C low-side pull-ups and MOSFET gates. +5V_EXT supplies CardKB, its high-side pull-ups and Fingerprint2 via JP3.3. 3V3_AUX supplies both radios, their CSN pull-ups/decoupling, and IR. All share GND. **No regulators are implemented here; do not parallel 3V3_AUX with A1 3V3, or use A1 VSYS as a presumed regulated 5V source.** Power sequencing/backfeed behavior remains unvalidated; the current annotation calls for coordinated external-rail and ESP32 USB power switching.

Firmware allocation retained by the design: both radios share SPI2 on GPIO12 SCK / GPIO11 MOSI / GPIO13 MISO, with separate CSN GPIO10/15 and CE GPIO14/16; display allocation is SPI3. CardKB uses Wire1, SDA GPIO1, SCL GPIO41, at 100kHz. IR receive is GPIO39; IR transmit control is GPIO40. Fingerprint UART uses Serial1 at 115200 baud, 8N1, with TX GPIO43 and RX GPIO44; native USB is intended for logging/programming. These are intended firmware settings, not tested operation.

### A1 — all 28 LILYGO header pins

| Ref | Symbol / pad pin | Saved label / meaning | PCB net | Status |
| --- | --- | --- | --- | --- |
| A1 | 1 | 3V3 | ESP3V3 | Connected |
| A1 | 2 | 01 (GPIO1) | SDA_LV | Connected |
| A1 | 3 | 02 (GPIO2) | A1_3 | Unconnected |
| A1 | 4 | 03 (GPIO3) | A1_4 | Unconnected |
| A1 | 5 | 10 (GPIO10) | RADIO1_CSN | Connected |
| A1 | 6 | 11 (GPIO11) | RADIO_MOSI | Connected |
| A1 | 7 | 12 (GPIO12) | RADIO_SCK | Connected |
| A1 | 8 | 13 (GPIO13) | RADIO_MISO | Connected |
| A1 | 9 | 14 (GPIO14) | RADIO1_CE | Connected |
| A1 | 10 | 15 (GPIO15) | RADIO2_CSN | Connected |
| A1 | 11 | GND | GND | Connected |
| A1 | 12 | VSYS | A1_12 | Unconnected |
| A1 | 13 | VSYS | A1_13 | Unconnected |
| A1 | 14 | 16 (GPIO16) | RADIO2_CE | Connected |
| A1 | 15 | 39 (GPIO39) | IR_RX | Connected |
| A1 | 16 | 3V3 | A1_16 | Unconnected |
| A1 | 17 | 3V3 | ESP3V3 | Connected |
| A1 | 18 | GND | GND | Connected |
| A1 | 19 | GND | A1_19 | Unconnected |
| A1 | 20 | 40 (GPIO40) | IR_TX | Connected |
| A1 | 21 | 41 (GPIO41) | SCL_LV | Connected |
| A1 | 22 | 42 (GPIO42) | A1_22 | Unconnected |
| A1 | 23 | 43 (GPIO43) | FP_UART_TX | Connected |
| A1 | 24 | 44 (GPIO44) | FP_UART_RX | Connected |
| A1 | 25 | 45 (GPIO45) | A1_25 | Unconnected |
| A1 | 26 | 46 (GPIO46) | A1_26 | Unconnected |
| A1 | 27 | GND | A1_27 | Unconnected |
| A1 | 28 | GND | A1_28 | Unconnected |

### PI1 — all 40 Raspberry Pi header pins

| Ref | Symbol / pad pin | Saved label / meaning | PCB net | Status |
| --- | --- | --- | --- | --- |
| PI1 | 1 | 3V3 | PI1_1 | Unconnected |
| PI1 | 2 | 5V | PI1_2 | Unconnected |
| PI1 | 3 | GPIO2 sda | PI1_3 | Unconnected |
| PI1 | 4 | 5V | PI1_4 | Unconnected |
| PI1 | 5 | GPIO3 scl | PI1_5 | Unconnected |
| PI1 | 6 | GND | PI1_6 | Unconnected |
| PI1 | 7 | GPIO4 | PI1_7 | Unconnected |
| PI1 | 8 | tx GPIO14 | PI1_8 | Unconnected |
| PI1 | 9 | GND | PI1_9 | Unconnected |
| PI1 | 10 | rx GPIO15 | PI1_10 | Unconnected |
| PI1 | 11 | GPIO17 | PI1_11 | Unconnected |
| PI1 | 12 | pwm0 GPIO18 | PI1_12 | Unconnected |
| PI1 | 13 | GPIO27 | PI1_13 | Unconnected |
| PI1 | 14 | GND | PI1_14 | Unconnected |
| PI1 | 15 | GPIO22 | PI1_15 | Unconnected |
| PI1 | 16 | GPIO23 | PI1_16 | Unconnected |
| PI1 | 17 | 3V3 | PI1_17 | Unconnected |
| PI1 | 18 | GPIO24 | PI1_18 | Unconnected |
| PI1 | 19 | GPIO10 mosi | PI1_19 | Unconnected |
| PI1 | 20 | GND | PI1_20 | Unconnected |
| PI1 | 21 | GPIO9 miso | PI1_21 | Unconnected |
| PI1 | 22 | GPIO25 | PI1_22 | Unconnected |
| PI1 | 23 | GPIO11 sck | PI1_23 | Unconnected |
| PI1 | 24 | cs0 GPIO8 | PI1_24 | Unconnected |
| PI1 | 25 | GND | PI1_25 | Unconnected |
| PI1 | 26 | cs1 GPIO7 | PI1_26 | Unconnected |
| PI1 | 27 | eeprom sda | PI1_27 | Unconnected |
| PI1 | 28 | eeprom scl | PI1_28 | Unconnected |
| PI1 | 29 | GPIO5 | PI1_29 | Unconnected |
| PI1 | 30 | GND | PI1_30 | Unconnected |
| PI1 | 31 | GPIO6 | PI1_31 | Unconnected |
| PI1 | 32 | pwm0 GPIO12 | PI1_32 | Unconnected |
| PI1 | 33 | GPIO13 pwm1 | PI1_33 | Unconnected |
| PI1 | 34 | GND | PI1_34 | Unconnected |
| PI1 | 35 | GPIO19 pwm1 | PI1_35 | Unconnected |
| PI1 | 36 | GPIO16 | PI1_36 | Unconnected |
| PI1 | 37 | GPIO26 | PI1_37 | Unconnected |
| PI1 | 38 | GPIO20 | PI1_38 | Unconnected |
| PI1 | 39 | GND | PI1_39 | Unconnected |
| PI1 | 40 | GPIO21 | PI1_40 | Unconnected |

### IC1/IC2 — both radio headers

| Ref | Symbol / pad pin | Saved label / meaning | PCB net | Status |
| --- | --- | --- | --- | --- |
| IC1 | 1 | GND | GND | Connected |
| IC1 | 2 | VCC | 3V3_AUX | Connected |
| IC1 | 3 | CE | RADIO1_CE | Connected |
| IC1 | 4 | CSN | RADIO1_CSN | Connected |
| IC1 | 5 | SCK | RADIO_SCK | Connected |
| IC1 | 6 | MOSI | RADIO_MOSI | Connected |
| IC1 | 7 | MISO | RADIO_MISO | Connected |
| IC1 | 8 | IRQ | IC1_8 | Unconnected |
| IC2 | 1 | GND | GND | Connected |
| IC2 | 2 | VCC | 3V3_AUX | Connected |
| IC2 | 3 | CE | RADIO2_CE | Connected |
| IC2 | 4 | CSN | RADIO2_CSN | Connected |
| IC2 | 5 | SCK | RADIO_SCK | Connected |
| IC2 | 6 | MOSI | RADIO_MOSI | Connected |
| IC2 | 7 | MISO | RADIO_MISO | Connected |
| IC2 | 8 | IRQ | IC2_8 | Unconnected |

### U1, JP1 and JP2 — keyboard, IR and regulated power connectors

| Ref | Symbol / pad pin | Saved label / meaning | PCB net | Status |
| --- | --- | --- | --- | --- |
| U1 | 1 | GND | GND | Connected |
| U1 | 2 | VCC | +5V_EXT | Connected |
| U1 | 3 | SDA | KB_SDA | Connected |
| U1 | 4 | SCL | KB_SCL | Connected |
| JP1 | 1 | IRout | IR_TX | Connected |
| JP1 | 2 | IRin | IR_RX | Connected |
| JP1 | 3 | GND | GND | Connected |
| JP1 | 4 | VIN | 3V3_AUX | Connected |
| JP2 | 1 | +5V_EXT | +5V_EXT | Connected |
| JP2 | 2 | GND | GND | Connected |
| JP2 | 3 | 3V3_AUX | 3V3_AUX | Connected |
| JP2 | 4 | GND | GND | Connected |

### JP3 — Fingerprint2 carrier header

| Ref | Symbol / pad pin | Saved label / meaning | PCB net | Status |
| --- | --- | --- | --- | --- |
| JP3 | 1 | FP_UART_RX | FP_UART_RX | Connected |
| JP3 | 2 | FP_UART_TX | FP_UART_TX | Connected |
| JP3 | 3 | +5V_EXT | +5V_EXT | Connected |
| JP3 | 4 | GND | GND | Connected |

JP3 is a generic 2.54 mm header. Cable mapping to Fingerprint2: white reader TX → pin 1 → ESP GPIO44; yellow reader RX ← pin 2 ← ESP GPIO43; red 5V → pin 3; black GND → pin 4. The included HY2.0-4P Grove cable needs a compatible adapter/harness; it does not directly mate with this footprint. Net TX/RX names describe the ESP direction.

### Q1/Q2 — I2C level-translator transistors

| Ref | Symbol / pad pin | Saved label / meaning | PCB net | Status |
| --- | --- | --- | --- | --- |
| Q1 | 1 | G | ESP3V3 | Connected |
| Q1 | 2 | S | SDA_LV | Connected |
| Q1 | 3 | D | KB_SDA | Connected |
| Q2 | 1 | G | ESP3V3 | Connected |
| Q2 | 2 | S | SCL_LV | Connected |
| Q2 | 3 | D | KB_SCL | Connected |

### C1–C8 — all capacitor terminals

| Ref | Symbol / pad pin | Saved label / meaning | PCB net | Status |
| --- | --- | --- | --- | --- |
| C1 | 1 | 1 | 3V3_AUX | Connected |
| C1 | 2 | 2 | GND | Connected |
| C2 | 1 | 1 | 3V3_AUX | Connected |
| C2 | 2 | 2 | GND | Connected |
| C3 | 1 | 1 (positive +) | 3V3_AUX | Connected |
| C3 | 2 | 2 (negative -) | GND | Connected |
| C4 | 1 | 1 (positive +) | 3V3_AUX | Connected |
| C4 | 2 | 2 (negative -) | GND | Connected |
| C5 | 1 | 1 | +5V_EXT | Connected |
| C5 | 2 | 2 | GND | Connected |
| C6 | 1 | 1 (positive +) | +5V_EXT | Connected |
| C6 | 2 | 2 (negative -) | GND | Connected |
| C7 | 1 | 1 | 3V3_AUX | Connected |
| C7 | 2 | 2 | GND | Connected |
| C8 | 1 | 1 (positive +) | 3V3_AUX | Connected |
| C8 | 2 | 2 (negative -) | GND | Connected |

### R1–R8 — all resistor terminals

| Ref | Symbol / pad pin | Saved label / meaning | PCB net | Status |
| --- | --- | --- | --- | --- |
| R1 | 1 | 1 | RADIO1_CSN | Connected |
| R1 | 2 | 2 | 3V3_AUX | Connected |
| R2 | 1 | 1 | RADIO1_CE | Connected |
| R2 | 2 | 2 | GND | Connected |
| R3 | 1 | 1 | RADIO2_CSN | Connected |
| R3 | 2 | 2 | 3V3_AUX | Connected |
| R4 | 1 | 1 | RADIO2_CE | Connected |
| R4 | 2 | 2 | GND | Connected |
| R5 | 1 | 1 | SDA_LV | Connected |
| R5 | 2 | 2 | ESP3V3 | Connected |
| R6 | 1 | 1 | SCL_LV | Connected |
| R6 | 2 | 2 | ESP3V3 | Connected |
| R7 | 1 | 1 | KB_SDA | Connected |
| R7 | 2 | 2 | +5V_EXT | Connected |
| R8 | 1 | 1 | KB_SCL | Connected |
| R8 | 2 | 2 | +5V_EXT | Connected |

### Historical revision 2 outline, layers and placement status (superseded mechanically)

The historical `pcb-corrected.json` outline was one closed rectangular TRACK on layer **10 (BoardOutLine)**, ID `gge32811`. Its vertices, in internal file coordinates, are:

```text
4047.559 3047.847 4606.613 3047.847 4606.613 3417.925 4047.559 3417.925 4047.559 3047.847
```

Bounds: X 4047.559 to 4606.613; Y 3047.847 to 3417.925. Width = 559.054 internal units; height = 370.078 internal units. At 0.254mm per internal unit, the stored geometry is **141.999716mm × 93.999812mm**, nominally **142mm × 94mm**. The small fractional difference is coordinate rounding in the saved export. This historical outline was first replaced by a 140 × 95 mm R5 outline and subsequently by the current 190 × 110 mm R5 outline; it is retained here only as a record of the electrical correction snapshot. Its boundary stroke width is 0.254mm; the nominal dimensions above describe the boundary coordinates, not added stroke width.

Unit-conversion evidence in the local file: the canvas display unit is `mm`, but internal coordinates are not millimetres. JP1's assigned `HDR-1X4T/2.54/10X2_J9` footprint has adjacent pad centres at X4218.937 and X4228.937, a 10-unit pitch corresponding to its 2.54mm pitch. R1's `R_AXIAL-0.3` footprint has a 30-unit pin-centre separation, corresponding to 0.3in = 7.62mm. Both support 1 internal unit = 0.01in = 10mil = 0.254mm; multiplying raw outline coordinates by 1mm would be wrong.

| Saved layer / item | Meaning and actual saved use |
| --- | --- |
| 1 TopLayer | All 25 component instances are on this side; six SMD pads belong to Q1/Q2. No copper traces. |
| 2 BottomLayer | Defined in the file; no bottom copper traces. |
| 3 TopSilkLayer | 100 footprint TRACK graphics plus component text/other footprint graphics; these are not copper routing. |
| 10 BoardOutLine | One closed rectangular boundary TRACK, unchanged from the before-corrections backup. |
| 11 Multi-Layer | 132 through-hole/mounting PAD records, including the four non-plated Pi holes. |
| 12 Document | Nine footprint TRACK graphics, plus some documentation graphics; not copper routing. |
| 21–52 inner-layer definitions | Present as disabled layer definitions. Their existence does not establish a manufactured multilayer stack-up. |
| Other footprint display layers | 99 ComponentShapeLayer and 100 LeadShapeLayer carry display/model graphics; they are not routed copper. |
| Routing state | Zero copper-layer TRACKs, zero other non-pad copper shapes, and zero vias in the verified saved export. |

In the historical revision 2 export, all 25 component anchors and all 138 physical pad centres were outside that old board rectangle, below it in saved Y coordinates. The footprints are parked for later placement. No routing was performed. That historical placement was not the clamshell mechanical layout, and decoupling adjacency is not yet implemented physically. All original 15 component anchors, rotations, pad geometry and the outline were preserved during correction; C1/C2 internal pad IDs were regenerated by EasyEDA without physical geometry changes. The ten added components are parked separately.

The following table preserves the historical revision 2 placement snapshot for comparison; the latest positions are in `pcb-fingerprint.json` and the current-placement section above; the older outline-pass positions remain in `pcb-rounded-outline.json`. X/Y are internal EasyEDA units, not millimetres; they are file origins, not recommended positions in the enclosure. Every listed rotation is 0 degrees and side is TopLayer (1).

| Ref | Saved origin X | Saved origin Y | Rotation (degrees) | Side |
| --- | --- | --- | --- | --- |
| A1 | 4050 | 3437.54 | 0 | Top (1) |
| PI1 | 4159.9372 | 3555.54 | 0 | Top (1) |
| IC1 | 4072.4671 | 3780.925 | 0 | Top (1) |
| IC2 | 4142.4671 | 3780.925 | 0 | Top (1) |
| U1 | 4160 | 3577.54 | 0 | Top (1) |
| JP1 | 4233.937 | 3588.54 | 0 | Top (1) |
| JP2 | 4651.5 | 3844.5 | 0 | Top (1) |
| Q1 | 4376.9685 | 3584.54 | 0 | Top (1) |
| Q2 | 4714.5 | 3880.5 | 0 | Top (1) |
| C1 | 4335 | 3582.54 | 0 | Top (1) |
| C2 | 4355 | 3582.54 | 0 | Top (1) |
| C3 | 4278.5 | 3600 | 0 | Top (1) |
| C4 | 4309.843 | 3587.54 | 0 | Top (1) |
| C5 | 4672.5 | 3798.5 | 0 | Top (1) |
| C6 | 4617.5 | 3803.5 | 0 | Top (1) |
| C7 | 4612.5 | 3838.5 | 0 | Top (1) |
| C8 | 4647.5 | 3803.5 | 0 | Top (1) |
| R1 | 4178.9 | 3631.54 | 0 | Top (1) |
| R2 | 4228.9 | 3631.54 | 0 | Top (1) |
| R3 | 4278.9 | 3631.54 | 0 | Top (1) |
| R4 | 4328.9 | 3631.54 | 0 | Top (1) |
| R5 | 4706.5 | 3797.5 | 0 | Top (1) |
| R6 | 4706.5 | 3827.5 | 0 | Top (1) |
| R7 | 4626.5 | 3877.5 | 0 | Top (1) |
| R8 | 4676.5 | 3877.5 | 0 | Top (1) |

A1 silkscreen was corrected without moving pads: `gge30150` near pad12 and `gge30156` near pad13 now read VSYS; `gge30174` near pad16 now reads 3V3. The final save also normalized 20 new-component text mirror flags from empty to 0; that is not a placement or connectivity change.

### Four additional Pi mounting-hole records

PI1 has four pre-existing non-plated, unconnected PAD records all numbered 41 in the footprint. They are excluded from the current 138 electrical-pin tables because no corresponding schematic pin exists. The coordinates immediately below are the historical revision 2 positions; current hole coordinates are in the mounting section above. They were preserved unchanged and have empty net fields.

| Ref | Footprint pad label | X (internal) | Y (internal) | Net | Plated |
| --- | --- | --- | --- | --- | --- |
| PI1 | 41 | 4174.09 | 3541.091 | None | No |
| PI1 | 41 | 4174.09 | 3450.54 | None | No |
| PI1 | 41 | 4402.437 | 3541.091 | None | No |
| PI1 | 41 | 4402.437 | 3450.54 | None | No |

### Verification boundary

The historical revision 2 export passed connectivity and preservation checks: 25 components, 17 nets, 79 connected electrical pins, 55 unused electrical singleton pins, correct pad mapping, preserved original placement/outline and corrected A1 silkscreen. That PASS is not approval of actual hardware compatibility, regulator/current budget, independent power sequencing, final board placement, antenna spacing/keepouts, enclosure clearances, firmware, or manufacturing readiness. The user retains PCB placement and trace-routing control.

Revision 3 appendix checks: all **138 electrical pin rows** were matched one-to-one to the saved schematic pins, independently reconstructed schematic graph, PCB pad numbers and wiring map. All **26 component references** match between schematic and PCB; the four non-electrical Pi mounting pads are counted separately. The 53 unconnected electrical pins are all 40 PI1 pins, IC1/IC2 IRQ pin 8, and A1 pins **3, 4, 12, 13, 16, 19, 22, 25, 26, 27, 28**. JP3 adds four connected pins and GPIO43/44 add two previously unused A1 pins to the connected inventory. Source files and IDs were not modified by this summary update.


## Historical custom USB expansion pin appendix — superseded October 1, 2026

**Not current wiring.** All 486 rows and four Pi-console overrides below belong to the canceled custom expansion. The retained HAT-based carrier uses the revision 3 mapping above; these overrides do not apply. Earlier statements below describe their historical snapshot only.

### Archived expansion context

The eight-sheet schematic and later 200 × 150 mm placement remain preserved as work history. The larger board, its 133 added components, five added mounting holes, additional microSD and independent USB-C-console circuits are outside the current rollback scope. The section below was written before that PCB placement; its “unapplied” wording is historical, not the current restoration status.


The saved [eight-page native EasyEDA export](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/cyberdeck-usb-expansion-easyeda.json) adds a **LAN9514** hub/Ethernet controller and a **USB2642** hub/card-reader controller. LAN9514 downstream ports 2, 3 and 4 feed USB-A1, USB-A2 and USB-A3. Its port 5 feeds the USB2642; that device's internal card reader supplies the additional microSD interface and its physical port 2 supplies USB-A4. Thus four external USB-A ports remain available. The extra microSD socket is removable storage, separate from the Pi's existing boot card. The spare USB2642 physical downstream port is left unwired; final configuration must account for it.

Provisional accessory allocation remains ALFA, Chameleon, LILYGO and one spare. Four **Adafruit #4055 USB 2.0 panel-mount cables** allow the female ports to be mounted in the case. The user permits removing the internal male ends and soldering to the carrier's VBUS, D−, D+, GND and shield connections. Preserve the twisted pair and shield until the short termination, provide strain relief, and verify conductor functions by continuity. These data links are not ordinary loose Dupont-wire connections. The Pi upstream data connection uses its **USB OTG connector or appropriate USB test pads**, not its 40-pin GPIO header; Pi host-role configuration and cable/ID behavior still need validation.

The LAN9514's integrated Ethernet PHY connects locally to the selected **Pulse J0011D01BNL MagJack**. An Ethernet-rated patch extension can bring the outside port to the case. The previous three-port Waveshare HAT is superseded as the target implementation. No PoE function is designed.

The exterior USB-C connection is a separate **Adafruit CP2102N Friend #5335 USB-to-3.3V-UART console**, with destination-powered buffer isolation. It provides a Pi serial terminal while the USB hub remains active; Ethernet/SSH is the normal network coding/file-transfer route. It is not a native USB networking/flashing port, and a downstream hub socket cannot itself turn the host Pi into a USB device. The draft assigns Pi header **1=PI_3V3, 6=GND, 8=PI_UART_TX (GPIO14), 10=PI_UART_RX (GPIO15)**. These changes are schematic-only and supersede the corresponding four NC entries in the historical pin appendix. Pi console configuration and testing remain pending.

The draft adds a dedicated **AP63203 2A +3V3_HUB regulator** from regulated +5V_EXT, LAN/SD decoupling, shared reset supervision, oscillator circuits, Ethernet termination, and separately protected/current-limited USB-A power. Keep +3V3_HUB separate from ESP3V3, 3V3_AUX and PI_3V3. Four USB 2.0 ports are allocated up to 500 mA each; the complete source, input connector, wiring, Pi/display/radio load and transient budget are not yet validated. The existing JP2 input is not automatically rated for this expanded load. Pi upstream VBUS is sensed separately and must not be fed from local +5V_EXT; PC USB-C VBUS likewise does not power the deck.

### Eight pages and their scope

| Page | Components | Schematic pins | Purpose |
|---|---:|---:|---|
| 01 Existing carrier and Pi | 26 | 138 | Existing circuit, plus four Pi header assignments |
| 02 Hub controller and Pi USB | 20 | 119 | LAN9514, Pi upstream data, clock/reset/configuration |
| 03 Hub power and decoupling | 27 | 58 | Dedicated regulator and controller supply networks |
| 04 Ethernet MagJack | 9 | 30 | PHY termination, magnetics, RJ45 and LEDs |
| 05 USB-A ports 1 to 3 | 24 | 81 | Three protected/switched panel-cable interfaces |
| 06 microSD controller and socket | 15 | 101 | USB2642, extra storage socket and configuration |
| 07 microSD decoupling and USB-A4 | 25 | 61 | Reader supplies and fourth protected/switched USB-A |
| 08 USB-C serial console | 13 | 36 | Separate USB-C UART module and power-off isolation |
| Total | 159 | 624 | One proposed circuit across eight pages |

The final live export's source graph and all new pin mappings passed the independent audit, including all original components and the four intended Pi changes. The saved eight-page project was also reviewed in EasyEDA. These checks establish saved schematic identities/connections, not correct physical footprints, high-speed signal integrity, complete power design or a fabrication-ready PCB. DNP parts remain in the schematic and pin appendix; their population/configuration choices are not completed by counting the pins.

### Mechanical proposal remains unapplied

A **200 × 150 mm carrier is proposed, not applied**. The saved 190 × 110 mm layout includes JP3 but does not provide a complete bay or matching mount for the actual fingerprint reader. The reader proposal remains landscape at **X112–152/Y111–135 mm**, Grove facing left, with mounting centers **(124,115)** and **(124,131) mm**. The reader's two Ø4.85 mm case holes have verified 16 mm spacing; carrier M3 clearance diameter, washers/spacers, mounting stack and case cutout remain pending. No reader holes have been added. The proposed coordinates fall beyond the current carrier's Y110 front edge and cannot be treated as a placement on the existing outline.

Keep CardKB left, the Pi between keyboard and LILYGO with their long axes parallel, and LILYGO screen-up on the right. Chameleon and loose wires may occupy the keyboard underside; carrier components, headers and the Pi must stay out of that reserved space. Keep the IR-only left strip, rear-middle ALFA bay, three folding antennas, left-side power-bank hooks, lid display/window and hinge cable clearance. Panel-mounted ports reduce reliance on the old HAT's socket positions but do not establish plug, bend, finger-access or enclosure fit. Existing frame holes are not a measured CardKB hole pattern, and new reader/port/frame geometry remains CAD and fit-validation work.

See the [redesign plan](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/usb-ethernet-redesign-plan.md) and [layout proposal](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/usb-ethernet-layout-proposal.svg) for the earlier mechanical proposal. Their circuit-selection statements are superseded by the current schematic draft; their proposed outline and reader bay remain unapplied.


### Archived expansion pin tables

This is the full draft pin record generated from [usb-expansion-pin-map.csv](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/usb-expansion-pin-map.csv) and checked against the [component map](C:/Users/matth/Documents/Codex/2026-09-29/cyberdeck-electrical-engineering/outputs/usb-expansion-component-map.json). It covers **133 new components and 486 new pins**, including explicit NC pins and DNP component pins. These are schematic pins, not verified PCB footprint pads. `FIT` indicates intended population in this draft; `DNP` means the component is present in the circuit documentation but not populated for the stated initial configuration. The source net name, not page position or wire color, is the connection authority.

### Four changes to existing Pi header pins

| Existing reference | Physical header pin | Previous revision 3 state | Draft net | Function |
|---|---:|---|---|---|
| PI1 | 1 | NC | PI_3V3 | Pi 3.3V supply for destination-powered console buffer |
| PI1 | 6 | NC | GND | Common console ground |
| PI1 | 8 | NC | PI_UART_TX | GPIO14/TXD from Pi, toward bridge RX through buffer |
| PI1 | 10 | NC | PI_UART_RX | GPIO15/RXD into Pi, from bridge TX through buffer |

The other 134 baseline electrical pins retain their revision 3 mapping. The Pi's other 36 header pins remain NC. Its upstream USB D+/D− use a separate OTG/test-pad harness and are not carried on these header pins. These four overrides have not been applied to the physical PCB.

### Complete new-pin table

| Ref | Logical ref | Part | Pin | Pin name | Net | Assembly |
|---|---|---|---|---|---|---|
| U100 | U_HUB | LAN9514-JZX | 1 | USBDM2 | USBA1_DM | FIT |
| U100 | U_HUB | LAN9514-JZX | 2 | USBDP2 | USBA1_DP | FIT |
| U100 | U_HUB | LAN9514-JZX | 3 | USBDM3 | USBA2_DM | FIT |
| U100 | U_HUB | LAN9514-JZX | 4 | USBDP3 | USBA2_DP | FIT |
| U100 | U_HUB | LAN9514-JZX | 5 | VDD33A | +3V3_HUB_A | FIT |
| U100 | U_HUB | LAN9514-JZX | 6 | USBDM4 | USBA3_DM | FIT |
| U100 | U_HUB | LAN9514-JZX | 7 | USBDP4 | USBA3_DP | FIT |
| U100 | U_HUB | LAN9514-JZX | 8 | USBDM5 | HUB_TO_SD_DM | FIT |
| U100 | U_HUB | LAN9514-JZX | 9 | USBDP5 | HUB_TO_SD_DP | FIT |
| U100 | U_HUB | LAN9514-JZX | 10 | VDD33A | +3V3_HUB_A | FIT |
| U100 | U_HUB | LAN9514-JZX | 11 | VBUS_DET | PI_VBUS_DET | FIT |
| U100 | U_HUB | LAN9514-JZX | 12 | nRESET | RESET_HUB_N | FIT |
| U100 | U_HUB | LAN9514-JZX | 13 | TEST1 | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 14 | PRTCTL2 | USBA1_CTL | FIT |
| U100 | U_HUB | LAN9514-JZX | 15 | VDD18CORE | LAN_1V8_CORE | FIT |
| U100 | U_HUB | LAN9514-JZX | 16 | PRTCTL3 | USBA2_CTL | FIT |
| U100 | U_HUB | LAN9514-JZX | 17 | PRTCTL4 | USBA3_CTL | FIT |
| U100 | U_HUB | LAN9514-JZX | 18 | PRTCTL5 | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 19 | VDD33IO | +3V3_HUB | FIT |
| U100 | U_HUB | LAN9514-JZX | 20 | nFDX_LED/GPIO0 | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 21 | nLNKA_LED/GPIO1 | ETH_LINK_N | FIT |
| U100 | U_HUB | LAN9514-JZX | 22 | nSPD_LED/GPIO2 | ETH_SPEED_N | FIT |
| U100 | U_HUB | LAN9514-JZX | 23 | EECLK | LAN_EECLK | FIT |
| U100 | U_HUB | LAN9514-JZX | 24 | EECS | LAN_EECS | FIT |
| U100 | U_HUB | LAN9514-JZX | 25 | EEDO | LAN_EEDO | FIT |
| U100 | U_HUB | LAN9514-JZX | 26 | EEDI | LAN_EEDI | FIT |
| U100 | U_HUB | LAN9514-JZX | 27 | VDD33IO | +3V3_HUB | FIT |
| U100 | U_HUB | LAN9514-JZX | 28 | nTRST | +3V3_HUB | FIT |
| U100 | U_HUB | LAN9514-JZX | 29 | TMS | +3V3_HUB | FIT |
| U100 | U_HUB | LAN9514-JZX | 30 | TDI | +3V3_HUB | FIT |
| U100 | U_HUB | LAN9514-JZX | 31 | TDO | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 32 | TCK | LAN_TCK | FIT |
| U100 | U_HUB | LAN9514-JZX | 33 | VDD33IO | +3V3_HUB | FIT |
| U100 | U_HUB | LAN9514-JZX | 34 | TEST2 | GND | FIT |
| U100 | U_HUB | LAN9514-JZX | 35 | GPIO3 | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 36 | GPIO4 | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 37 | GPIO5 | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 38 | VDD18CORE | LAN_1V8_CORE | FIT |
| U100 | U_HUB | LAN9514-JZX | 39 | VDD33IO | +3V3_HUB | FIT |
| U100 | U_HUB | LAN9514-JZX | 40 | TEST3 | +3V3_HUB | FIT |
| U100 | U_HUB | LAN9514-JZX | 41 | AUTOMDIX_EN | LAN_AUTO_MDIX | FIT |
| U100 | U_HUB | LAN9514-JZX | 42 | GPIO6 | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 43 | GPIO7 | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 44 | CLK24_EN | LAN_CLK24_EN | FIT |
| U100 | U_HUB | LAN9514-JZX | 45 | CLK24_OUT | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 46 | VDD33IO | +3V3_HUB | FIT |
| U100 | U_HUB | LAN9514-JZX | 47 | TEST4 | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 48 | VDD18ETHPLL | LAN_1V8_ETHPLL | FIT |
| U100 | U_HUB | LAN9514-JZX | 49 | VDD33A | +3V3_HUB_A | FIT |
| U100 | U_HUB | LAN9514-JZX | 50 | EXRES | LAN_EXRES | FIT |
| U100 | U_HUB | LAN9514-JZX | 51 | VDD33A | +3V3_HUB_A | FIT |
| U100 | U_HUB | LAN9514-JZX | 52 | RXP | ETH_RXP | FIT |
| U100 | U_HUB | LAN9514-JZX | 53 | RXN | ETH_RXN | FIT |
| U100 | U_HUB | LAN9514-JZX | 54 | VDD33A | +3V3_HUB_A | FIT |
| U100 | U_HUB | LAN9514-JZX | 55 | TXP | ETH_TXP | FIT |
| U100 | U_HUB | LAN9514-JZX | 56 | TXN | ETH_TXN | FIT |
| U100 | U_HUB | LAN9514-JZX | 57 | VDD33A | +3V3_HUB_A | FIT |
| U100 | U_HUB | LAN9514-JZX | 58 | USBDM0 | PI_USB_DM | FIT |
| U100 | U_HUB | LAN9514-JZX | 59 | USBDP0 | PI_USB_DP | FIT |
| U100 | U_HUB | LAN9514-JZX | 60 | XO | NC | FIT |
| U100 | U_HUB | LAN9514-JZX | 61 | XI | LAN_CLK25 | FIT |
| U100 | U_HUB | LAN9514-JZX | 62 | VDD18USBPLL | LAN_1V8_USBPLL | FIT |
| U100 | U_HUB | LAN9514-JZX | 63 | USBRBIAS | LAN_USBRBIAS | FIT |
| U100 | U_HUB | LAN9514-JZX | 64 | VDD33A | +3V3_HUB_A | FIT |
| U100 | U_HUB | LAN9514-JZX | 65 | VSS_EP | GND | FIT |
| U101 | U_HUB_BUCK | AP63203WU-7 | 1 | FB | +3V3_HUB | FIT |
| U101 | U_HUB_BUCK | AP63203WU-7 | 2 | EN | +5V_EXT | FIT |
| U101 | U_HUB_BUCK | AP63203WU-7 | 3 | VIN | +5V_EXT | FIT |
| U101 | U_HUB_BUCK | AP63203WU-7 | 4 | GND | GND | FIT |
| U101 | U_HUB_BUCK | AP63203WU-7 | 5 | SW | HUB_BUCK_SW | FIT |
| U101 | U_HUB_BUCK | AP63203WU-7 | 6 | BST | HUB_BUCK_BST | FIT |
| L100 | L_HUB_BUCK | 4.7uH | 1 | 1 | HUB_BUCK_SW | FIT |
| L100 | L_HUB_BUCK | 4.7uH | 2 | 2 | +3V3_HUB | FIT |
| C100 | C_HUB_BUCK_IN | 10uF | 1 | 1 | +5V_EXT | FIT |
| C100 | C_HUB_BUCK_IN | 10uF | 2 | 2 | GND | FIT |
| C101 | C_HUB_BUCK_HF | 100nF | 1 | 1 | +5V_EXT | FIT |
| C101 | C_HUB_BUCK_HF | 100nF | 2 | 2 | GND | FIT |
| C102 | C_HUB_BOOT | 100nF | 1 | 1 | HUB_BUCK_BST | FIT |
| C102 | C_HUB_BOOT | 100nF | 2 | 2 | HUB_BUCK_SW | FIT |
| C103 | C_HUB_BUCK_OUT1 | 22uF | 1 | 1 | +3V3_HUB | FIT |
| C103 | C_HUB_BUCK_OUT1 | 22uF | 2 | 2 | GND | FIT |
| C104 | C_HUB_BUCK_OUT2 | 22uF | 1 | 1 | +3V3_HUB | FIT |
| C104 | C_HUB_BUCK_OUT2 | 22uF | 2 | 2 | GND | FIT |
| FB100 | FB_HUB_A | 120ohm@100MHz | 1 | 1 | +3V3_HUB | FIT |
| FB100 | FB_HUB_A | 120ohm@100MHz | 2 | 2 | +3V3_HUB_A | FIT |
| FB101 | FB_HUB_PLL | 120ohm@100MHz | 1 | 1 | LAN_1V8_USBPLL | FIT |
| FB101 | FB_HUB_PLL | 120ohm@100MHz | 2 | 2 | LAN_1V8_ETHPLL | FIT |
| C105 | C_HUB_IO19 | 100nF | 1 | 1 | +3V3_HUB | FIT |
| C105 | C_HUB_IO19 | 100nF | 2 | 2 | GND | FIT |
| C106 | C_HUB_IO27 | 100nF | 1 | 1 | +3V3_HUB | FIT |
| C106 | C_HUB_IO27 | 100nF | 2 | 2 | GND | FIT |
| C107 | C_HUB_IO33 | 100nF | 1 | 1 | +3V3_HUB | FIT |
| C107 | C_HUB_IO33 | 100nF | 2 | 2 | GND | FIT |
| C108 | C_HUB_IO39 | 100nF | 1 | 1 | +3V3_HUB | FIT |
| C108 | C_HUB_IO39 | 100nF | 2 | 2 | GND | FIT |
| C109 | C_HUB_IO46 | 100nF | 1 | 1 | +3V3_HUB | FIT |
| C109 | C_HUB_IO46 | 100nF | 2 | 2 | GND | FIT |
| C110 | C_HUB_A5 | 100nF | 1 | 1 | +3V3_HUB_A | FIT |
| C110 | C_HUB_A5 | 100nF | 2 | 2 | GND | FIT |
| C111 | C_HUB_A10 | 100nF | 1 | 1 | +3V3_HUB_A | FIT |
| C111 | C_HUB_A10 | 100nF | 2 | 2 | GND | FIT |
| C112 | C_HUB_A49 | 100nF | 1 | 1 | +3V3_HUB_A | FIT |
| C112 | C_HUB_A49 | 100nF | 2 | 2 | GND | FIT |
| C113 | C_HUB_A51 | 100nF | 1 | 1 | +3V3_HUB_A | FIT |
| C113 | C_HUB_A51 | 100nF | 2 | 2 | GND | FIT |
| C114 | C_HUB_A54 | 100nF | 1 | 1 | +3V3_HUB_A | FIT |
| C114 | C_HUB_A54 | 100nF | 2 | 2 | GND | FIT |
| C115 | C_HUB_A57 | 100nF | 1 | 1 | +3V3_HUB_A | FIT |
| C115 | C_HUB_A57 | 100nF | 2 | 2 | GND | FIT |
| C116 | C_HUB_A64 | 100nF | 1 | 1 | +3V3_HUB_A | FIT |
| C116 | C_HUB_A64 | 100nF | 2 | 2 | GND | FIT |
| C117 | C_HUB_A_BULK | 4.7uF | 1 | 1 | +3V3_HUB_A | FIT |
| C117 | C_HUB_A_BULK | 4.7uF | 2 | 2 | GND | FIT |
| C118 | C_HUB_CORE15 | 100nF | 1 | 1 | LAN_1V8_CORE | FIT |
| C118 | C_HUB_CORE15 | 100nF | 2 | 2 | GND | FIT |
| C119 | C_HUB_CORE38 | 100nF | 1 | 1 | LAN_1V8_CORE | FIT |
| C119 | C_HUB_CORE38 | 100nF | 2 | 2 | GND | FIT |
| C120 | C_HUB_CORE_BULK | 4.7uF | 1 | 1 | LAN_1V8_CORE | FIT |
| C120 | C_HUB_CORE_BULK | 4.7uF | 2 | 2 | GND | FIT |
| C121 | C_HUB_USBPLL | 1uF | 1 | 1 | LAN_1V8_USBPLL | FIT |
| C121 | C_HUB_USBPLL | 1uF | 2 | 2 | GND | FIT |
| C122 | C_HUB_ETHPLL | 1uF | 1 | 1 | LAN_1V8_ETHPLL | FIT |
| C122 | C_HUB_ETHPLL | 1uF | 2 | 2 | GND | FIT |
| R100 | R_HUB_EXRES | 12.4k | 1 | 1 | LAN_EXRES | FIT |
| R100 | R_HUB_EXRES | 12.4k | 2 | 2 | GND | FIT |
| R101 | R_HUB_USBRBIAS | 12k | 1 | 1 | LAN_USBRBIAS | FIT |
| R101 | R_HUB_USBRBIAS | 12k | 2 | 2 | GND | FIT |
| R102 | R_HUB_TCK | 10k | 1 | 1 | LAN_TCK | FIT |
| R102 | R_HUB_TCK | 10k | 2 | 2 | +3V3_HUB | FIT |
| R103 | R_HUB_MDIX | 10k | 1 | 1 | LAN_AUTO_MDIX | FIT |
| R103 | R_HUB_MDIX | 10k | 2 | 2 | +3V3_HUB | FIT |
| R104 | R_HUB_CLK24 | 10k | 1 | 1 | LAN_CLK24_EN | FIT |
| R104 | R_HUB_CLK24 | 10k | 2 | 2 | GND | FIT |
| Y100 | Y_HUB | 25MHz 3.3V HCMOS XO | 1 | ENABLE | +3V3_HUB | FIT |
| Y100 | Y_HUB | 25MHz 3.3V HCMOS XO | 2 | GND | GND | FIT |
| Y100 | Y_HUB | 25MHz 3.3V HCMOS XO | 3 | OUT | LAN_CLK25 | FIT |
| Y100 | Y_HUB | 25MHz 3.3V HCMOS XO | 4 | VDD | +3V3_HUB | FIT |
| C123 | C_HUB_XO | 100nF | 1 | 1 | +3V3_HUB | FIT |
| C123 | C_HUB_XO | 100nF | 2 | 2 | GND | FIT |
| U102 | U_HUB_RESET | TLV803EA30DBZR | 1 | GND | GND | FIT |
| U102 | U_HUB_RESET | TLV803EA30DBZR | 2 | RESET_N | RESET_HUB_N | FIT |
| U102 | U_HUB_RESET | TLV803EA30DBZR | 3 | VDD | +3V3_HUB | FIT |
| R105 | R_HUB_RESET | 10k | 1 | 1 | RESET_HUB_N | FIT |
| R105 | R_HUB_RESET | 10k | 2 | 2 | +3V3_HUB | FIT |
| C124 | C_HUB_RESET | 100nF | 1 | 1 | +3V3_HUB | FIT |
| C124 | C_HUB_RESET | 100nF | 2 | 2 | GND | FIT |
| U103 | U_HUB_EE | 93LC66A-I/SN | 1 | CS | LAN_EECS | FIT |
| U103 | U_HUB_EE | 93LC66A-I/SN | 2 | CLK | LAN_EECLK | FIT |
| U103 | U_HUB_EE | 93LC66A-I/SN | 3 | DI | LAN_EEDO | FIT |
| U103 | U_HUB_EE | 93LC66A-I/SN | 4 | DO | LAN_EEDI | FIT |
| U103 | U_HUB_EE | 93LC66A-I/SN | 5 | VSS | GND | FIT |
| U103 | U_HUB_EE | 93LC66A-I/SN | 6 | NC | NC | FIT |
| U103 | U_HUB_EE | 93LC66A-I/SN | 7 | NC | NC | FIT |
| U103 | U_HUB_EE | 93LC66A-I/SN | 8 | VCC | +3V3_HUB | FIT |
| C125 | C_HUB_EE | 100nF | 1 | 1 | +3V3_HUB | FIT |
| C125 | C_HUB_EE | 100nF | 2 | 2 | GND | FIT |
| R106 | R_HUB_EECS | 10k | 1 | 1 | LAN_EECS | FIT |
| R106 | R_HUB_EECS | 10k | 2 | 2 | GND | FIT |
| J100 | J_PI_USB | Pi USB2 OTG upstream solderpads | 1 | VBUS_SENSE | PI_USB_VBUS | FIT |
| J100 | J_PI_USB | Pi USB2 OTG upstream solderpads | 2 | D- | PI_USB_DM | FIT |
| J100 | J_PI_USB | Pi USB2 OTG upstream solderpads | 3 | D+ | PI_USB_DP | FIT |
| J100 | J_PI_USB | Pi USB2 OTG upstream solderpads | 4 | GND | GND | FIT |
| J100 | J_PI_USB | Pi USB2 OTG upstream solderpads | 5 | SHIELD | GND | FIT |
| R107 | R_PI_VBUS_TOP | 39.2k | 1 | 1 | PI_USB_VBUS | FIT |
| R107 | R_PI_VBUS_TOP | 39.2k | 2 | 2 | PI_VBUS_DET | FIT |
| R108 | R_PI_VBUS_BOT | 61.9k | 1 | 1 | PI_VBUS_DET | FIT |
| R108 | R_PI_VBUS_BOT | 61.9k | 2 | 2 | GND | FIT |
| C126 | C_PI_VBUS_DET | 100nF | 1 | 1 | PI_VBUS_DET | FIT |
| C126 | C_PI_VBUS_DET | 100nF | 2 | 2 | GND | FIT |
| C127 | C_PI_VBUS_ESD | 100nF | 1 | 1 | PI_USB_VBUS | FIT |
| C127 | C_PI_VBUS_ESD | 100nF | 2 | 2 | GND | FIT |
| D100 | D_PI_USB | USBLC6-2SC6 | 1 | IO1_A | PI_USB_DM | FIT |
| D100 | D_PI_USB | USBLC6-2SC6 | 2 | GND | GND | FIT |
| D100 | D_PI_USB | USBLC6-2SC6 | 3 | IO2_A | PI_USB_DP | FIT |
| D100 | D_PI_USB | USBLC6-2SC6 | 4 | IO2_B | PI_USB_DP | FIT |
| D100 | D_PI_USB | USBLC6-2SC6 | 5 | VBUS | PI_USB_VBUS | FIT |
| D100 | D_PI_USB | USBLC6-2SC6 | 6 | IO1_B | PI_USB_DM | FIT |
| U104 | U_USBA1_PWR | AP22653W6-7 | 1 | IN | +5V_EXT | FIT |
| U104 | U_USBA1_PWR | AP22653W6-7 | 2 | GND | GND | FIT |
| U104 | U_USBA1_PWR | AP22653W6-7 | 3 | EN | USBA1_CTL | FIT |
| U104 | U_USBA1_PWR | AP22653W6-7 | 4 | FAULT_N | USBA1_CTL | FIT |
| U104 | U_USBA1_PWR | AP22653W6-7 | 5 | ILIM | USBA1_ILIM | FIT |
| U104 | U_USBA1_PWR | AP22653W6-7 | 6 | OUT | USBA1_VBUS | FIT |
| R109 | R_USBA1_CTL | 10k | 1 | 1 | USBA1_CTL | FIT |
| R109 | R_USBA1_CTL | 10k | 2 | 2 | +3V3_HUB | FIT |
| R110 | R_USBA1_ILIM | 40.2k | 1 | 1 | USBA1_ILIM | FIT |
| R110 | R_USBA1_ILIM | 40.2k | 2 | 2 | GND | FIT |
| C128 | C_USBA1_IN | 1uF | 1 | 1 | +5V_EXT | FIT |
| C128 | C_USBA1_IN | 1uF | 2 | 2 | GND | FIT |
| C129 | C_USBA1_HF | 100nF | 1 | 1 | USBA1_VBUS | FIT |
| C129 | C_USBA1_HF | 100nF | 2 | 2 | GND | FIT |
| C130 | C_USBA1_BULK | 150uF | 1 | 1 | USBA1_VBUS | FIT |
| C130 | C_USBA1_BULK | 150uF | 2 | 2 | GND | FIT |
| D101 | D_USBA1 | USBLC6-2SC6 | 1 | IO1_A | USBA1_DM | FIT |
| D101 | D_USBA1 | USBLC6-2SC6 | 2 | GND | GND | FIT |
| D101 | D_USBA1 | USBLC6-2SC6 | 3 | IO2_A | USBA1_DP | FIT |
| D101 | D_USBA1 | USBLC6-2SC6 | 4 | IO2_B | USBA1_DP | FIT |
| D101 | D_USBA1 | USBLC6-2SC6 | 5 | VBUS | USBA1_VBUS | FIT |
| D101 | D_USBA1 | USBLC6-2SC6 | 6 | IO1_B | USBA1_DM | FIT |
| J101 | J_USBA1 | USB-A panelcable solderpads | 1 | VBUS | USBA1_VBUS | FIT |
| J101 | J_USBA1 | USB-A panelcable solderpads | 2 | D- | USBA1_DM | FIT |
| J101 | J_USBA1 | USB-A panelcable solderpads | 3 | D+ | USBA1_DP | FIT |
| J101 | J_USBA1 | USB-A panelcable solderpads | 4 | GND | GND | FIT |
| J101 | J_USBA1 | USB-A panelcable solderpads | 5 | SHIELD | GND | FIT |
| U105 | U_USBA2_PWR | AP22653W6-7 | 1 | IN | +5V_EXT | FIT |
| U105 | U_USBA2_PWR | AP22653W6-7 | 2 | GND | GND | FIT |
| U105 | U_USBA2_PWR | AP22653W6-7 | 3 | EN | USBA2_CTL | FIT |
| U105 | U_USBA2_PWR | AP22653W6-7 | 4 | FAULT_N | USBA2_CTL | FIT |
| U105 | U_USBA2_PWR | AP22653W6-7 | 5 | ILIM | USBA2_ILIM | FIT |
| U105 | U_USBA2_PWR | AP22653W6-7 | 6 | OUT | USBA2_VBUS | FIT |
| R111 | R_USBA2_CTL | 10k | 1 | 1 | USBA2_CTL | FIT |
| R111 | R_USBA2_CTL | 10k | 2 | 2 | +3V3_HUB | FIT |
| R112 | R_USBA2_ILIM | 40.2k | 1 | 1 | USBA2_ILIM | FIT |
| R112 | R_USBA2_ILIM | 40.2k | 2 | 2 | GND | FIT |
| C131 | C_USBA2_IN | 1uF | 1 | 1 | +5V_EXT | FIT |
| C131 | C_USBA2_IN | 1uF | 2 | 2 | GND | FIT |
| C132 | C_USBA2_HF | 100nF | 1 | 1 | USBA2_VBUS | FIT |
| C132 | C_USBA2_HF | 100nF | 2 | 2 | GND | FIT |
| C133 | C_USBA2_BULK | 150uF | 1 | 1 | USBA2_VBUS | FIT |
| C133 | C_USBA2_BULK | 150uF | 2 | 2 | GND | FIT |
| D102 | D_USBA2 | USBLC6-2SC6 | 1 | IO1_A | USBA2_DM | FIT |
| D102 | D_USBA2 | USBLC6-2SC6 | 2 | GND | GND | FIT |
| D102 | D_USBA2 | USBLC6-2SC6 | 3 | IO2_A | USBA2_DP | FIT |
| D102 | D_USBA2 | USBLC6-2SC6 | 4 | IO2_B | USBA2_DP | FIT |
| D102 | D_USBA2 | USBLC6-2SC6 | 5 | VBUS | USBA2_VBUS | FIT |
| D102 | D_USBA2 | USBLC6-2SC6 | 6 | IO1_B | USBA2_DM | FIT |
| J102 | J_USBA2 | USB-A panelcable solderpads | 1 | VBUS | USBA2_VBUS | FIT |
| J102 | J_USBA2 | USB-A panelcable solderpads | 2 | D- | USBA2_DM | FIT |
| J102 | J_USBA2 | USB-A panelcable solderpads | 3 | D+ | USBA2_DP | FIT |
| J102 | J_USBA2 | USB-A panelcable solderpads | 4 | GND | GND | FIT |
| J102 | J_USBA2 | USB-A panelcable solderpads | 5 | SHIELD | GND | FIT |
| U106 | U_USBA3_PWR | AP22653W6-7 | 1 | IN | +5V_EXT | FIT |
| U106 | U_USBA3_PWR | AP22653W6-7 | 2 | GND | GND | FIT |
| U106 | U_USBA3_PWR | AP22653W6-7 | 3 | EN | USBA3_CTL | FIT |
| U106 | U_USBA3_PWR | AP22653W6-7 | 4 | FAULT_N | USBA3_CTL | FIT |
| U106 | U_USBA3_PWR | AP22653W6-7 | 5 | ILIM | USBA3_ILIM | FIT |
| U106 | U_USBA3_PWR | AP22653W6-7 | 6 | OUT | USBA3_VBUS | FIT |
| R113 | R_USBA3_CTL | 10k | 1 | 1 | USBA3_CTL | FIT |
| R113 | R_USBA3_CTL | 10k | 2 | 2 | +3V3_HUB | FIT |
| R114 | R_USBA3_ILIM | 40.2k | 1 | 1 | USBA3_ILIM | FIT |
| R114 | R_USBA3_ILIM | 40.2k | 2 | 2 | GND | FIT |
| C134 | C_USBA3_IN | 1uF | 1 | 1 | +5V_EXT | FIT |
| C134 | C_USBA3_IN | 1uF | 2 | 2 | GND | FIT |
| C135 | C_USBA3_HF | 100nF | 1 | 1 | USBA3_VBUS | FIT |
| C135 | C_USBA3_HF | 100nF | 2 | 2 | GND | FIT |
| C136 | C_USBA3_BULK | 150uF | 1 | 1 | USBA3_VBUS | FIT |
| C136 | C_USBA3_BULK | 150uF | 2 | 2 | GND | FIT |
| D103 | D_USBA3 | USBLC6-2SC6 | 1 | IO1_A | USBA3_DM | FIT |
| D103 | D_USBA3 | USBLC6-2SC6 | 2 | GND | GND | FIT |
| D103 | D_USBA3 | USBLC6-2SC6 | 3 | IO2_A | USBA3_DP | FIT |
| D103 | D_USBA3 | USBLC6-2SC6 | 4 | IO2_B | USBA3_DP | FIT |
| D103 | D_USBA3 | USBLC6-2SC6 | 5 | VBUS | USBA3_VBUS | FIT |
| D103 | D_USBA3 | USBLC6-2SC6 | 6 | IO1_B | USBA3_DM | FIT |
| J103 | J_USBA3 | USB-A panelcable solderpads | 1 | VBUS | USBA3_VBUS | FIT |
| J103 | J_USBA3 | USB-A panelcable solderpads | 2 | D- | USBA3_DM | FIT |
| J103 | J_USBA3 | USB-A panelcable solderpads | 3 | D+ | USBA3_DP | FIT |
| J103 | J_USBA3 | USB-A panelcable solderpads | 4 | GND | GND | FIT |
| J103 | J_USBA3 | USB-A panelcable solderpads | 5 | SHIELD | GND | FIT |
| J104 | J_ETH | J0011D01BNL | 1 | TD+ | ETH_TXP | FIT |
| J104 | J_ETH | J0011D01BNL | 2 | TD- | ETH_TXN | FIT |
| J104 | J_ETH | J0011D01BNL | 3 | RD+ | ETH_RXP | FIT |
| J104 | J_ETH | J0011D01BNL | 4 | TCT | ETH_CT | FIT |
| J104 | J_ETH | J0011D01BNL | 5 | RCT | ETH_CT | FIT |
| J104 | J_ETH | J0011D01BNL | 6 | RD- | ETH_RXN | FIT |
| J104 | J_ETH | J0011D01BNL | 7 | NC | NC | FIT |
| J104 | J_ETH | J0011D01BNL | 8 | CHS_GND | GND | FIT |
| J104 | J_ETH | J0011D01BNL | 9 | GREEN_A | +3V3_HUB | FIT |
| J104 | J_ETH | J0011D01BNL | 10 | GREEN_K | ETH_LED_G_K | FIT |
| J104 | J_ETH | J0011D01BNL | 11 | YELLOW_K | ETH_LED_Y_K | FIT |
| J104 | J_ETH | J0011D01BNL | 12 | YELLOW_A | +3V3_HUB | FIT |
| J104 | J_ETH | J0011D01BNL | 13 | SHIELD1 | GND | FIT |
| J104 | J_ETH | J0011D01BNL | 14 | SHIELD2 | GND | FIT |
| R115 | R_ETH_TXP | 49.9 | 1 | 1 | ETH_TXP | FIT |
| R115 | R_ETH_TXP | 49.9 | 2 | 2 | +3V3_HUB_A | FIT |
| R116 | R_ETH_TXN | 49.9 | 1 | 1 | ETH_TXN | FIT |
| R116 | R_ETH_TXN | 49.9 | 2 | 2 | +3V3_HUB_A | FIT |
| R117 | R_ETH_RXP | 49.9 | 1 | 1 | ETH_RXP | FIT |
| R117 | R_ETH_RXP | 49.9 | 2 | 2 | +3V3_HUB_A | FIT |
| R118 | R_ETH_RXN | 49.9 | 1 | 1 | ETH_RXN | FIT |
| R118 | R_ETH_RXN | 49.9 | 2 | 2 | +3V3_HUB_A | FIT |
| R119 | R_ETH_CT | 10 | 1 | 1 | +3V3_HUB_A | FIT |
| R119 | R_ETH_CT | 10 | 2 | 2 | ETH_CT | FIT |
| C137 | C_ETH_CT | 22nF | 1 | 1 | ETH_CT | FIT |
| C137 | C_ETH_CT | 22nF | 2 | 2 | GND | FIT |
| R120 | R_ETH_LINK | 332 | 1 | 1 | ETH_LED_G_K | FIT |
| R120 | R_ETH_LINK | 332 | 2 | 2 | ETH_LINK_N | FIT |
| R121 | R_ETH_SPEED | 332 | 1 | 1 | ETH_LED_Y_K | FIT |
| R121 | R_ETH_SPEED | 332 | 2 | 2 | ETH_SPEED_N | FIT |
| U200 | U_SD | USB2642-I/ML | 1 | USBDN_DM2 | USB_A4_DM | FIT |
| U200 | U_SD | USB2642-I/ML | 2 | USBDN_DP2 | USB_A4_DP | FIT |
| U200 | U_SD | USB2642-I/ML | 3 | USBDN_DM3 | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 4 | USBDN_DP3 | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 5 | VDDA33 | +3V3_HUB | FIT |
| U200 | U_SD | USB2642-I/ML | 6 | PRTCTL2 | USB_A4_CTL | FIT |
| U200 | U_SD | USB2642-I/ML | 7 | PRTCTL3 | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 8 | SPI_CE_N | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 9 | SCL_EP/SPI_CLK | SD_EE_SCL | FIT |
| U200 | U_SD | USB2642-I/ML | 10 | SDA_EP/SPI_DO/SPI_SPD_SEL | SD_EE_SDA | FIT |
| U200 | U_SD | USB2642-I/ML | 11 | SPI_DI | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 12 | VDD33 | +3V3_HUB | FIT |
| U200 | U_SD | USB2642-I/ML | 13 | SD_WP | SD_WP_LOW | FIT |
| U200 | U_SD | USB2642-I/ML | 14 | SD_nCD | SD_CD_N | FIT |
| U200 | U_SD | USB2642-I/ML | 15 | VDD18 | SD_VDD18 | FIT |
| U200 | U_SD | USB2642-I/ML | 16 | VDD33 | +3V3_HUB | FIT |
| U200 | U_SD | USB2642-I/ML | 17 | SD_D1 | SD_DAT1 | FIT |
| U200 | U_SD | USB2642-I/ML | 18 | SD_D0 | SD_DAT0 | FIT |
| U200 | U_SD | USB2642-I/ML | 19 | SD_D7 | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 20 | SD_D6 | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 21 | SD_CLK | SD_CLK_SRC | FIT |
| U200 | U_SD | USB2642-I/ML | 22 | REG_EN | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 23 | SD_D5 | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 24 | SD_CMD | SD_CMD | FIT |
| U200 | U_SD | USB2642-I/ML | 25 | VDD33 | +3V3_HUB | FIT |
| U200 | U_SD | USB2642-I/ML | 26 | VDD33_OTP | +3V3_HUB | FIT |
| U200 | U_SD | USB2642-I/ML | 27 | TEST1 | GND | FIT |
| U200 | U_SD | USB2642-I/ML | 28 | TEST2 | GND | FIT |
| U200 | U_SD | USB2642-I/ML | 29 | SDA | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 30 | SD_D4 | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 31 | NC | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 32 | SD_D3 | SD_DAT3 | FIT |
| U200 | U_SD | USB2642-I/ML | 33 | SD_D2 | SD_DAT2 | FIT |
| U200 | U_SD | USB2642-I/ML | 34 | VDD33 | +3V3_HUB | FIT |
| U200 | U_SD | USB2642-I/ML | 35 | CRD_PWR | SD_3V3 | FIT |
| U200 | U_SD | USB2642-I/ML | 36 | SCL | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 37 | GPO1 | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 38 | RESET_N | RESET_HUB_N | FIT |
| U200 | U_SD | USB2642-I/ML | 39 | VBUS_DET | SD_UP_PRESENT | FIT |
| U200 | U_SD | USB2642-I/ML | 40 | TEST0 | GND | FIT |
| U200 | U_SD | USB2642-I/ML | 41 | VDDA33 | +3V3_HUB | FIT |
| U200 | U_SD | USB2642-I/ML | 42 | USBUP_DP | HUB_TO_SD_DP | FIT |
| U200 | U_SD | USB2642-I/ML | 43 | USBUP_DM | HUB_TO_SD_DM | FIT |
| U200 | U_SD | USB2642-I/ML | 44 | XTAL2 | NC | FIT |
| U200 | U_SD | USB2642-I/ML | 45 | XTAL1/CLKIN | SD_CLK24 | FIT |
| U200 | U_SD | USB2642-I/ML | 46 | VDD18PLL | SD_VDD18_PLL | FIT |
| U200 | U_SD | USB2642-I/ML | 47 | RBIAS | SD_RBIAS | FIT |
| U200 | U_SD | USB2642-I/ML | 48 | VDDA33 | +3V3_HUB | FIT |
| U200 | U_SD | USB2642-I/ML | 49 | VSS_EP | GND | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | 1 | 1 | SD_DAT2 | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | 2 | 2 | SD_DAT3 | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | 3 | 3 | SD_CMD | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | 4 | 4 | SD_3V3 | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | 5 | 5 | SD_CLK | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | 6 | 6 | GND | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | 7 | 7 | SD_DAT0 | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | 8 | 8 | SD_DAT1 | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | A | A | SD_CD_N | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | B | B | GND | FIT |
| J200 | J_SD | DM3AT-SF-PEJM5 | SHELL | SHELL | GND | FIT |
| U201 | U_SD_EE | 24LC04BT-I/SN | 1 | 1 | GND | DNP prototype |
| U201 | U_SD_EE | 24LC04BT-I/SN | 2 | 2 | GND | DNP prototype |
| U201 | U_SD_EE | 24LC04BT-I/SN | 3 | 3 | GND | DNP prototype |
| U201 | U_SD_EE | 24LC04BT-I/SN | 4 | 4 | GND | DNP prototype |
| U201 | U_SD_EE | 24LC04BT-I/SN | 5 | 5 | SD_EE_SDA_DEV | DNP prototype |
| U201 | U_SD_EE | 24LC04BT-I/SN | 6 | 6 | SD_EE_SCL_DEV | DNP prototype |
| U201 | U_SD_EE | 24LC04BT-I/SN | 7 | 7 | GND | DNP prototype |
| U201 | U_SD_EE | 24LC04BT-I/SN | 8 | 8 | +3V3_HUB | DNP prototype |
| R200 | R_SD_EE_SCL_LINK | 0R | 1 | 1 | SD_EE_SCL | DNP prototype |
| R200 | R_SD_EE_SCL_LINK | 0R | 2 | 2 | SD_EE_SCL_DEV | DNP prototype |
| R201 | R_SD_EE_SDA_LINK | 0R | 1 | 1 | SD_EE_SDA | DNP prototype |
| R201 | R_SD_EE_SDA_LINK | 0R | 2 | 2 | SD_EE_SDA_DEV | DNP prototype |
| R202 | R_SD_EE_SCL_PU | 4.7k | 1 | 1 | SD_EE_SCL_DEV | DNP prototype |
| R202 | R_SD_EE_SCL_PU | 4.7k | 2 | 2 | +3V3_HUB | DNP prototype |
| R203 | R_SD_EE_SDA_PU | 4.7k | 1 | 1 | SD_EE_SDA_DEV | DNP prototype |
| R203 | R_SD_EE_SDA_PU | 4.7k | 2 | 2 | +3V3_HUB | DNP prototype |
| Y200 | X_SD | ECS-2520S33-240-FN-TR | 1 | 1 | +3V3_HUB | FIT |
| Y200 | X_SD | ECS-2520S33-240-FN-TR | 2 | 2 | GND | FIT |
| Y200 | X_SD | ECS-2520S33-240-FN-TR | 3 | 3 | SD_CLK24_SRC | FIT |
| Y200 | X_SD | ECS-2520S33-240-FN-TR | 4 | 4 | +3V3_HUB | FIT |
| R204 | R_SD_XO | 0R | 1 | 1 | SD_CLK24_SRC | FIT |
| R204 | R_SD_XO | 0R | 2 | 2 | SD_CLK24 | FIT |
| R205 | R_SD_BIAS | 12k1% | 1 | 1 | SD_RBIAS | FIT |
| R205 | R_SD_BIAS | 12k1% | 2 | 2 | GND | FIT |
| R206 | R_SD_WP | 10k | 1 | 1 | SD_WP_LOW | FIT |
| R206 | R_SD_WP | 10k | 2 | 2 | GND | FIT |
| R207 | R_SD_PRESENT | 10k | 1 | 1 | SD_UP_PRESENT | FIT |
| R207 | R_SD_PRESENT | 10k | 2 | 2 | +3V3_HUB | FIT |
| R208 | R_SD_CLK | 0R | 1 | 1 | SD_CLK_SRC | FIT |
| R208 | R_SD_CLK | 0R | 2 | 2 | SD_CLK | FIT |
| C200 | C_SD_P5 | 100nF16V X7R 0603 | 1 | 1 | +3V3_HUB | FIT |
| C200 | C_SD_P5 | 100nF16V X7R 0603 | 2 | 2 | GND | FIT |
| C201 | C_SD_P12 | 100nF16V X7R 0603 | 1 | 1 | +3V3_HUB | FIT |
| C201 | C_SD_P12 | 100nF16V X7R 0603 | 2 | 2 | GND | FIT |
| C202 | C_SD_P16 | 100nF16V X7R 0603 | 1 | 1 | +3V3_HUB | FIT |
| C202 | C_SD_P16 | 100nF16V X7R 0603 | 2 | 2 | GND | FIT |
| C203 | C_SD_P25 | 100nF16V X7R 0603 | 1 | 1 | +3V3_HUB | FIT |
| C203 | C_SD_P25 | 100nF16V X7R 0603 | 2 | 2 | GND | FIT |
| C204 | C_SD_P26 | 100nF16V X7R 0603 | 1 | 1 | +3V3_HUB | FIT |
| C204 | C_SD_P26 | 100nF16V X7R 0603 | 2 | 2 | GND | FIT |
| C205 | C_SD_P34 | 100nF16V X7R 0603 | 1 | 1 | +3V3_HUB | FIT |
| C205 | C_SD_P34 | 100nF16V X7R 0603 | 2 | 2 | GND | FIT |
| C206 | C_SD_P41 | 100nF16V X7R 0603 | 1 | 1 | +3V3_HUB | FIT |
| C206 | C_SD_P41 | 100nF16V X7R 0603 | 2 | 2 | GND | FIT |
| C207 | C_SD_P48 | 100nF16V X7R 0603 | 1 | 1 | +3V3_HUB | FIT |
| C207 | C_SD_P48 | 100nF16V X7R 0603 | 2 | 2 | GND | FIT |
| C208 | C_SD_BULK16 | 4.7uF10V X7R | 1 | 1 | +3V3_HUB | FIT |
| C208 | C_SD_BULK16 | 4.7uF10V X7R | 2 | 2 | GND | FIT |
| C209 | C_SD_BULK48 | 4.7uF10V X7R | 1 | 1 | +3V3_HUB | FIT |
| C209 | C_SD_BULK48 | 4.7uF10V X7R | 2 | 2 | GND | FIT |
| C210 | C_SD_18 | 1uF6.3V X7R | 1 | 1 | SD_VDD18 | FIT |
| C210 | C_SD_18 | 1uF6.3V X7R | 2 | 2 | GND | FIT |
| C211 | C_SD_18PLL | 1uF6.3V X7R | 1 | 1 | SD_VDD18_PLL | FIT |
| C211 | C_SD_18PLL | 1uF6.3V X7R | 2 | 2 | GND | FIT |
| C212 | C_SD_EE | 100nF16V X7R | 1 | 1 | +3V3_HUB | DNP prototype |
| C212 | C_SD_EE | 100nF16V X7R | 2 | 2 | GND | DNP prototype |
| C213 | C_SD_XO | 100nF16V X7R | 1 | 1 | +3V3_HUB | FIT |
| C213 | C_SD_XO | 100nF16V X7R | 2 | 2 | GND | FIT |
| C214 | C_SD_CARD1 | 4.7uF10V X7R | 1 | 1 | SD_3V3 | FIT |
| C214 | C_SD_CARD1 | 4.7uF10V X7R | 2 | 2 | GND | FIT |
| C215 | C_SD_CARD2 | 100nF16V X7R | 1 | 1 | SD_3V3 | FIT |
| C215 | C_SD_CARD2 | 100nF16V X7R | 2 | 2 | GND | FIT |
| D200 | D_SD | TPD6E004RSER | 1 | 1 | SD_DAT0 | FIT |
| D200 | D_SD | TPD6E004RSER | 2 | 2 | SD_DAT1 | FIT |
| D200 | D_SD | TPD6E004RSER | 3 | 3 | SD_DAT2 | FIT |
| D200 | D_SD | TPD6E004RSER | 4 | 4 | GND | FIT |
| D200 | D_SD | TPD6E004RSER | 5 | 5 | SD_DAT3 | FIT |
| D200 | D_SD | TPD6E004RSER | 6 | 6 | SD_CMD | FIT |
| D200 | D_SD | TPD6E004RSER | 7 | 7 | SD_CLK | FIT |
| D200 | D_SD | TPD6E004RSER | 8 | 8 | +3V3_HUB | FIT |
| C216 | C_SD_ESD | 100nF16V X7R | 1 | 1 | +3V3_HUB | FIT |
| C216 | C_SD_ESD | 100nF16V X7R | 2 | 2 | GND | FIT |
| D201 | D_SD_AUX | TPD2E2U06DCKR | 1 | 1 | SD_CD_N | FIT |
| D201 | D_SD_AUX | TPD2E2U06DCKR | 2 | 2 | SD_3V3 | FIT |
| D201 | D_SD_AUX | TPD2E2U06DCKR | 3 | 3 | GND | FIT |
| U202 | U_A4_PWR | AP22653W6-7 | 1 | 1 | +5V_EXT | FIT |
| U202 | U_A4_PWR | AP22653W6-7 | 2 | 2 | GND | FIT |
| U202 | U_A4_PWR | AP22653W6-7 | 3 | 3 | USB_A4_CTL | FIT |
| U202 | U_A4_PWR | AP22653W6-7 | 4 | 4 | USB_A4_CTL | FIT |
| U202 | U_A4_PWR | AP22653W6-7 | 5 | 5 | USB_A4_ILIM | FIT |
| U202 | U_A4_PWR | AP22653W6-7 | 6 | 6 | USB_A4_VBUS | FIT |
| R209 | R_A4_CTL | 10k | 1 | 1 | USB_A4_CTL | FIT |
| R209 | R_A4_CTL | 10k | 2 | 2 | +3V3_HUB | FIT |
| R210 | R_A4_ILIM | 40.2k1% | 1 | 1 | USB_A4_ILIM | FIT |
| R210 | R_A4_ILIM | 40.2k1% | 2 | 2 | GND | FIT |
| C217 | C_A4_IN | 1uF10V X7R | 1 | 1 | +5V_EXT | FIT |
| C217 | C_A4_IN | 1uF10V X7R | 2 | 2 | GND | FIT |
| C218 | C_A4_OUT | 150uF10V | 1 | 1 | USB_A4_VBUS | FIT |
| C218 | C_A4_OUT | 150uF10V | 2 | 2 | GND | FIT |
| C219 | C_A4_HF | 100nF16V X7R | 1 | 1 | USB_A4_VBUS | FIT |
| C219 | C_A4_HF | 100nF16V X7R | 2 | 2 | GND | FIT |
| D202 | D_A4 | USBLC6-2SC6 | 1 | 1 | USB_A4_DM | FIT |
| D202 | D_A4 | USBLC6-2SC6 | 2 | 2 | GND | FIT |
| D202 | D_A4 | USBLC6-2SC6 | 3 | 3 | USB_A4_DP | FIT |
| D202 | D_A4 | USBLC6-2SC6 | 4 | 4 | USB_A4_DP | FIT |
| D202 | D_A4 | USBLC6-2SC6 | 5 | 5 | USB_A4_VBUS | FIT |
| D202 | D_A4 | USBLC6-2SC6 | 6 | 6 | USB_A4_DM | FIT |
| J201 | J_A4 | USB-A female case-port harness interface | 1 | 1 | USB_A4_VBUS | FIT |
| J201 | J_A4 | USB-A female case-port harness interface | 2 | 2 | USB_A4_DM | FIT |
| J201 | J_A4 | USB-A female case-port harness interface | 3 | 3 | USB_A4_DP | FIT |
| J201 | J_A4 | USB-A female case-port harness interface | 4 | 4 | GND | FIT |
| J201 | J_A4 | USB-A female case-port harness interface | 5 | 5 | GND | FIT |
| U300 | CON_U1 | SN74LVC2G125DCTR | 1 | 1OE_N | CONSOLE_DISABLE | FIT |
| U300 | CON_U1 | SN74LVC2G125DCTR | 2 | 1A | CONSOLE_TXD_RAW | FIT |
| U300 | CON_U1 | SN74LVC2G125DCTR | 3 | 2Y | CONSOLE_RX_BUF | FIT |
| U300 | CON_U1 | SN74LVC2G125DCTR | 4 | GND | GND | FIT |
| U300 | CON_U1 | SN74LVC2G125DCTR | 5 | 2A | PI_UART_TX | FIT |
| U300 | CON_U1 | SN74LVC2G125DCTR | 6 | 1Y | PI_RX_BUF | FIT |
| U300 | CON_U1 | SN74LVC2G125DCTR | 7 | 2OE_N | CONSOLE_DISABLE | FIT |
| U300 | CON_U1 | SN74LVC2G125DCTR | 8 | VCC | PI_3V3 | FIT |
| Q300 | CON_Q1 | MMBT3904LT1G | 1 | B | CONSOLE_BASE | FIT |
| Q300 | CON_Q1 | MMBT3904LT1G | 2 | E | GND | FIT |
| Q300 | CON_Q1 | MMBT3904LT1G | 3 | C | CONSOLE_DISABLE | FIT |
| R300 | CON_R1 | 10k | 1 | 1 | PI_3V3 | FIT |
| R300 | CON_R1 | 10k | 2 | 2 | CONSOLE_DISABLE | FIT |
| R301 | CON_R2 | 47k | 1 | 1 | PC_USB_VBUS_SENSE | FIT |
| R301 | CON_R2 | 47k | 2 | 2 | CONSOLE_BASE | FIT |
| R302 | CON_R3 | 100k | 1 | 1 | CONSOLE_BASE | FIT |
| R302 | CON_R3 | 100k | 2 | 2 | GND | FIT |
| R303 | CON_R4 | 100k | 1 | 1 | CONSOLE_TXD_RAW | FIT |
| R303 | CON_R4 | 100k | 2 | 2 | GND | FIT |
| R304 | CON_R5 | 100k | 1 | 1 | PI_UART_TX | FIT |
| R304 | CON_R5 | 100k | 2 | 2 | PI_3V3 | FIT |
| R305 | CON_R6 | 10k | 1 | 1 | PI_UART_RX | FIT |
| R305 | CON_R6 | 10k | 2 | 2 | PI_3V3 | FIT |
| R306 | CON_R7 | 10k | 1 | 1 | CONSOLE_RXD_RAW | FIT |
| R306 | CON_R7 | 10k | 2 | 2 | CONSOLE_3V3 | FIT |
| R307 | CON_R8 | 330 | 1 | 1 | PI_RX_BUF | FIT |
| R307 | CON_R8 | 330 | 2 | 2 | PI_UART_RX | FIT |
| R308 | CON_R9 | 330 | 1 | 1 | CONSOLE_RX_BUF | FIT |
| R308 | CON_R9 | 330 | 2 | 2 | CONSOLE_RXD_RAW | FIT |
| C300 | CON_C1 | 100nF X7R 10V | 1 | 1 | PI_3V3 | FIT |
| C300 | CON_C1 | 100nF X7R 10V | 2 | 2 | GND | FIT |
| J300 | CON_J1 | CP2102N Friend #5335 wired interface | 1 | GND (JP1.1) | GND | FIT |
| J300 | CON_J1 | CP2102N Friend #5335 wired interface | 2 | VBUS (JP1.3) | PC_USB_VBUS_SENSE | FIT |
| J300 | CON_J1 | CP2102N Friend #5335 wired interface | 3 | TXD (JP1.4) | CONSOLE_TXD_RAW | FIT |
| J300 | CON_J1 | CP2102N Friend #5335 wired interface | 4 | RXD (JP1.5) | CONSOLE_RXD_RAW | FIT |
| J300 | CON_J1 | CP2102N Friend #5335 wired interface | 5 | 3V3 (JP4.2) | CONSOLE_3V3 | FIT |
