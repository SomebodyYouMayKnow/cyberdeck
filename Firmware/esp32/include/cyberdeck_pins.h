#pragma once

// Pin assignments match the cyberdeck-completed carrier schematic.
// Change these only after changing and re-verifying the schematic.
namespace CyberdeckPins {
// CardKB uses GPIO1/GPIO41 for shifted I2C. Keep the quadrature encoder off
// those bus pins: its A/B phases use GPIO2/GPIO3.
constexpr int ENCODER_A = 2;
constexpr int ENCODER_B = 3;
constexpr int ENCODER_BUTTON = 42;
// The SELECT tact switch is wired in parallel with the encoder's push contact.
constexpr int BUTTON_SELECT = ENCODER_BUTTON;

// Navigation buttons: normally open to GND, using internal pull-ups.
constexpr int BUTTON_BACK = 43;
constexpr int BUTTON_MENU = 44;
constexpr int BUTTON_UP = 45;
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
