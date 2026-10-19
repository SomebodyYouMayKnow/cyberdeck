# NEONRED

NEONRED is a compact cyberdeck built around a Raspberry Pi Zero 2 W and a LILYGO T-Display-S3 AMOLED. The Pi runs Linux and drives a 3.5-inch Waveshare HDMI display; the LILYGO ESP32-S3 provides a small control interface. The current BOM has no battery, so operation requires external 5 V power. The build uses a CardKB keyboard, rotary encoder, navigation buttons, IR hardware, two nRF24L01+ modules, a Waveshare USB Hub HAT, and an external Chameleon Ultra SE3 for RFID/NFC experiments.

The current saved EasyEDA working design is `cyberdeck-completed`; its live two-layer order-candidate export and Gerber files are recorded under `PCB/`. The exported board passed the configured EasyEDA DRC (0 errors; 29/29 nets assigned), so it is ready for a bare-board prototype order. That does not confirm assembled electrical operation or power-on safety. See the current verification report and BOM before buying or powering the build.

## Current scope

- Raspberry Pi Zero 2 W as the Linux host.
- Waveshare 3.5-inch HDMI LCD (SKU12824), connected by Mini-HDMI-to-HDMI cable.
- LILYGO T-Display-S3 AMOLED as the ESP32 control/display module.
- CardKB, rotary encoder, navigation buttons, IR receiver/transmitter, and two nRF24L01+ modules.
- Waveshare four-port USB Hub HAT mounted separately beside the Pi.
- Chameleon Ultra SE3 as a removable external RFID/NFC device.
- No RTL-SDR/radar detector in the current version. The listed INIU bank is assigned to the Pi/HAT branch only; the auxiliary board rail uses a separate owned bank and external regulator, subject to checking labels and measuring loads.

## Project files

- [Current action and verification status](docs/NEONRED_ACTIONS_AND_TEST_STATUS_2026-10-18.md)
- [Current scope and intended uses](docs/NEONRED_FINAL_VERSION_2026-10-09.md)
- [Rollback record](docs/NEONRED_SCOPE_RESET_2026-10-16.md)
- [Current purchase BOM](BOM.csv)
- [Current BOM with ownership and LCSC columns](BOM_NEONRED_LCSC_Owned_current_2026-10-17.csv)
- [Restored EasyEDA PCB source export](PCB/PCB_savecopy_2026-10-16.json)
- [PCB and schematic exports](PCB/)
- [Firmware](Firmware/)
- [CAD](cad/)
- [Historical project notes](docs/PROJECT_SUMMARY.md)

Older dated audit/BOM documents are historical records; use the current scope and BOM links above for build decisions.
