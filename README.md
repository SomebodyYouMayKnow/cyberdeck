# NEONRED

NEONRED is a compact, modular cyberdeck built around a Raspberry Pi Zero 2 W and a LILYGO T-Display-S3 AMOLED. The Pi runs Linux and hosts USB peripherals through the Waveshare USB HUB HAT. The LILYGO board provides the ESP32-S3 control interface and its own AMOLED display. **The current design has no separate HDMI display.**

## Planned capabilities

- Portable Linux development and an on-device ESP32 control interface.
- CardKB keyboard, rotary encoder and navigation buttons.
- IR receive/transmit hardware and two nRF24L01+ modules for controlled lab experiments.
- Chameleon Ultra SE3 for testing owned RFID/NFC tags and lab cards.
- ALFA dual-band Wi-Fi adapter for authorized testing on owned or explicitly authorized networks.
- Proxmark3 RDV4 as a separately mounted USB instrument, with its own LF/HF antenna system; it is not a bare IC to solder onto the carrier PCB.
- RTL-SDR Blog V4 as a USB receive-only SDR. The radar-detector experiment needs external X/K/Ka downconverters because the V4 cannot tune directly to those radar frequencies.
- ESP32 firmware experiments: the project’s control UI, passive Flock You detection, and ESP32 Marauder are separate firmware modes. They cannot all run simultaneously on one ESP32, and support for this exact LILYGO board must be validated.
- A switchable 2.4 GHz external antenna for the ESP32, conditional on confirming the exact LILYGO revision has an antenna-feed option.

Radio work is for the user's own equipment and explicitly authorized environments. Keep Wi-Fi testing non-disruptive and do not interfere with or access other people's networks or devices.

## Design status

The EasyEDA files in `PCB/` are saved design-stage exports, not a fabrication release. The new radio additions need mechanical outlines, serviceable USB connections, antenna clearances, and a power/thermal check. The exact Proxmark3 model, RTL-SDR supply, LILYGO revision, and antenna-feed option are not yet verified. See [the current feature and integration plan](docs/NEONRED_FINAL_VERSION_2026-10-09.md).

Existing project files include source exports, wiring notes, screenshots, firmware scaffolding, and CAD/layout artifacts. Treat older HDMI-specific and superseded power documents as historical until reconciled with the live EasyEDA project.

## Useful files

- [Current goal and integration plan](docs/NEONRED_FINAL_VERSION_2026-10-09.md)
- [PCB source and screenshots](PCB/)
- [Firmware scaffold](Firmware/)
- [CAD files](cad/)
- [Current master BOM/status list](BOM.csv)
- [Earlier dated purchase list](BOM_NEONRED_purchase-list_2026-10-06.csv; historical until reconciled)
- [Detailed project notes](docs/PROJECT_SUMMARY.md)
