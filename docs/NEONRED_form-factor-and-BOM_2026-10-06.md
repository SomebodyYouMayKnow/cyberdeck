# NEONRED portrait form factor and purchase BOM

This revision records the requested smaller, portrait-oriented, custom stepped board concept. It leaves component placement open for the user. The companion SVG contains only detached ALFA and Chameleon size guides plus proposed case and retainer holes; it does not imply that any module has been positioned on the carrier. The Raspberry Pi outline is omitted because the Pi is already owned and has a real PCB outline.

## Form factor draft

- Proposed maximum envelope: **120 × 180 mm**, portrait. This is a smaller area than the previous 200 × 120 mm interim outline.
- Proposed silhouette: stepped shoulders near the upper left and lower right, with mostly straight edges elsewhere. Finalize the notches only after choosing external connector locations and screw access.
- The SVG shows a conceptual stepped silhouette, detached guides, and draft hole positions. It is not a fabrication outline and does not replace the saved EasyEDA PCB.
- ALFA AWUS036ACS body outline is nominally 55 × 25 mm; the RP-SMA connector and antenna/cable keepout extend beyond that body.
- The Chameleon Ultra SE3 listing does not provide a mechanical drawing. The 40 × 24 mm rectangle in the SVG is explicitly a placeholder, not a verified SE3 dimension.
- Each device guide has two draft Ø2.7 mm non-plated holes for a printed retainer/clip. These holes fasten the holder to the carrier; they do not go through the ALFA or Chameleon enclosure. Their coordinates must be finalized after measuring the real devices and designing the clips.
- Four draft Ø3.2 mm non-plated M3 case-mount holes are placed inside the board perimeter, outside the device areas, with a 7 mm copper/mechanical keepout. A hole cannot be physically outside the PCB edge; use edge tabs if the case geometry needs mounting points farther out.
- LILYGO, CardKB, display, USB hub, external connectors, and all actual mounting-hole locations still need exact-revision measurements before the envelope can become a final PCB.

## Power and battery choice

Keep the battery external and feed each main device from a normal USB output. Do not route the power bank's main current through the carrier PCB. The already-owned Miady banks can remain available for individual-device tests, but the recorded 5 V / 2.4 A output may not supply all deck loads at once. If one replacement bank is desired, the Anker A1384 20,000 mAh / 30 W is a candidate commercial regulated power bank; its internal charging circuitry means a separate bare-cell charger module is not needed. Confirm simultaneous-port output and measure peak current for the actual system before relying on one bank.

## Purchase list

`BOM_NEONRED_purchase-list_2026-10-06.csv` contains unowned required purchase items, current known costs, links, and TBD prices where the exact selection is unresolved. The conditional Anker replacement is excluded from the required subtotal. The owned Pi, LILYGO board, Waveshare hub, and Miady banks are intentionally absent from the purchase rows. The old BOM remains as historical project data.

Known-priced required items subtotal: **$181.52**. This excludes TBD passives/IR parts, the custom PCB quote, shipping/tax, and the conditional Anker power bank.

## Before fabrication

Measure the ALFA adapter and Chameleon, design the printed retainers, confirm the case screw locations against the enclosure, choose case-side I/O openings, place components inside the final silhouette, then run ERC/DRC. The new SVG and BOM are planning artifacts, not evidence that the board is fabrication-ready.
