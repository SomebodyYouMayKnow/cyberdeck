# Stardance funding and shipping checklist — Cyberdeck

**Status snapshot:** 2026-10-03. This separates the funding request from the physical build. Funding is requested from a complete design package before parts are bought. Shipping/Stardust comes after the physical device is assembled.

## Phase 1 — create the Stardance project and record work

- [ ] Create or sign in to a Stardance account. You must be eligible for the program and complete the account details yourself.
- [ ] Create a new **Hardware** project on Stardance and set its title, short description, and public GitHub source URL.
- [ ] Start Lapse before continuing design work, or create a Markdown build journal if Lapse is unavailable.
- [ ] Add design devlogs that explain your own decisions, revisions, problems, and next steps.
- [ ] Ask for feedback in `#stardance-help` or from other makers and record the feedback plus changes made.

## Phase 2 — funding-request design package

### Already done

- [x] Public GitHub repository: https://github.com/SomebodyYouMayKnow/cyberdeck
- [x] Commit and publish the core design package on GitHub.
- [x] Organize the repository into `cad/`, `PCB/`, `Firmware/`, `production/`, and `docs/`.
- [x] Publish a linked root `BOM.csv` and the BOM workbook.
- [x] Publish the current PCB source, schematic source, wiring map, DRC evidence, and 1:1 mounting template.
- [x] Publish editable OpenSCAD enclosure source, Fusion-importable DXF, layout SVG, and mechanical-validation document.
- [x] Publish untested starter firmware: ESP32 pin-map/I2C/radio/IR code, Pi serial bridge, and Chameleon BLE discovery scaffold.
- [x] Add a license and `.gitignore`.

### Still needed before clicking **Request funding**

- [ ] Finish the enclosure as a detailed, electronics-inclusive CAD assembly. It needs the case, lid, display, keyboard, Pi, USB HAT, ESP32, Chameleon, battery, carrier PCB, cables, screws/standoffs, antenna arms, and openings positioned in one assembly.
- [ ] Save the editable Fusion source file, such as `assembled-cyberdeck.f3d`.
- [ ] Export the full assembly as `assembled-cyberdeck.step`. Stardance says a funding submission without an electronics-inclusive STEP file will not be approved.
- [ ] Export the individual printable case parts as STEP/STL where relevant.
- [ ] Use accurate component envelopes or manufacturer STEP models in the CAD assembly. Mark dimensions that still need physical checking.
- [ ] Take screenshots/renders of the **digital** full CAD assembly. These are required for review; they are not photos of a completed physical build.
- [ ] Take a screenshot of the PCB layout and a schematic/wiring-diagram image from the current files.
- [ ] Write the final root `README.md` yourself. Stardance explicitly does not allow an AI-generated README.
- [ ] In your README, add: what the project is; why you are making it; subsystem explanation; CAD render; PCB screenshot; wiring diagram; how to reproduce it; and the BOM table.
- [ ] Confirm every BOM line has the correct quantity, price or clearly marked TBD status, and a purchase link.
- [ ] Keep the current firmware source in the repository. It may be untested for funding, but it must be present.
- [ ] Choose a funding tier in Stardance. The reviewer can move it up or down. Current published limits are B up to $25, A up to $120, S up to $200, and X up to $600 case-by-case.
- [ ] From the Stardance project page, click **Request funding** and submit the public repository link after the items above are present.

## Do **not** require these before funding

- [x] You do not need to buy the requested parts first.
- [x] You do not need to 3D-print the enclosure first.
- [x] You do not need to fabricate the PCB first.
- [x] You do not need physical build photos before requesting funding.
- [x] You do not need successful hardware tests before requesting funding. Firmware can be untested.

## Phase 3 — after funding and parts arrive

- [ ] Confirm exact part revisions and measure all physical modules, connectors, cable bends, and screw locations.
- [ ] Print the 1:1 template and check its 100 mm calibration line.
- [ ] Test-fit the Pi, HAT header slot, keyboard, ESP32, display, Chameleon, battery, cables, antennas, and all mounts before final fabrication.
- [ ] Correct the CAD and PCB from physical measurements; rerun final DRC/ERC.
- [ ] Export final Gerbers and drill files as `production/gerbers.zip` before ordering the carrier PCB.
- [ ] Print the case, assemble the carrier PCB, mount the modules, and add insulation/strain relief.
- [ ] Flash and test the ESP32/Pi firmware one subsystem at a time: keyboard, encoder, radios, IR, display, USB HAT, Wi-Fi, and Chameleon BLE discovery.
- [ ] Update the repository with the final CAD/STEP, Gerbers, firmware changes, wiring photos, and build notes.

## Phase 4 — ship the completed project for Stardust

- [ ] Add real photos or a video showing the completed cyberdeck and its working functions.
- [ ] Update the README with build photos, measured changes, and tested behavior.
- [ ] Ship the completed project from the Stardance project page. This sends it to review for Stardust, separate from the funding request.

## Current funding blockers

1. A Stardance account/project and work log need to be created by you.
2. The CAD is still a parametric concept; it needs a complete Fusion assembly and an electronics-inclusive STEP export.
3. The final README must be written by you and include digital renders/screenshots.
4. Feedback must be requested and documented.

Sources: [Stardance hardware shipping guide](https://stardance.hackclub.com/resources/shipping-hardware), [starting-hardware guide](https://stardance.hackclub.com/resources/starting-hardware), and [hardware funding tiers](https://stardance.hackclub.com/resources/tiers).

