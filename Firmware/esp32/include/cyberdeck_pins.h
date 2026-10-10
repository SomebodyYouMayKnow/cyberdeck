#pragma once

// Pin assignments match the NEONRED EasyEDA schematic (2026-10-06).
// Change these only after changing and re-verifying the schematic.
namespace CyberdeckPins {
constexpr int ENCODER_A = 1;
constexpr int ENCODER_B = 2;
constexpr int ENCODER_BUTTON = 42;

// Navigation buttons: normally open to GND, using internal pull-ups.
constexpr int BUTTON_BACK = 43;
constexpr int BUTTON_MENU = 44;
constexpr int BUTTON_UP = 41;
constexpr int BUTTON_DOWN = 46;

constexpr int RADIO_SCK = 12;
constexpr int RADIO_MOSI = 11;
constexpr int RADIO_MISO = 13;
constexpr int RADIO1_CSN = 10;
constexpr int RADIO1_CE = 14;
constexpr int RADIO2_CSN = 15;
constexpr int RADIO2_CE = 16;

constexpr int IR_RX = 39;
constexpr int IR_TX = 40;

}
