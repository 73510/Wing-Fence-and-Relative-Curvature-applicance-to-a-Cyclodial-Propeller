#include <Servo.h>

Servo ESC;

void setup() {
  Serial.begin(9600); // Initialize the serial communication at 9600 baud rate
  ESC.attach(8);
}

int thrustValue;
void loop() {
  if (Serial.available()) { // Check if data is available to read
    thrustValue = Serial.parseInt(); // Parse the incoming integer value
  }
  
  int thrusttoservo = map(0, 100, 0, 90, thrustValue);
  
  ESC.write(thrusttoservo);
  
  delay(50);
  Serial.print("thrust value: ");
  Serial.println(thrustValue);
}
