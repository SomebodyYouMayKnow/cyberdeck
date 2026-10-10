# NEONRED — current goal and hardware expansion

Updated: 2026-10-09. This note is the current high-level target and supersedes the older HDMI-based project descriptions. On 2026-10-09, I opened the live EasyEDA Standard `neonred` project and exported its current schematic and PCB to `PCB/neonred-live-schematic_2026-10-09.json` and `PCB/neonred-live-PCB_2026-10-09.json`, with PNG views in `PCB/screenshots/`. The requested Proxmark3/RTL-SDR/antenna expansion has **not** been laid out; these are baseline exports, not an updated fabrication design.

## Final version description

NEONRED is a portable, modular cyberdeck and authorized electronics/security-learning workbench built around a Raspberry Pi Zero 2 W and a LILYGO T-Display-S3 AMOLED. The Pi runs Linux and connects to the Waveshare USB HUB HAT. The LILYGO board supplies the ESP32-S3 control interface and its integrated AMOLED screen. The current version has **no separate HDMI display**.

The device combines a CardKB keyboard, rotary encoder and navigation controls with IR receive/transmit hardware, two nRF24L01+ modules, the Chameleon Ultra SE3, and an ALFA USB Wi-Fi adapter. The proposed expansion adds a separately mounted Proxmark3 instrument and an RTL-SDR Blog V4 receiver, plus an external 2.4 GHz antenna for the ESP32 if the exact LILYGO board revision supports a switchable RF feed. Modules with USB or antenna connections remain replaceable serviceable devices; the carrier PCB provides mounting and correctly routed interfaces, rather than copying complete complex RF products onto the carrier.

Software modes under consideration are the NEONRED control firmware, passive Flock You detection, and ESP32 Marauder experimentation in an isolated, authorized lab. These are not simultaneous capabilities on one ESP32: each firmware image replaces the others unless a separate ESP32 is added and independently supported. The exact LILYGO display/board support for Marauder and Flock You requires a port and bench test before it can be claimed as working.

## What can physically go on the PCB

| Addition | Practical integration | Open issue |
|---|---|---|
| Proxmark3 | Mount a complete Proxmark3 RDV4 or other selected assembled unit as a removable USB module. Provide a retainer, accessible USB connection, and room for its LF/HF antenna loops. | “Proxmark3” has multiple hardware variants. Select the exact unit and measure it. Do not replace it with an unverified home-designed RF clone. Keep its loop antennas clear of metal and other coils. |
| RTL-SDR Blog V4 | Mount the intact USB-A dongle at the Pi USB hub; reserve a 50-ohm SMA feedthrough/pigtail and antenna clearance. Leave airflow around its metal enclosure. | The V4 is a receive-only USB dongle, 500 kHz–1.766 GHz, 250–270 mA typical, with USB-A male and SMA. It cannot directly receive X/K/Ka police-radar bands. The linked detector software describes external block downconverters; select and validate those separately. Its manufacturer has announced the V4 end of life, so confirm availability before listing it as a guaranteed purchase. |
| ESP32 external antenna | Reserve a mechanically accessible antenna connector and keepout only after confirming an RF feed point and selector on the exact owned LILYGO revision. If that board has no documented external-antenna option, use the onboard antenna or a different ESP32-S3 module with a factory u.FL/IPEX connector. | The ESP32-S3 is 2.4 GHz Wi-Fi/Bluetooth; it does not provide 5 GHz Wi-Fi. The vendor documentation for a different T-Display-S3 board describes moving an RF-selection resistor, but that must not be copied to the AMOLED board without its exact schematic and visual inspection. |
| Flock You | Treat as a separate, receive-only firmware experiment; the referenced project describes passive 2.4 GHz Wi-Fi frame detection. | Its published default target is a Seeed XIAO ESP32-S3. Porting the display/buttons and validating the exact LILYGO board is still required. |
| ESP32 Marauder | Treat as a separate firmware mode on a compatible ESP32 target, used only in an isolated lab on owned or explicitly authorized systems. | The current LILYGO T-Display-S3 AMOLED is not listed as a ready-made target in the upstream compatibility table. Display, buttons, flash layout and GPIO assignments must be ported and tested. It cannot run alongside NEONRED UI or Flock You on the same chip at the same time. |

The RTL-SDR V4’s SMA connector is an RF input, not a connector to solder directly to GPIO or a PCB antenna trace. The Proxmark device likewise has dedicated LF/HF antenna circuits; preserve the complete selected device and its correct antenna arrangement. Any coaxial feedthroughs should be 50-ohm RF connectors appropriate to the chosen device, and must be isolated from mounting metal where the antenna design requires it.

## Power and performance checks

The V4’s published typical current is 250–270 mA; the ALFA adapter, HAT, Proxmark and Pi add to the system load. The Raspberry Pi Zero 2 W is specified around a 5 V / 2.5 A supply recommendation. The Waveshare hub adds ports, not unlimited power. Bench-test the complete load from the selected source and hub before assuming one bank can run all modules. Keep the SDR’s software-controlled bias tee disabled unless the selected antenna accessory explicitly needs it. Do not connect independent USB VBUS outputs together or route unmeasured high-current device power through narrow carrier traces.

The linked radar detector project describes an SDR plus external downconverters to translate radar-frequency signals into the V4’s tunable range. This is a substantial, separate RF subsystem, not a firmware-only feature. The proposed use here is passive reception and alerts; no radar transmission or interference is part of this design.

## Authorized scope

- Linux development, programming, diagnostics, and hardware bring-up.
- IR learning/testing on the user's own remotes.
- NFC/RFID experiments using tags, cards and systems the user owns or has explicit permission to test.
- Wi-Fi, Bluetooth and nRF24 experiments on owned equipment or in an isolated authorized lab. No disrupting other people's networks or radio communications.
- Passive reception for the proposed SDR detector and passive Flock You experiment, subject to local law.
- Physical integration of serviceable off-the-shelf modules, custom PCB design, enclosure CAD, firmware and documentation.

## Required before changing/fabricating the PCB

1. Use the live EasyEDA exports as the starting baseline. After the mechanical and electrical choices below are verified, update the project and export a new schematic, PCB source, and screenshots to `PCB/`.
2. Confirm the exact LILYGO model/revision and inspect its manufacturer schematic for an external antenna selector/feed. Do not add a connector footprint based only on the standard T-Display-S3 instructions.
3. Choose the exact Proxmark3 hardware and RTL-SDR V4 (or an available equivalent); obtain their dimensions, mounting points, connector positions and antenna clearances.
4. Decide whether the Pi Zero 2 W has enough CPU and USB power headroom for one SDR, the ALFA adapter and the other peripherals. Test incrementally; the software's advertised support is not a performance guarantee for this deck.
5. Choose the radar-band downconverter set and antenna arrangement, then verify its output frequencies stay inside the selected SDR's tuning range.
6. Allocate separate, replaceable mounts and USB paths for the Proxmark and RTL-SDR. Avoid routing high-speed USB over long unshielded PCB traces; use short controlled connections or certified cables.
7. Update schematic, PCB footprints, board outline/keepouts, mounting template, current budget, BOM and screenshots together. Run ERC/DRC and check the physical assemblies before calling the PCB fabrication-ready.

## References

- [Proxmark3 RDV4 product/hardware overview](https://proxmark.com/proxmark-3-hardware/proxmark-3-rdv4/) and [Proxmark3 hardware description](https://github.com/Proxmark/proxmark3/wiki/Hardware-Description)
- [RTL-SDR Blog V4 datasheet](https://www.rtl-sdr.com/wp-content/uploads/2024/12/RTLSDR_V4_Datasheet_V_1_0.pdf) and [V4 end-of-life notice](https://www.rtl-sdr.com/rtl-sdr-blog-v4-end-of-line/)
- [Requested radar-detector project](https://github.com/rayhe/sdr-radar-detector)
- [LILYGO AMOLED series hardware and pinout sources](https://github.com/Xinyuan-LilyGO/LilyGo-AMOLED-Series)
- [ESP32 Marauder supported hardware](https://github.com/justcallmekoko/ESP32Marauder/wiki/supported-hardware) and [FAQ](https://github.com/justcallmekoko/ESP32Marauder/wiki/faq)
- [Flock You project](https://github.com/colonelpanichacks/flock-you)
