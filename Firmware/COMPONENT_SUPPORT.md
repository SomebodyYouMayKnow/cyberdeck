# Component software coverage

| Component | Connection | Current firmware support | Hardware-dependent work remaining |
| --- | --- | --- | --- |
| LILYGO T-Display-S3 AMOLED | Runs ESP32 firmware | PlatformIO scaffold and USB serial bridge | Confirm board revision and display library/pin configuration before adding UI. |
| CardKB | I²C address `0x5F`; level-shifted SDA/SCL on GPIO1/GPIO41 | Polls one-byte key events and sends JSON to Pi | Verify the CardKB module pullups, voltage, and wiring before connecting. |
| PEC11R mechanical encoder | A/B on GPIO2/GPIO3, common C to GND; push contact on GPIO42/GND | Polls quadrature and push state; internal pull-ups enabled on all inputs | Verify rotation direction and contact numbering on the physical encoder. The tactile SELECT button shares GPIO42 with encoder push. |
| Two nRF24L01+ radios | Shared SPI, separate CE/CSN | Initialises safely at minimum power and can send/receive 32-byte packets | Choose unique RF addresses/channels and measure regulated-rail current. |
| Discrete onboard IR | TSOP38238 output on GPIO39; GPIO40 drives a 2N2222A LED switch through 1 kΩ | Receives decoded data and sends commanded NEC codes | Use a 100 Ω series resistor for the IR LED from 3V3_AUX; verify transistor pinout/footprint and LED orientation before fabrication. |
| Raspberry Pi | ESP32 USB serial cable | Python bridge prints events and sends commands | Add a systemd service and user-interface integration after device testing. |
| Chameleon Ultra SE3 | BLE | Safe BLE discovery utility only | Verify exact firmware GATT UUIDs and documented command protocol before any connection or control. |
| HDMI display | Pi HDMI | Handled by Raspberry Pi OS | Confirm exact panel power/touch wiring and configure display rotation. |
| Waveshare USB HUB HAT | Pi USB host | No custom firmware required | Check the physical hub, cable, and USB enumeration. |
| ALFA USB Wi-Fi adapter | Pi USB | Handled by Raspberry Pi OS/driver | Install the matching driver and confirm legal, authorized use. |

Nothing in this scaffold enables impersonation, credential extraction, or access to networks, cards, tags, or IR-controlled devices without authorization. It is for owned hardware, basic interoperability, and bring-up tests.
