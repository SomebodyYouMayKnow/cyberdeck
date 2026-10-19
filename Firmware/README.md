# NEONRED firmware

This is a bring-up scaffold for the saved `cyberdeck-completed` design, not a tested release. The ESP32-S3 firmware handles button/encoder events, polls the M5Stack CardKB over I²C, starts two nRF24L01 radios, handles IR receive/transmit, and exposes a line-based USB-serial protocol to the Raspberry Pi. The Pi script relays events and commands; it does not yet turn the CardKB into Linux keyboard input or draw the finished display UI.

## Current wiring assumptions

- CardKB I²C address `0x5F` through the carrier's level shifter: SDA GPIO1, SCL GPIO41.
- Encoder A/B GPIO2/GPIO3; common to GND. Encoder push and SELECT are the shared active-low GPIO42/`ENC_SW` net.
- BACK/MENU/UP/DOWN are active-low GPIO43/44/45/46.
- Both nRF24 modules share SPI (SCK 12, MOSI 11, MISO 13), with separate CE/CSN pairs.
- IR receiver GPIO39; the transistor-driven IR emitter control is GPIO40.

These assignments match the saved 2026-10-18 PCB export's labeled connector nets. They still need continuity and module-level checks on the physical assembly. Keep the signal source and receiver power domains on together; there is no powered-off signal isolation on these direct connections.

## Build and staged bring-up

1. Build and flash `esp32/` with PlatformIO after installing the dependencies in `platformio.ini`. This workspace does not currently have PlatformIO installed, so this revision has **not** been compiled here.
2. Use `pi/requirements.txt` and connect the Pi to the ESP32 with an intact USB data cable.
3. Start with current-limited bench supplies, rails disconnected from USB power-bank wiring. Measure polarity and voltage at JP4 before inserting modules.
4. Test one function at a time: serial `PING`/`STATUS`, keyboard I²C, each button, encoder, IR receive, IR transmit at low duty, then each radio at minimum output.
5. Measure branch current and regulator temperature; only then test the combined load.

Do not connect the currently listed INIU BI-B5 bank to power the whole deck. Its simultaneous multi-port output is rated at 5 V / 3 A total, while the Pi's recommended input alone is 5 V / 2.5 A and the deck needs a separate auxiliary rail. See [the power report](../docs/NEONRED_ACTIONS_AND_TEST_STATUS_2026-10-18.md).
