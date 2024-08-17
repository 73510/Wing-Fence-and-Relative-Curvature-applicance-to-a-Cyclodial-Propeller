#include <Servo.h>
#include "HX711.h"


//setting Servo
Servo ESC;

//Setting Tacho
unsigned long rpmtime;
float rpmfloat;
unsigned int rpm;
bool tooslow = 1;

const int INTERRUPT_SENSOR_PIN = 2;

//Setting LoadCell
const int LOADCELL_DOUT_PIN = 5;
const int LOADCELL_SCK_PIN = 6;
HX711 scale;
int powerLevel;

long zero = 1286527;
long _500g = 2136588;
long weight = 0;

bool test_mode = false;

void setup() {
  Serial.begin(9600); // Initialize the serial communication at 9600 baud rate
  TCCR3A = 0; //Named as Timer/Counter Control Register
  TCCR3B = 0b00000100; //Prescaler 256
  TIMSK3 = 0b00000001; //enable timer overflow
  
  ESC.attach(10);
  pinMode(2, INPUT);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  attachInterrupt(digitalPinToInterrupt(INTERRUPT_SENSOR_PIN), RPM, FALLING);
  //digitalPinToInterrupt(INTERRUPT_SENSOR_PIN)
}



void loop() {
  
  float cal_factor = (_500g-zero)/509;
  
  if (Serial.available()) { // Check if data is available to read
    powerLevel = Serial.parseInt(); // Parse the incoming integer value
  }
  
  int thrusttoservo = map(0, 100, 0, 90, powerLevel);
  
  ESC.write(thrusttoservo);
  
  Serial.print("thrust value: ");
  Serial.print(powerLevel);
    
  delay(1000);
  if (tooslow == 1) {
    Serial.print("slow");
  }
  else {
    rpmfloat = 60 / (rpmtime/ float((16000000/256)));
    rpm = round(rpmfloat);Serial.print(" rpm : ");
    Serial.print(rpm/4);
  }

  if (scale.is_ready()) {
    long reading = scale.read();
    Serial.print("  HX711 reading: ");
    Serial.print(reading);
    Serial.print("  HX711 recalibration: ");
    Serial.print((reading-zero)/cal_factor);
  } else {
    Serial.print("HX711 not found.");
  }

  Serial.println();
}


ISR(TIMER3_OVF_vect) {
  tooslow = 1;
}
void RPM () {
  rpmtime = TCNT3;
  TCNT3 = 0;
  tooslow = 0;
}

