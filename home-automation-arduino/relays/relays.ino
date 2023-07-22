#include <Arduino.h>
#include <Wire.h>
#include <PZEM004Tv30.h>

#define RELAY_1_PIN 8 
#define RELAY_2_PIN 9 
#define RELAY_3_PIN 7 
#define RELAY_4_PIN 6 

#define RELAY_5_PIN 3
#define RELAY_6_PIN 5
#define RELAY_7_PIN 4
#define RELAY_8_PIN 2

PZEM004Tv30 pzem(10, 11);
unsigned long previousMillis = 0;
const long interval = 5000;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);

  // Set the pin modes for the relay pins
  pinMode(RELAY_1_PIN, OUTPUT);
  pinMode(RELAY_2_PIN, OUTPUT);
  pinMode(RELAY_3_PIN, OUTPUT);
  pinMode(RELAY_4_PIN, OUTPUT);
  pinMode(RELAY_5_PIN, OUTPUT);
  pinMode(RELAY_6_PIN, OUTPUT);
  pinMode(RELAY_7_PIN, OUTPUT);
  pinMode(RELAY_8_PIN, OUTPUT);

  // Turn off all the relays
  digitalWrite(RELAY_1_PIN, LOW);
  digitalWrite(RELAY_2_PIN, LOW);
  digitalWrite(RELAY_3_PIN, LOW);
  digitalWrite(RELAY_4_PIN, LOW);
  digitalWrite(RELAY_5_PIN, LOW);
  digitalWrite(RELAY_6_PIN, LOW);
  digitalWrite(RELAY_7_PIN, LOW);
  digitalWrite(RELAY_8_PIN, LOW);
}

void loop() {

  unsigned long currentMillis = millis();
  float current = pzem.current();
  float power = pzem.power();
  float energy = pzem.energy();

  if (Serial.available()) {
    String incomingData = Serial.readStringUntil('\n');
    incomingData.trim();
    incomingData.toUpperCase();

    if (incomingData.startsWith("L")) {
      if (incomingData.startsWith("LBR")) {
        controlLight1(incomingData.substring(3));
      } else if (incomingData.startsWith("LB")) {
        controlLight2(incomingData.substring(2));
      } else if (incomingData.startsWith("LK")) {
        controlLight3(incomingData.substring(2));
      } else if (incomingData.startsWith("LL")) {
        controlLight4(incomingData.substring(2));
      }
    } else if (incomingData.startsWith("O")) {
      if (incomingData.startsWith("OBR")) {
        controlOutlet1(incomingData.substring(3));
      } else if (incomingData.startsWith("OB")) {
        controlOutlet2(incomingData.substring(2));
      } else if (incomingData.startsWith("OK")) {
        controlOutlet3(incomingData.substring(2));
      } else if (incomingData.startsWith("OL")) {
        controlOutlet4(incomingData.substring(2));
      }
    }
  }

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    if (current != NAN) {
      Serial.print("current: ");
      Serial.print(current);
      Serial.println(" A");
    } else {
      Serial.println("Error reading current");
    }


    if (current != NAN) {
      Serial.print("power: ");
      Serial.print(power);
      Serial.println(" W");
    } else {
      Serial.println("Error reading power");
    }

    if (current != NAN) {
      Serial.print("energy: ");
      Serial.print(energy, 6);
      Serial.println(" kWh");
    } else {
      Serial.println("Error reading energy");
    }
  }
}

void controlLight1(String light1Status) {
  Serial.println("light(BR)-status: " + light1Status);
  if (light1Status == "HIGH") {
    digitalWrite(RELAY_1_PIN, HIGH);
  }
  else if (light1Status == "LOW") {
    digitalWrite(RELAY_1_PIN, LOW);
  }
  Serial.flush();
}


void controlLight2(String light2Status) {
  Serial.println("light(B)-status: " + light2Status);
  if (light2Status == "HIGH") {
    digitalWrite(RELAY_2_PIN, HIGH);
  }
  else if (light2Status == "LOW") {
    digitalWrite(RELAY_2_PIN, LOW);
  }
  Serial.flush();
}

void controlLight3(String light3Status) {
  Serial.println("light(K)-status: " + light3Status);
  if (light3Status == "HIGH") {
    digitalWrite(RELAY_3_PIN, HIGH);
  }
  else if (light3Status == "LOW") {
    digitalWrite(RELAY_3_PIN, LOW);
  }
  Serial.flush();
}

void controlLight4(String light4Status) {
  Serial.println("light(L)-status: " + light4Status);
  if (light4Status == "HIGH") {
    digitalWrite(RELAY_4_PIN, HIGH);
  }
  else if (light4Status == "LOW") {
    digitalWrite(RELAY_4_PIN, LOW);
  }
  Serial.flush();
}

void controlOutlet1(String outlet2Status) {
  Serial.println("outlet(BR)-status: " + outlet2Status);
  if (outlet2Status == "HIGH") {
    digitalWrite(RELAY_5_PIN, HIGH);
  }
  else if (outlet2Status == "LOW") {
    digitalWrite(RELAY_5_PIN, LOW);
  }
  Serial.flush();
}

void controlOutlet2(String outlet1Status) {
  Serial.println("outlet(B)-status: " + outlet1Status);
  if (outlet1Status == "HIGH") {
    digitalWrite(RELAY_6_PIN, HIGH);
  }
  else if (outlet1Status == "LOW") {
    digitalWrite(RELAY_6_PIN, LOW);
  }
  Serial.flush();
}

void controlOutlet3(String outlet3Status) {
  Serial.println("outlet(K)-status: " + outlet3Status);
  if (outlet3Status == "HIGH") {
    digitalWrite(RELAY_7_PIN, HIGH);
  }
  else if (outlet3Status == "LOW") {
    digitalWrite(RELAY_7_PIN, LOW);
  }
  Serial.flush();
}

void controlOutlet4(String outlet4Status) {
  Serial.println("outlet(L)-status: " + outlet4Status);
  if (outlet4Status == "HIGH") {
    digitalWrite(RELAY_8_PIN, HIGH);
  }
  else if (outlet4Status == "LOW") {
    digitalWrite(RELAY_8_PIN, LOW);
  }
  Serial.flush();
}
