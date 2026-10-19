# ESP32 ⇄ Pi serial protocol

The ESP32 and Pi communicate through an intact USB data cable. Serial speed is 115200 baud, UTF-8, one line per message.

## Pi to ESP32 commands

| Command | Effect |
| --- | --- |
| `PING` | Checks that the bridge is alive. |
| `STATUS` | Reports radio and encoder detection. |
| `RADIO1:text` | Sends up to 31 bytes through radio 1. |
| `RADIO2:text` | Sends up to 31 bytes through radio 2. |
| `IR_NEC:00FF:12ED` | Transmits an NEC IR code. Address and command are hexadecimal. |

## ESP32 to Pi events

Each event is a JSON object on one line. Types currently include `boot`, `status`, `key`, `encoder_delta`, `encoder_button`, `button`, `radio_rx`, `ir_rx`, `radio_sent`, `radio_failed`, and `command_error`.

CardKB emits `{"type":"key","code":113,"character":"q"}` for printable ASCII and `{"type":"key","code":128}` for special/control codes. The Pi bridge prints the event; mapping keys into Linux input devices still requires choosing and testing that behavior.
# Navigation-button event

The firmware reports each debounced press as a JSON line on the ESP32 USB serial connection:

    {"type":"button","detail":"back"}
    {"type":"button","detail":"menu"}

The existing rotary encoder rotation and push continue to report encoder_delta and encoder_button. These events are ready for the Pi bridge or a later AMOLED menu renderer. The current scaffold does not yet draw the menu on the ESP32 display.
