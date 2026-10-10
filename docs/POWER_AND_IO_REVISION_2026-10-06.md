# NEONRED power, controls, and service-port revision

Updated: 2026-10-06. This is the current requested architecture for the next schematic/PCB revision. It supersedes the earlier “separate USB power cables / peripheral-only switch” proposal in `PROJECT_SUMMARY.md`. This is an electrical design draft, not a fabrication release.

## Requested interfaces

- One latching master switch controls the complete deck power distribution.
- One external USB-C female port is the 5 V system-power input.
- One external USB-C female port carries native USB data for ESP32-S3 programming/control.
- One external micro-USB female port provides access to the Pi Zero 2 W OTG/data connector.
- Add two momentary through-hole controls: Back and Menu. Keep the rotary encoder for scrolling and its push contact for Select.
- Replace the Adafruit #5990 plug-in IR board with its receive/transmit functions on the carrier PCB; place the IR receiver and two emitters at the left wall aperture, on short leads only if needed for optical alignment.

## Power-path intent

`USB-C power input → 5 V-only sink/PD interface → input protection → master switch → protected branches`.

The switched 5 V branches are: Pi PWR IN, LILYGO 5 V/VBUS input, HDMI display (only if its exact revision uses 5 V), and the peripheral regulator input. The regulator supplies the nRF24 modules and IR transmit stage at 3.3 V. CardKB is supplied at 5 V through its existing level-shifter arrangement. Grounds are common. Do not connect independent USB VBUS sources together.

The input must negotiate or otherwise provide 5 V at the measured total load. If USB-PD is used, the sink must request a 5 V profile; do not feed a 9/12/15/20 V profile directly to the 5 V rails. Place a fuse/current-limiting stage immediately after the input. Size the fuse, switch, connector, copper, and each branch from measured peak currents and the weakest cable/connector; values are deliberately TBD until those measurements and exact module revisions are known. The source's maximum rating limits available current, while a fuse protects against faults. Never treat a wide trace as overcurrent protection.

The currently listed Miady two-pack bank is not suitable as the single source for this proposed architecture: its published output is up to 5 V/2.4 A, while Raspberry Pi recommends a 5 V/2.5 A supply for Zero-series boards, before the HDMI display, LILYGO, HAT peripherals, radios, and IR are counted. Use a higher-capacity source for one-input operation or retain electrically isolated separate sources; do not pretend the existing bank has enough headroom.

The master switch must interrupt the system 5 V after input protection and before every load branch. Its OFF position must also prevent the ESP32 programming cable or Pi service cable from back-powering system rails. The computer USB-C VBUS is therefore isolated from system 5 V; retain only a correctly isolated VBUS-detect path if the LILYGO native USB implementation requires it. Verify enumeration with the exact LILYGO revision before PCB release.

This is a hard power cut, not a graceful Pi shutdown. Until a proper shutdown controller is designed and tested, shut Linux down first and then use the master switch; cutting power during SD-card writes can corrupt the Pi boot card.

## USB service paths

- **ESP32 USB-C:** Use the LILYGO's native USB 2.0 D+/D− path, brought to a panel female connector. Keep the data pair together and short; ground the shield to chassis at the entry. The computer's VBUS must not become an alternate source for the switched 5 V bus.
- **Pi micro-USB:** Treat the requested panel jack as the Pi's OTG/data service connection. Pi power remains on the switched 5 V rail through the separate PWR IN connector. The Pi OTG port is already used by the Waveshare four-port USB HUB HAT, so add a break-before-make 2:1 USB 2.0 selector labelled `HAT / PC`. It must route only one upstream connection to the Pi at a time, prevent VBUS backfeed, and preserve the correct OTG host/device role. The external PC service mode may require Pi USB-gadget configuration. Do not wire the HAT and external computer in parallel.
- **Power USB-C:** This is the only system-power entry. It requires a correctly wired USB-C sink interface/CC termination (or a preassembled sink module) and input protection. A bare USB-C receptacle with only VBUS/GND wires is not a complete C-to-C sink.

## Controls and IR

Button assignments for the next firmware/hardware revision:

| Control | ESP32 pin | Wiring |
| --- | --- | --- |
| Back | GPIO43 | Normally-open switch to GND; internal pull-up |
| Menu | GPIO44 | Normally-open switch to GND; internal pull-up |
| Select | GPIO42 | Existing rotary encoder push contact to GND; internal pull-up |
| Navigate | Existing encoder A/B | Keep current assignments |

This gives the screen UI Back, Menu, Select, and rotary navigation. GPIO43/44 are also the LILYGO UART0 pins, so the native USB CDC connection is used for the programming/service port; do not use UART0 at the same time. The current firmware can report button events over USB serial; drawing a menu on the AMOLED still requires the exact display-driver initialization for the owned LILYGO revision.

The integrated IR block keeps `IR_RX` on GPIO39 and `IR_TX` on GPIO40. The receive sensor is a 38 kHz demodulating device. The transmit LEDs need a transistor/FET driver and current-limiting designed for the measured supply; do not drive them directly from a GPIO. The Adafruit #5990 board draws up to about 400 mA while transmitting from 5 V, so the carrier's 3.3 V regulator and switch must be sized from the actual implementation's pulse current. If reproducing Adafruit's circuit, retain the required attribution/share-alike notice in the project files.

## What is changed now vs. what still blocks fabrication

The firmware pin definitions and USB-serial button event handling are updated for Back/Menu, and the BOM now lists the required design items with unresolved ratings. The wiring map, PCB footprints, copper routes, port selector schematic, and IR discrete circuit are **not yet changed or verified**. They must be updated together in EasyEDA after identifying exact connector modules and measuring the complete 5 V load. This avoids silently treating a planning block diagram as a wired, current-rated PCB.

Before releasing fabrication files, verify: exact LILYGO USB-C/VBUS behavior; Pi OTG and HAT upstream wiring/role; the selected 2:1 selector's VBUS/ID behavior; USB-C sink module output; measured peak current for Pi, hub devices, display, ESP32, radios and IR; switch/fuse/copper ratings; connector pinouts; and physical fit of the three panel ports and the added buttons.

## References

- [Raspberry Pi Zero 2 W product page](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) — distinguishes the OTG micro-USB port from the separate power input.
- [Raspberry Pi power guidance](https://www.raspberrypi.com/documentation/computers/getting-started.html) — recommends 5 V / 2.5 A for Pi Zero boards.
- [Raspberry Pi USB gadget-mode guide](https://www.raspberrypi.com/news/usb-gadget-mode-ssh-over-usb/) — gadget connection uses the Zero's OTG port, not PWR IN.
- [Waveshare USB HUB HAT](https://www.waveshare.com/wiki/USB_HUB_HAT) — HAT uses the Pi Zero USB connection for its upstream data link.
- [Adafruit #5990 open hardware source](https://github.com/adafruit/Adafruit-Infrared-IR-Remote-Transceiver) — reference design, operating notes, and license.
- [Miady 2-pack listing specification](https://www.newegg.com/p/359-04A3-00191) — lists the bank's maximum output as 5 V / 2.4 A.
