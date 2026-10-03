# Cyberdeck firmware

This folder is an **untested pre-hardware bring-up scaffold** for the current simple-power PCB revision.

- `esp32/` is a PlatformIO Arduino project for the LILYGO ESP32-S3 AMOLED board.
- `pi/` reads the ESP32 USB serial link and sends console commands back.
- `PROTOCOL.md` documents the line-based command protocol.

## Bring-up order

1. Confirm the actual hardware revisions and the carrier PCB against the saved wiring map.
2. Power the ESP32 and the regulated peripheral rail as required by `outputs/wiring-map-simple-power.txt`.
3. Flash `Firmware/esp32` with PlatformIO.
4. On the Pi, install `pyserial` and run `python3 cyberdeck_bridge.py --port /dev/ttyACM0`.
5. Send `STATUS` first. Verify I²C devices, radios and IR one subsystem at a time.

Do not operate direct SPI/IR/I²C signal connections when the related domain is unpowered. Begin radios at minimum power and measure the external regulator load and temperature before normal use.

