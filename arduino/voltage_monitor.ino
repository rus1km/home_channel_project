// A code for arduino voltage monitor. Use to create new sketch in Arduino IDE
// const int voltagePin = A0;  // Analog pin connected to the sensor's OUT
// float calibrationFactor = 0.036;  // Calibration factor for your sensor (find experimentally)

// void setup() {
//   Serial.begin(9600);  // Initialize serial communication at 9600 bps
// }

// void loop() {
//   int numSamples = 1000;  // Number of samples for accurate RMS calculation
//   float sum = 0.0;

//   for (int i = 0; i < numSamples; i++) {
//     int sensorValue = analogRead(voltagePin);
//     float voltage = sensorValue * (5.0 / 1023.0);  // Convert to voltage
//     sum += voltage * voltage;  // Sum of squares for RMS calculation
//     delay(1);  // Short delay for better sampling
//   }

//   float rmsVoltage = sqrt(sum / numSamples) * calibrationFactor;
//   Serial.print("RMS Voltage: ");
//   Serial.println(rmsVoltage);
//   delay(1000);  // Delay for readability
// }