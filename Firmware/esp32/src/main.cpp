#include <Arduino.h>
#include <SPI.h>
#include <Wire.h>
#include <RF24.h>
#include <IRremote.hpp>

#include "cyberdeck_pins.h"

// This firmware is deliberately a bring-up scaffold. It provides one serial
// protocol for the Pi and starts every peripheral in a safe idle state.
// Do not connect or power a signal harness while its source rail is off.

using namespace CyberdeckPins;

RF24 radio1(RADIO1_CE, RADIO1_CSN);
RF24 radio2(RADIO2_CE, RADIO2_CSN);
const uint8_t RADIO1_ADDRESS[6] = "CDR1";
const uint8_t RADIO2_ADDRESS[6] = "CDR2";
bool radio1Ready = false;
bool radio2Ready = false;
bool cardKbReady = false;
bool encoderReady = true;
int32_t encoderPosition = 0;
uint8_t encoderAB = 0;
bool lastButtonPressed = false;
unsigned long lastButtonEventMs = 0;

struct ButtonState {
  int pin;
  const char *name;
  bool lastPressed;
  unsigned long lastChangeMs;
};
ButtonState buttons[] = {
    {BUTTON_BACK, "back", false, 0},
    {BUTTON_MENU, "menu", false, 0},
    {BUTTON_UP, "up", false, 0},
    {BUTTON_DOWN, "down", false, 0},
};

char commandBuffer[128];
size_t commandLength = 0;
unsigned long lastScanMs = 0;
unsigned long lastCardKbPollMs = 0;

void event(const char *type, const char *detail) {
  Serial.printf("{\"type\":\"%s\",\"detail\":\"%s\"}\n", type, detail);
}

void eventNumber(const char *type, int32_t value) {
  Serial.printf("{\"type\":\"%s\",\"value\":%ld}\n", type, static_cast<long>(value));
}

bool configureRadio(RF24 &radio, const uint8_t *address, const char *name) {
  if (!radio.begin(&SPI)) {
    event("radio_error", name);
    return false;
  }
  radio.setPALevel(RF24_PA_MIN);       // Begin at the lowest transmit power.
  radio.setDataRate(RF24_1MBPS);
  radio.setChannel(76);
  radio.setRetries(5, 15);
  radio.openWritingPipe(address);
  radio.openReadingPipe(1, address);
  radio.startListening();
  event("radio_ready", name);
  return true;
}

void sendRadio(RF24 &radio, bool ready, const char *name, const char *payload) {
  if (!ready) {
    event("radio_error", "not_ready");
    return;
  }
  char packet[32] = {};
  strncpy(packet, payload, sizeof(packet) - 1);
  radio.stopListening();
  const bool sent = radio.write(packet, sizeof(packet));
  radio.startListening();
  event(sent ? "radio_sent" : "radio_failed", name);
}

void pollRadio(RF24 &radio, bool ready, const char *name) {
  if (!ready || !radio.available()) return;
  char packet[32] = {};
  radio.read(packet, sizeof(packet));
  Serial.printf("{\"type\":\"radio_rx\",\"radio\":\"%s\",\"payload\":\"%s\"}\n", name, packet);
}

void pollEncoder() {
  // Mechanical quadrature encoder with common pin grounded. INPUT_PULLUP
  // supplies the idle-high level; no external pull-up resistors are needed.
  static const int8_t transitions[16] = {
     0, -1,  1,  0,
     1,  0,  0, -1,
    -1,  0,  0,  1,
     0,  1, -1,  0
  };
  const uint8_t currentAB = (digitalRead(ENCODER_A) << 1) | digitalRead(ENCODER_B);
  const uint8_t index = (encoderAB << 2) | currentAB;
  const int8_t step = transitions[index];
  encoderAB = currentAB;
  if (step != 0) {
    encoderPosition += step;
    eventNumber("encoder_delta", step);
  }

  const bool pressed = digitalRead(ENCODER_BUTTON) == LOW;
  const unsigned long now = millis();
  if (pressed && !lastButtonPressed && now - lastButtonEventMs >= 35) {
    event("button", "select");
    lastButtonEventMs = now;
  }
  lastButtonPressed = pressed;
}

void pollNavigationButtons() {
  const unsigned long now = millis();
  for (auto &button : buttons) {
    const bool pressed = digitalRead(button.pin) == LOW;
    if (pressed != button.lastPressed && now - button.lastChangeMs >= 25) {
      button.lastPressed = pressed;
      button.lastChangeMs = now;
      if (pressed) event("button", button.name);
    }
  }
}

void pollCardKb() {
  const unsigned long now = millis();
  if (now - lastCardKbPollMs < 10) return;
  lastCardKbPollMs = now;

  const uint8_t requested = Wire.requestFrom(CARDKB_I2C_ADDRESS, static_cast<uint8_t>(1));
  if (requested == 0 || !Wire.available()) return;
  const uint8_t key = static_cast<uint8_t>(Wire.read());
  if (key == 0) return;

  // Keep the serial event valid JSON for printable ASCII keys. Non-ASCII
  // special-key codes are reported numerically and interpreted by the Pi.
  if (key >= 32 && key <= 126) {
    Serial.printf("{\"type\":\"key\",\"code\":%u,\"character\":\"", key);
    if (key == '"' || key == '\\') Serial.write('\\');
    Serial.write(key);
    Serial.println("\"}");
  } else {
    Serial.printf("{\"type\":\"key\",\"code\":%u}\n", key);
  }
}

void pollIrReceiver() {
  if (!IrReceiver.decode()) return;
  Serial.printf("{\"type\":\"ir_rx\",\"protocol\":%u,\"address\":%u,\"command\":%u}\n",
                static_cast<unsigned>(IrReceiver.decodedIRData.protocol),
                static_cast<unsigned>(IrReceiver.decodedIRData.address),
                static_cast<unsigned>(IrReceiver.decodedIRData.command));
  IrReceiver.resume();
}

void reportStatus() {
  Serial.printf("{\"type\":\"status\",\"radio1\":%s,\"radio2\":%s,\"encoder\":%s,\"keyboard\":%s}\n",
                radio1Ready ? "true" : "false", radio2Ready ? "true" : "false",
                encoderReady ? "true" : "false", cardKbReady ? "true" : "false");
}

void handleCommand(const char *command) {
  if (strcmp(command, "PING") == 0) {
    event("pong", "cyberdeck");
  } else if (strcmp(command, "STATUS") == 0) {
    reportStatus();
  } else if (strncmp(command, "RADIO1:", 7) == 0) {
    sendRadio(radio1, radio1Ready, "radio1", command + 7);
  } else if (strncmp(command, "RADIO2:", 7) == 0) {
    sendRadio(radio2, radio2Ready, "radio2", command + 7);
  } else if (strncmp(command, "IR_NEC:", 7) == 0) {
    // Format: IR_NEC:ADDRESS:COMMAND, both hexadecimal, for example IR_NEC:00FF:12ED.
    unsigned int address = 0;
    unsigned int irCommand = 0;
    if (sscanf(command + 7, "%x:%x", &address, &irCommand) == 2) {
      IrSender.sendNEC(address, irCommand, 0);
      event("ir_sent", "nec");
    } else {
      event("command_error", "bad_ir_nec");
    }
  } else {
    event("command_error", "unknown");
  }
}

void pollUsbSerial() {
  while (Serial.available()) {
    const char c = static_cast<char>(Serial.read());
    if (c == '\r') continue;
    if (c == '\n') {
      commandBuffer[commandLength] = '\0';
      if (commandLength > 0) handleCommand(commandBuffer);
      commandLength = 0;
    } else if (commandLength < sizeof(commandBuffer) - 1) {
      commandBuffer[commandLength++] = c;
    } else {
      commandLength = 0;
      event("command_error", "too_long");
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(250);
  event("boot", "cyberdeck_esp32");

  pinMode(ENCODER_A, INPUT_PULLUP);
  pinMode(ENCODER_B, INPUT_PULLUP);
  pinMode(ENCODER_BUTTON, INPUT_PULLUP);
  for (auto &button : buttons) pinMode(button.pin, INPUT_PULLUP);
  Wire.begin(CARDKB_SDA, CARDKB_SCL, 100000);
  Wire.beginTransmission(CARDKB_I2C_ADDRESS);
  cardKbReady = Wire.endTransmission() == 0;
  event(cardKbReady ? "keyboard_ready" : "keyboard_missing", "cardkb_0x5f_gpio1_gpio41");
  encoderAB = (digitalRead(ENCODER_A) << 1) | digitalRead(ENCODER_B);
  SPI.begin(RADIO_SCK, RADIO_MISO, RADIO_MOSI, RADIO1_CSN);
  radio1Ready = configureRadio(radio1, RADIO1_ADDRESS, "radio1");
  radio2Ready = configureRadio(radio2, RADIO2_ADDRESS, "radio2");

  event("encoder_ready", "gpio2_gpio3_button42_pullups");
  event("buttons_ready", "up45_down46_back43_menu44_select42_pullups");

  IrReceiver.begin(IR_RX, DISABLE_LED_FEEDBACK);
  IrSender.begin(IR_TX, DISABLE_LED_FEEDBACK);
  event("ir_ready", "rx39_tx40");
  reportStatus();
}

void loop() {
  pollUsbSerial();
  pollEncoder();
  pollNavigationButtons();
  pollCardKb();
  pollIrReceiver();
  pollRadio(radio1, radio1Ready, "radio1");
  pollRadio(radio2, radio2Ready, "radio2");

  if (millis() - lastScanMs >= 5000) {
    lastScanMs = millis();
    reportStatus();
  }
}
