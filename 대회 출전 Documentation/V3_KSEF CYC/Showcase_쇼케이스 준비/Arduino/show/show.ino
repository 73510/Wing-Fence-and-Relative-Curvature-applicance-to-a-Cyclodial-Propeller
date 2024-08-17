#include <Servo.h>
#include "HX711.h"

// Servos for each propeller
Servo servoA, servoB, servoC;

// Tachometers variables
unsigned long rpmTimeA, rpmTimeB, rpmTimeC;
bool tooSlowA = true, tooSlowB = true, tooSlowC = true;

// Load Cells
HX711 loadCellA, loadCellC;
long weightA, weightB, weightC;

// Load Cell calibration and pins
long zeroA = 406051, zeroC = 332931;
long calFactorA = 1, calFactorC = 1;
const int LOADCELL_DOUT_PIN_A = 5; // Modify these pins as per your hardware setup
const int LOADCELL_SCK_PIN_A = 6;
const int LOADCELL_DOUT_PIN_C = 7; // Modify these pins as per your hardware setup
const int LOADCELL_SCK_PIN_C = 8;

int rpmA, rpmB, rpmC;
// Repeat for loadCellB and loadCellC with different pins

void setup() {
  Serial.begin(115200);



  // Setup Load Cells
  loadCellA.begin(LOADCELL_DOUT_PIN_A, LOADCELL_SCK_PIN_A);
  loadCellC.begin(LOADCELL_DOUT_PIN_C, LOADCELL_SCK_PIN_C);

  // Repeat setup for loadCellB and loadCellC with their respective pins

  // Setup Tachometers
  pinMode(2, INPUT); // Modify these pins as per your hardware setup
  pinMode(3, INPUT);
  pinMode(18, INPUT);
  
  attachInterrupt(digitalPinToInterrupt(2), RPM_A, FALLING);
  attachInterrupt(digitalPinToInterrupt(3), RPM_B, FALLING);
  attachInterrupt(digitalPinToInterrupt(18), RPM_C, FALLING);

  // Initialize Timers for Tachometers
  TCCR3A = 0; TCCR3B = 0b00000100; TIMSK3 = 0b00000001; // Timer 3
  TCCR4A = 0; TCCR4B = 0b00000100; TIMSK4 = 0b00000001; // Timer 4
  TCCR5A = 0; TCCR5B = 0b00000100; TIMSK5 = 0b00000001; // Timer 5
  
    // Setup Servos
  servoA.attach(9); // Modify these pins as per your hardware setup
  servoB.attach(10);
  servoC.attach(13);
}

void loop() {
  if (Serial.available()) {
    int powerA, powerB, powerC;
    sscanf(Serial.readStringUntil('\n').c_str(), "%d %d %d", &powerA, &powerB, &powerC);
    servoA.write(map(0, 100, 0, 90, powerA));
    servoB.write(map(0, 100, 0, 90, powerB));
    servoC.write(map(0, 100, 0, 90, powerC));
    
    Serial.print(powerA);
    Serial.print(powerB);
    Serial.print(powerC);
    Serial.println();
  }

  // Read and store weight from each load cell
  weightA = readWeight(loadCellA, calFactorA, zeroA);
  weightB = weightA;
  weightC = readWeight(loadCellC, calFactorC, zeroC);
  if (!tooSlowA) {
    rpmA = calculateRPM(rpmTimeA);
  }
  else rpmA = 0;
  if (!tooSlowB) {
    rpmB = calculateRPM(rpmTimeB);
  }
  else rpmB = 0;
  if (!tooSlowC) {
    rpmC = calculateRPM(rpmTimeC);
  }
  else rpmC = 0;
  Serial.print("A ");
  Serial.print(rpmA);
  Serial.print(' ');
  Serial.print(weightA);
  Serial.print('_');
  Serial.print("B ");
  Serial.print(rpmB);
  Serial.print(' ');
  Serial.print(weightB);
  Serial.print('_');
  Serial.print("C ");
  Serial.print(rpmC);
  Serial.print(' ');
  Serial.println(weightC);
  
  delay(200);
}

long readWeight(HX711 &loadCell, long calFactor, long zero) {
  if (loadCell.is_ready()) {
    long reading = loadCell.read();
    return (reading - zero) / calFactor;
   
  } else {
    return 0; // Error value
  }
}

float calculateRPM(unsigned long timerCount) {
  float rpmFloat = 60.0 * (16000000.0 / 256.0) / timerCount;
  return round(rpmFloat);
}

ISR(TIMER3_OVF_vect) { tooSlowA = true; }
ISR(TIMER4_OVF_vect) { tooSlowB = true; }
ISR(TIMER5_OVF_vect) { tooSlowC = true; }

void RPM_A() { rpmTimeA = TCNT3; TCNT3 = 0; tooSlowA = false; }
void RPM_B() { rpmTimeB = TCNT4; TCNT4 = 0; tooSlowB = false; }
void RPM_C() { rpmTimeC = TCNT5; TCNT5 = 0; tooSlowC = false; }
