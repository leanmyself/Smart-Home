#include <Wire.h>
#include <Servo.h>
#include <DHT.h>

#define flamePin A0
#define rainPin A1
#define LDRPin A2
#define soilPin A3
#define gasPin A4

#define buzzer 2
#define DHTPIN 3
#define motionPin 4
#define servoPin 5 //window
#define fan1INA 7 //living-room
#define fan1INB 6 //living-room
#define fan2INA 9 //kitchen
#define fan2INB 8 //kitchen
#define fan3INA 11 //bedroom
#define fan3INB 10 //bedroom
#define motionLED 12
#define outdoorLED 13

#define DHTTYPE DHT22

volatile int soilMoisture = 0;
volatile int gasSensor = 0;
volatile int rainSensor = 0;
volatile int flameSensor = 0;

unsigned long previousMillis = 0;
const long interval = 5000;

Servo myservo;
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  dht.begin();

  myservo.attach(servoPin);
  myservo.write(0);

  pinMode(buzzer, OUTPUT);
  pinMode(gasPin, INPUT);
  pinMode(rainPin, INPUT);
  pinMode(soilPin, INPUT);
  pinMode(LDRPin, INPUT);
  pinMode(flamePin, INPUT);
  pinMode(motionLED, OUTPUT);
  pinMode(outdoorLED, OUTPUT);
  pinMode(fan1INA, OUTPUT);
  pinMode(fan1INB, OUTPUT);
  pinMode(fan2INA, OUTPUT);
  pinMode(fan2INB, OUTPUT);
  pinMode(fan3INA, OUTPUT);
  pinMode(fan3INB, OUTPUT);

  digitalWrite(fan1INA, LOW);
  digitalWrite(fan1INB, LOW);
  digitalWrite(fan2INA, LOW);
  digitalWrite(fan2INB, LOW);
  digitalWrite(fan3INA, LOW);
  digitalWrite(fan3INB, LOW);

}

void loop() {
  flameDetection();
  gasDetection();
  rainDetection();
  LDRModuleLED();
  PIRMotion();
  printingSensor();


  if (Serial.available()) {
    String incomingData = Serial.readStringUntil('\n');
    incomingData.trim();
    incomingData.toUpperCase();

    if (incomingData[0] == 'W') {
      controlWindow(incomingData.substring(1));
    }
    if (incomingData.startsWith("F")) {
      if (incomingData.startsWith("FBR")) {
        controlFan3(incomingData.substring(3));
      } else if (incomingData.startsWith("FK")) {
        controlFan2(incomingData.substring(2));
      } else if (incomingData.startsWith("FL")) {
        controlFan1(incomingData.substring(2));
      }
    }
  }

}

void controlWindow(String switchStatus) {
  Serial.println("Window-status: " + switchStatus);
  if (switchStatus == "HIGH") {
    myservo.write(0);

  }
  else if (switchStatus == "LOW") {
    myservo.write(180);
  }
  Serial.flush();
}

void LDRModuleLED() {
  int lightValue = analogRead(LDRPin);
  if (lightValue <= 500) {
    digitalWrite (outdoorLED, LOW);
  }
  else {
    digitalWrite (outdoorLED, HIGH);
  }
}


void controlFan1(String fan1Status) {
  Serial.println("fan(LR)-status: " + fan1Status);
  if (fan1Status == "HIGH") {
    analogWrite(fan1INA, 255);
    digitalWrite(fan1INB, LOW);
  }
  else if (fan1Status == "LOW") {
    digitalWrite(fan1INA, LOW);
    digitalWrite(fan1INB, LOW);
  }
  Serial.flush();
}


void controlFan2(String fan2Status) {
  Serial.println("fan(K)-status: " + fan2Status);
  if (fan2Status == "HIGH") {
    analogWrite(fan2INA, 255);
    digitalWrite(fan2INB, LOW);
  }
  else if (fan2Status == "LOW") {
    digitalWrite(fan2INA, LOW);
    digitalWrite(fan2INB, LOW);
  }
  Serial.flush();
}

void controlFan3(String fan3Status) {
  Serial.println("fan(BR)-status: " + fan3Status);
  if (fan3Status == "HIGH") {
    analogWrite(fan3INA, 255);
    digitalWrite(fan3INB, LOW);
  }
  else if (fan3Status == "LOW") {
    digitalWrite(fan3INA, LOW);
    digitalWrite(fan3INB, LOW);
  }
  Serial.flush();
}

int readSoilHumiditySensor() {
  soilMoisture = analogRead(soilPin);
  int soilPercentage = map(soilMoisture, 0, 1023, 0, 100);
  return soilPercentage;
}

int readGasSensor() {
  gasSensor = analogRead(gasPin);
  return gasSensor;
}

int readRainSensor() {
  rainSensor = analogRead(rainPin);
  return rainSensor;
}

int readFlameSensor() {
  flameSensor = analogRead(flamePin);
  return flameSensor;
}

int flameDetection() {
  readFlameSensor();
  const unsigned long toneDuration = 30000;  // 30 seconds

  if (flameSensor < 100) {
    tone(buzzer, 1000, toneDuration);
    delay(1000);
  } else {
    noTone(buzzer);
  }
}

int gasDetection() {
  readGasSensor();
  const unsigned long toneDuration = 30000;  // 30 seconds

  if (gasSensor > 240) {
    tone(buzzer, 2000, toneDuration);
    delay(1000);
  } else {
    noTone(buzzer);
  }
}

int rainDetection() {
  readRainSensor();
  const unsigned long toneDuration = 30000;  // 30 seconds

  if (rainSensor >= 100) {
    myservo.write(180);
  }
}

int printingSensor() {
  unsigned long currentMillis = millis();
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  float f = dht.readTemperature(true);
  float hif = dht.computeHeatIndex(f, h);

  if (currentMillis - previousMillis >= interval) {
    previousMillis = currentMillis;

    soilMoisture = readSoilHumiditySensor();
    gasSensor = readGasSensor();
    rainSensor = readRainSensor();
    flameSensor = readFlameSensor();

    Serial.print("soil: ");
    Serial.println(soilMoisture);

    Serial.print("rain: ");
    Serial.println(rainSensor);

    Serial.print("gas: ");
    Serial.println(gasSensor);

    Serial.print("flame: ");
    Serial.println(flameSensor);

    Serial.print(F("humidity: "));
    Serial.println(h);
    Serial.print(F("temperature: "));
    Serial.println(t);
    Serial.print(F("heat-index: "));
    Serial.println(hif);

  }
}

void PIRMotion() {
  int motion_detected = digitalRead(motionPin);
  if (motion_detected == HIGH) {
    digitalWrite(motionLED, HIGH);
  }
  else  {
    digitalWrite(motionLED, LOW);
  }
}
