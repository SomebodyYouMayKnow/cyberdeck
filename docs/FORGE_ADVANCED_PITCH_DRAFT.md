# Forge advanced-project pitch draft

**Use this as a draft.** Replace the bracketed past-project line with your own experience before posting. The budget is a rough planning estimate, not an order or a claim that the project is already built.

Name: **NEONRED**

I'm designing: **NEONRED, a modular clamshell cyberdeck built around a Raspberry Pi Zero 2 W and a LILYGO ESP32-S3 AMOLED board.** The Pi provides the Linux computer and HDMI display, while the ESP32 handles the small local display, CardKB keyboard, rotary encoder, IR transceiver, and two nRF24 radio modules. A custom 190 × 110 mm carrier PCB keeps the low-current peripheral wiring organized, and a 3D-printed case will hold the keyboard, display, battery, Pi, USB hub, electronics, and folding antenna mounts. I have already published the in-progress CAD, PCB/schematic, wiring map, BOM, and starter firmware here: https://github.com/SomebodyYouMayKnow/cyberdeck

Inspo / reference: I am combining the compact, repairable layout of a clamshell field terminal with the accessible modular electronics of Raspberry Pi and ESP32 projects. My main reference is my own design repository above, especially its wiring map, carrier-PCB layout, and enclosure layout. I want this to become a portable computer that teaches me enclosure design, PCB design, embedded firmware, Linux integration, and physical assembly in one project.

Past projects: **[Replace this with your own truthful experience. Example: “This is my first large hardware project. I have previously learned programming and basic electronics, and for NEONRED I have already created the PCB, wiring plan, CAD layout, BOM, and starter firmware.”]**

Why this is worth more than $200: NEONRED needs more than a normal small PCB grant because it combines a custom carrier PCB, a 3D-printed clamshell enclosure, a Raspberry Pi computer, display, keyboard, ESP32 interface, separate peripheral power hardware, radio modules, IR hardware, mounting hardware, and cables. The goal is not only to buy modules, but to turn the documented design into a functional, repairable physical system and learn through the complete cycle: CAD → PCB → firmware → fabrication → testing → documented open-source build. The current planned cost is about **$277.38**, and this includes a conservative estimate for the custom PCB and enclosure materials. I will update the repository with physical measurements, fabrication files, build notes, test results, and photos after funding.

Rough BOM:

| Item | Cost (USD) |
| --- | ---: |
| Chameleon Ultra SE3 | $39.99 |
| nRF24L01+ PA/LNA radio kit | $9.99 |
| ALFA AWUS036ACS USB Wi-Fi adapter | $26.97 |
| Waveshare 3.5-inch HDMI LCD | $31.99 |
| M5Stack CardKB v1.1 | $7.95 |
| Miady 10,000 mAh power-bank two-pack | $19.97 |
| I2C level shifter, encoder, IR transceiver, 3.3 V regulator | $24.80 |
| M2.5/M3 mounting hardware | $19.98 |
| HDMI, USB, hub-data, and adapter cables | $25.75 |
| Through-hole component kit | $9.99 |
| Custom 190 × 110 mm carrier PCB — estimate | $35.00 |
| 3D-printed enclosure material/service — estimate | $25.00 |
| **Total** | **$277.38** |

## Before posting

1. Replace the `Past projects` line with your own words.
2. Check each item, quantity, and link against `BOM.csv`.
3. Post this in `#forgery` only after you are happy with every statement.
4. Do not say the hardware has been tested or built yet; it has not.
