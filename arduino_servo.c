#include <Servo.h>

Servo servothumb;
Servo servoindex;
Servo servomiddle;
Servo servoring;
Servo servopinky;

int servoPositions[5];    //store servo positions (0 or 180)
String inputString = "";  //string to hold incoming data
bool newData = false;     //flag for new data availability

void setup() {
  Serial.begin(9600);
  servothumb.attach(11);
  servoindex.attach(9);
  servopinky.attach(10);
  servoring.attach(6);
  servomiddle.attach(5);

  Serial.println("Setup complete. Waiting for data...");
}

void loop() {
  receiveData();
  if (newData) {
    updateServos();
    newData = false;
  }
}

void receiveData() {
  while (Serial.available() > 0) {
    char c = Serial.read();
    if (c == '\n') {  //end of input detected
      parseData();
      newData = true;
      inputString = "";  //reset input string for new data
    } else {
      inputString += c;  //append incoming characters
    }
  }
}

void parseData() {
  int index = 0;
  int startIndex = 0;

  for (int i = 0; i < inputString.length(); i++) {
    if (inputString.charAt(i) == ',' || i == inputString.length() - 1) {
      String valueStr = inputString.substring(startIndex, i + (i == inputString.length() - 1));
      servoPositions[index] = (valueStr.toInt() == 1) ? 165 : 15;
      index++;
      startIndex = i + 1;
    }
  }
  
  Serial.print("Parsed servo positions: ");
  for (int i = 0; i < 5; i++) {
    Serial.print(servoPositions[i]);
    Serial.print(" ");
  }
  Serial.println();
}

void updateServos() {
  servopinky.write(servoPositions[4]);
  servoring.write(servoPositions[3]);
  servomiddle.write(servoPositions[2]);
  servoindex.write(servoPositions[1]);
  servothumb.write(servoPositions[0]);

  Serial.println("Servo positions updated.");
}
