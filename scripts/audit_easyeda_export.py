"""Summarize a native EasyEDA PCB JSON export without changing it."""

import collections
import json
import re
import sys
from pathlib import Path


def main(path: Path) -> None:
    pcb = json.loads(path.read_text(encoding="utf-8"))
    shapes = pcb["shape"]
    counts = collections.Counter(s.split("~", 1)[0] for s in shapes)
    print("shapes", len(shapes), dict(counts))
    print("copper areas:")
    for s in shapes:
        if s.startswith("COPPERAREA~"):
            p = s.split("~", 10)
            print(" ", "layer", p[2], "net", p[3], "id", p[7], "outline", p[4])

    net_pads: dict[str, list[tuple[str, str, str, str]]] = collections.defaultdict(list)
    components = []
    for s in shapes:
        if not s.startswith("LIB~"):
            continue
        sections = s.split("#@$")
        header = sections[0].split("~")
        package = re.search(r"package`([^`]*)", header[3])
        value = re.search(r"value`([^~`]*)", header[3])
        ref = "?"
        pads = []
        for section in sections[1:]:
            p = section.split("~")
            if p[0] == "TEXT" and len(p) > 10 and p[1] == "P":
                ref = p[10]
            elif p[0] == "PAD" and len(p) > 9:
                pads.append((p[7], p[8], p[2], p[3]))
        components.append((ref, package.group(1) if package else "", value.group(1) if value else "", header[1], header[2], pads))
        for net, number, x, y in pads:
            if net:
                net_pads[net].append((ref, number, x, y))
    print("components", len(components))
    print("GND pads", len(net_pads["GND"]))
    print("3V3 pads", len(net_pads["3V3"]))
    print("+3V3 pads", len(net_pads["+3V3"]))
    print("selected components:")
    for ref, package, value, x, y, pads in components:
        if not ref.startswith("PROX") or ref in {"PROXSV1", "PROXSV2"}:
            print(" ", ref, package, value, x, y, "GND", [(n, x, y) for net, n, x, y in pads if net == "GND"][:12])
    print("GND pads by ref:", dict(collections.Counter(ref for ref, *_ in net_pads["GND"])))
    print("interface pad nets:")
    for ref, package, value, x, y, pads in components:
        if ref in {"A1", "IC1", "IC2", "U3", "PI1", "PROXSV1", "SW1"}:
            print(" ", ref, [(number, net) for net, number, _, _ in pads])
    print("GND tracks near A1:")
    for s in shapes:
        if not s.startswith("TRACK~"):
            continue
        p = s.split("~")
        if len(p) < 5 or p[3] != "GND":
            continue
        coords = [float(n) for n in p[4].split()]
        points = list(zip(coords[::2], coords[1::2]))
        if any(4380 < x < 4520 and 3750 < y < 3900 for x, y in points):
            print(" ", "layer", p[2], "width", p[1], "points", p[4], "id", p[5])
    print("top-level net names:", sorted({p[3] for s in shapes if (p := s.split("~", 5))[0] == "TRACK" and len(p) > 3})[:100])


if __name__ == "__main__":
    main(Path(sys.argv[1]))
