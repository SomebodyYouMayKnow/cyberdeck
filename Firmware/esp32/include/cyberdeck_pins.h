#pragma once

// Pin assignments are copied from outputs/wiring-map-simple-power.txt.
// Change these only after changing and re-verifying the carrier PCB.
namespace CyberdeckPins {
constexpr int I2C_SDA = 1;
constexpr int I2C_SCL = 41;

constexpr int RADIO_SCK = 12;
constexpr int RADIO_MOSI = 11;
constexpr int RADIO_MISO = 13;
constexpr int RADIO1_CSN = 10;
constexpr int RADIO1_CE = 14;
constexpr int RADIO2_CSN = 15;
constexpr int RADIO2_CE = 16;

constexpr int IR_RX = 39;
constexpr int IR_TX = 40;

constexpr uint8_t CARDKB_ADDRESS = 0x5F;
constexpr uint8_t ENCODER_ADDRESS = 0x36;
constexpr uint32_t I2C_CLOCK_HZ = 100000;
}

