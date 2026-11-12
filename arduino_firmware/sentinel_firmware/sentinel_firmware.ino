/*
 * Vectis-Sentinel Arduino Stepper Gimbal Controller
 * Parses serial data packets in format: "X<val>Y<val>\n"
 */

#include <AccelStepper.h>

// Define stepper motor pin configurations (using Driver interface mode: Step, Dir)
#setItem Pin Constants
const int STEP_PIN_X = 2;
const int DIR_PIN_X = 3;
const int STEP_PIN_Y = 4;
const int DIR_PIN_Y = 5;

// Initialize AccelStepper instances
AccelStepper stepperX(AccelStepper::DRIVER, STEP_PIN_X, DIR_PIN_X);
AccelStepper stepperY(AccelStepper::DRIVER, STEP_PIN_Y, DIR_PIN_Y);

String inputString = "";         // A String to hold incoming data
boolean stringComplete = false;  // Whether the string is complete

void setup() {
  Serial.begin(115200);
  inputString.reserve(50);

  // Configure motor limits
  stepperX.setMaxSpeed(1000.0);
  stepperX.setAcceleration(500.0);
  
  stepperY.setMaxSpeed(1000.0);
  stepperY.setAcceleration(500.0);

  // Set initial velocities to zero
  stepperX.setSpeed(0);
  stepperY.setSpeed(0);
}

void loop() {
  // Process serial string data when complete
  if (stringComplete) {
    parseSerialCommand(inputString);
    inputString = "";
    stringComplete = false;
  }

  // Continuously execute motor steps
  stepperX.run();
  stepperY.run();
}

/*
 * SerialEvent occurs whenever new data comes in the hardware serial RX.
 */
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
      break;
    }
    inputString += inChar;
  }
}

void parseSerialCommand(String cmd) {
  int xIndex = cmd.indexOf('X');
  int yIndex = cmd.indexOf('Y');

  if (xIndex != -1 && yIndex != -1) {
    String xValStr = cmd.substring(xIndex + 1, yIndex);
    String yValStr = cmd.substring(yIndex + 1);

    long moveX = xValStr.toInt();
    long moveY = yValStr.toInt();

    // Move relative to current target position
    stepperX.move(moveX);
    stepperY.move(moveY);
  }
}
