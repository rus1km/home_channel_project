// A code for Arduino voltage monitor. Use to create new sketch in Arduino IDE

// const int voltagePin = A0;
// float calibrationFactor = 0.036;

// void setup() {
//   Serial.begin(9600);  // Initialize serial communication at 9600 bps
// }

// void loop() {
//   int numSamples = 1000;
//   float sum = 0.0;

//   for (int i = 0; i < numSamples; i++) {
//     int sensorValue = analogRead(voltagePin);
//     float voltage = sensorValue * (5.0 / 1023.0);
//     sum += voltage * voltage;
//     delay(1);
//   }

//   float rmsVoltage = sqrt(sum / numSamples) * calibrationFactor;
//   Serial.println(rmsVoltage);  // Send the voltage reading over serial
//   delay(1000);  // Wait 1 second before next reading
// }