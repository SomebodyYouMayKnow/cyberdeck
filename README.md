# NEONRED

NEONRED is a compact cyberdeck built around a Raspberry Pi Zero 2 W and a LILYGO T-Display-S3 AMOLED. The Pi runs Linux and drives a 3.5-inch Waveshare HDMI display; the LILYGO ESP32-S3 provides a small control interface. The current BOM has no battery, so operation requires external 5 V power. The build uses a CardKB keyboard, rotary encoder, navigation buttons, IR hardware, two nRF24L01+ modules, a Waveshare USB Hub HAT, and an external Chameleon Ultra SE3 for RFID/NFC experiments.

The EasyEDA PCB was restored from the preserved `savecopy` on 2026-10-16. The savecopy itself was not edited. This project is not yet cleared for fabrication or power-on; see the current scope and release notes before ordering.

## Current scope

- Raspberry Pi Zero 2 W as the Linux host.
- Waveshare 3.5-inch HDMI LCD (SKU12824), connected by Mini-HDMI-to-HDMI cable.
- LILYGO T-Display-S3 AMOLED as the ESP32 control/display module.
- CardKB, rotary encoder, navigation buttons, IR receiver/transmitter, and two nRF24L01+ modules.
- Waveshare four-port USB Hub HAT mounted separately beside the Pi.
- Chameleon Ultra SE3 as a removable external RFID/NFC device.
- No battery, integrated Proxmark3, RTL-SDR/radar detector, or external ESP32 antenna in the current version.

## Project files

- [Current scope and intended uses](docs/NEONRED_FINAL_VERSION_2026-10-09.md)
- [Rollback record](docs/NEONRED_SCOPE_RESET_2026-10-16.md)
- [Current BOM](BOM_NEONRED_current_2026-10-17.csv)
- [Current BOM with ownership and LCSC columns](BOM_NEONRED_LCSC_Owned_current_2026-10-17.csv)
- [Restored EasyEDA PCB source export](PCB/PCB_savecopy_2026-10-16.json)
- [PCB and schematic exports](PCB/)
- [Firmware](Firmware/)
- [CAD](cad/)
- [Historical project notes](docs/PROJECT_SUMMARY.md)

Older dated audit/BOM documents remain as historical records. They may describe Proxmark3 and SDR experiments that are outside the current scope.
