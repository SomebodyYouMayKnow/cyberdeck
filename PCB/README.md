# NEONRED PCB order candidate

The active EasyEDA project is `cyberdeck-completed`. These are the final files exported from its live PCB on 2026-10-18 after saving and rerunning EasyEDA DRC:

- [PCB_cyberdeck-completed-order-candidate-2026-10-18.json](PCB_cyberdeck-completed-order-candidate-2026-10-18.json) — native EasyEDA JSON source export.
- [NEONRED_Gerber_bare-board-order_2026-10-18.zip](NEONRED_Gerber_bare-board-order_2026-10-18.zip) — cleaned fabrication archive for upload; it omits EasyEDA's non-fabrication DocumentLayer from the original generated archive.
- [NEONRED_Gerber_order-candidate_2026-10-18.zip](NEONRED_Gerber_order-candidate_2026-10-18.zip) — unmodified EasyEDA-generated archive, retained for traceability.
- [NEONRED_READINESS_CHECK_2026-10-18.md](../docs/NEONRED_READINESS_CHECK_2026-10-18.md) — audit, power boundary, and remaining prototype tests.
- [BOM.csv](../BOM.csv) — project purchase list and board quote.

The live EasyEDA Design Manager showed **29/29 nets** and **DRC Errors (0)** immediately before Gerber generation. The Gerber generator reported **2 copper layers**, **210 × 110 mm**, and a JLCPCB preview of **$14.88 for five green boards**, excluding shipping and tax. The cleaned upload archive contains top/bottom copper, top/bottom solder mask, top silkscreen, top paste, the board outline, plated/non-plated/via drills, and the order note. The manufacturing outline is `Gerber_BoardOutlineLayer.GKO`.

This clears the exported geometry for a **bare-board prototype order**. It does not clear electrical operation or assembly. No PCB assembly option is included; modules and through-hole parts must be sourced and fitted separately. Mechanical fit remains unverified and was outside this pass.

## Power boundary

`JP4` carries `+5V_EXT` (pin 1), GND (pin 2), `3V3_AUX` (pin 3), and GND (pin 4). They are power inputs, not outputs. The carrier contains no battery charger, 5 V converter, input fuse, or reverse-polarity protection. Keep the Pi on its own intact micro-USB cable into `PWR IN`; do not route Pi/HAT current through JP4 or inject a second source into the Pi-to-HAT USB cable. Power `+5V_EXT` from a regulated 5 V source and `3V3_AUX` from an external 3.3 V regulator; check voltage and polarity at JP4 before inserting modules.

The BOM's INIU 20 Ah bank is a candidate for the Pi branch only: its simultaneous multi-port output is limited to 5 V/3 A. The owned Miady bank is listed as the separate auxiliary source, subject to checking its label. This split is a proposed prototype wiring arrangement, not a measured power budget. Simultaneous load on the Pi/HAT USB branch and runtime remain unverified.
