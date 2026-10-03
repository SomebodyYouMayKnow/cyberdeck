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

- [ ] Finish the enclosure as a detailed, electronics-inclusive CAD assembly: case, lid, display, keyboard, Pi, USB HAT, ESP32, Chameleon, battery, carrier PCB, cables, screws/standoffs, antenna arms, and openings.
- [ ] Save the editable Fusion source file, such as `assembled-cyberdeck.f3d`.
- [ ] Export the full assembly as `assembled-cyberdeck.step`. Stardance says a funding submission without an electronics-inclusive STEP file will not be approved.
- [ ] Export the individual printable case parts as STEP/STL where relevant.
- [ ] Use accurate component envelopes or manufacturer STEP models in the CAD assembly. Mark dimensions that still need physical checking.
- [ ] Take digital full-CAD renders, plus PCB and schematic/wiring screenshots.
- [ ] Write the final root `README.md` yourself. Stardance explicitly does not allow an AI-generated README.
- [ ] Add to README: description, motivation, subsystem explanation, CAD render, PCB, wiring, reproduction steps, and BOM table.
- [ ] Confirm every BOM line has quantity, price or explicit TBD status, and a purchase link.
- [ ] Choose a funding tier: B up to $25; A up to $120; S up to $200; X up to $600 case-by-case. Reviewers can adjust the tier.
- [ ] From the project page, click **Request funding** with the public repository link.

## Not needed before funding

- [x] No parts purchase, 3D print, PCB fabrication, physical build photos, or hardware tests are required before requesting funding.
- [x] Firmware is present and may be untested.

## After funding and parts arrive

- [ ] Measure/test-fit components, cables, header slot, display, antennas and mounts.
- [ ] Update CAD/PCB from measurements and run final DRC/ERC.
- [ ] Export final Gerbers and drill files as `production/gerbers.zip`.
- [ ] Fabricate/assemble the case and carrier PCB, then test each subsystem.
- [ ] Update the repository with final CAD/STEP, Gerbers, firmware, wiring photos, and build notes.

## Ship later for Stardust

- [ ] Add real photos or video and tested behavior to README.
- [ ] Ship the completed project from its Stardance page for Stardust review.

Sources: [hardware shipping guide](https://stardance.hackclub.com/resources/shipping-hardware), [starting hardware](https://stardance.hackclub.com/resources/starting-hardware), [funding tiers](https://stardance.hackclub.com/resources/tiers).

