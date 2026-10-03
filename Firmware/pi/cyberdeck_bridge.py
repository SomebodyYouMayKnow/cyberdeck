#!/usr/bin/env python3
"""USB-serial bridge between the Raspberry Pi and the Cyberdeck ESP32.

Run this after the ESP32 has been flashed and connected by an intact USB data
cable. It prints CardKB, encoder, radio and IR events as JSON and accepts
commands on stdin. This is a bring-up program, not an installed service.
"""

import argparse
import json
import queue
import sys
import threading
import serial


def serial_reader(port: serial.Serial, events: queue.Queue[str]) -> None:
    while True:
        try:
            line = port.readline().decode("utf-8", errors="replace").strip()
        except serial.SerialException as exc:
            events.put(json.dumps({"type": "serial_error", "detail": str(exc)}))
            return
        if line:
            events.put(line)


def keyboard_reader(commands: queue.Queue[str]) -> None:
    for line in sys.stdin:
        command = line.strip()
        if command:
            commands.put(command)


def main() -> int:
    parser = argparse.ArgumentParser(description="Cyberdeck ESP32 USB bridge")
    parser.add_argument("--port", default="/dev/ttyACM0", help="ESP32 USB serial device")
    parser.add_argument("--baud", type=int, default=115200)
    args = parser.parse_args()

    try:
        port = serial.Serial(args.port, args.baud, timeout=0.2)
    except serial.SerialException as exc:
        print(f"Cannot open {args.port}: {exc}", file=sys.stderr)
        return 2

    events: queue.Queue[str] = queue.Queue()
    commands: queue.Queue[str] = queue.Queue()
    threading.Thread(target=serial_reader, args=(port, events), daemon=True).start()
    threading.Thread(target=keyboard_reader, args=(commands,), daemon=True).start()

    print("Cyberdeck bridge ready. Commands: PING, STATUS, RADIO1:text, RADIO2:text, IR_NEC:00FF:12ED")
    port.write(b"STATUS\n")

    while True:
        try:
            command = commands.get_nowait()
            port.write((command + "\n").encode("utf-8"))
        except queue.Empty:
            pass

        try:
            raw = events.get(timeout=0.1)
        except queue.Empty:
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            print(json.dumps({"type": "unparsed", "raw": raw}))
            continue
        print(json.dumps(event, sort_keys=True))


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("\nCyberdeck bridge stopped")
