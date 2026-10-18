# PCB label correction — 2026-10-17

Updated from the live `cyberdeck-completed` EasyEDA PCB export. Corrected the silkscreen control labels to match the button locations: `BACK` and `UP` on the upper row; `MENU` and `DOWN` on the lower row; `SELECT` beneath the separate right-side switch; `ENTER` by the rotary encoder. Removed crowded default value/reference text from the tactile-switch footprints. Added compact component value labels and polarity marks.

The live EasyEDA Design Manager showed **DRC Errors (0)** after the label adjustment. The exported board contains 36 component footprints. This update is silkscreen-only; no pads, traces, nets, or component positions were edited. This DRC result checks EasyEDA’s configured rules only; it is not an electrical or manufacturing sign-off.

Files: `PCB_cyberdeck-completed-label-fix-2026-10-17.json` is the live EasyEDA source export; `screenshots/NEONRED-2D-button-label-fix-2026-10-17.png` is the matching 2D render.
