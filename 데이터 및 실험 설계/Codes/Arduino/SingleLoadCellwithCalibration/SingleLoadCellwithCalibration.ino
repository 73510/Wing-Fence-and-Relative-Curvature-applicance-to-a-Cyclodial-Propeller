#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 5;
const int LOADCELL_SCK_PIN = 6;

HX711 scale;

void setup() {
  Serial.begin(57600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
}

void loop() {
  
  long zero = 329244;
  long weight_read = 638642;
  long weight = 185.5;
  
  float cal_factor = (weight_read-zero)/weight;

  if (scale.is_ready()) {
    long reading = scale.read();
    Serial.print("HX711 reading: ");
    Serial.println(reading);
    Serial.print("HX711 recalibration: ");
    Serial.println((reading-zero)/cal_factor);
  } else {
    Serial.println("HX711 not found.");
  }

  delay(1000);
  
}
