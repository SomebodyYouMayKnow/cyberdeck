# Cyberdeck firmware

This folder is an **untested pre-hardware bring-up scaffold**. The 2026-10-06 master-power / service-port redesign is documented in [POWER_AND_IO_REVISION_2026-10-06.md](../docs/POWER_AND_IO_REVISION_2026-10-06.md) but has not yet been applied to the EasyEDA schematic or PCB. Do not follow the earlier simple-power wiring notes as the new design.

- `esp32/` is a PlatformIO Arduino project for the LILYGO ESP32-S3 AMOLED board.
- `pi/` reads the ESP32 USB serial link and sends console commands back.
- `PROTOCOL.md` documents the line-based command protocol.

## Bring-up order

1. Confirm the actual hardware revisions and the carrier PCB against the saved wiring map.
2. Do not connect the proposed single-input power system until its source, protection, and PCB have been measured and verified. The currently listed Miady bank does not meet the revised one-input power requirement.
3. Flash `Firmware/esp32` with PlatformIO.
4. On the Pi, install `pyserial` and run `python3 cyberdeck_bridge.py --port /dev/ttyACM0`.
5. Send `STATUS` first. Verify I²C devices, radios and IR one subsystem at a time.

Do not operate direct SPI/IR/I²C signal connections when the related domain is unpowered. Begin radios at minimum power and measure the external regulator load and temperature before normal use.
