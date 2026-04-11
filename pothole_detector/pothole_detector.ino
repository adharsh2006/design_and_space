// Automated Pothole Detection System
// Designed to be run in Simulation (Wokwi / Proteus)

// If SIMULATION_MODE is defined, it reads from Serial instead of real I2C/UART sensors
#define SIMULATION_MODE 1

#define Z_ACCEL_THRESHOLD 1.5 // 1.5g difference from 1g gravity

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ; // wait for serial port to connect
  }
  Serial.println("System Booted. Pothole Detector Ready.");
  
  if (SIMULATION_MODE) {
    Serial.println("SIMULATION MODE ACTIVE. Waiting for data format: DATA:ts,ax,ay,az,lat,lon");
  } else {
    // Initialize real MPU6050 and GPS here
    Serial.println("HARDWARE MODE ACTIVE. (Not implemented in this sketch)");
  }
}

void processSimulatedData(String dataLine) {
  // Expected Format: DATA:timestamp,accel_x,accel_y,accel_z,lat,lon
  // E.g., DATA:1682000004.0,0.05,0.08,3.45,37.7753,-122.4194

  // Remove "DATA:"
  dataLine.replace("DATA:", "");
  
  // Basic parsing (for simplicity using String indexOf and substring)
  int comma1 = dataLine.indexOf(',');
  int comma2 = dataLine.indexOf(',', comma1 + 1);
  int comma3 = dataLine.indexOf(',', comma2 + 1);
  int comma4 = dataLine.indexOf(',', comma3 + 1);
  int comma5 = dataLine.indexOf(',', comma4 + 1);
  
  if (comma1 == -1 || comma5 == -1) {
    // Invalid format
    return;
  }
  
  String ts_str = dataLine.substring(0, comma1);
  String ax_str = dataLine.substring(comma1 + 1, comma2);
  String ay_str = dataLine.substring(comma2 + 1, comma3);
  String az_str = dataLine.substring(comma3 + 1, comma4);
  String lat_str = dataLine.substring(comma4 + 1, comma5);
  String lon_str = dataLine.substring(comma5 + 1);
  
  float az = az_str.toFloat();
  
  // Calculate Z acceleration anomaly (assuming resting is ~1.0g or -1.0g)
  // We check absolute deviation from 1.0g, but it might be upside down, so let's just 
  // check if the absolute change is very high. Wait, in our dataset resting is ~1.0.
  // Pothole triggers when az > 2.0 or az < 0.0 (roughly)
  float deviation = abs(abs(az) - 1.0);
  
  if (deviation > Z_ACCEL_THRESHOLD) {
    Serial.print("POTHOLE DETECTED | ");
    Serial.print("TS: ");
    Serial.print(ts_str);
    Serial.print(" | Z_ACCEL: ");
    Serial.print(az, 2);
    Serial.print(" | LAT: ");
    Serial.print(lat_str);
    Serial.print(" | LON: ");
    Serial.println(lon_str);
    
    // In a real system, you might trigger an LED or I2C display here
  }
}

void loop() {
  if (SIMULATION_MODE) {
    if (Serial.available() > 0) {
      String incomingString = Serial.readStringUntil('\n');
      incomingString.trim();
      
      if (incomingString.startsWith("DATA:")) {
        processSimulatedData(incomingString);
      }
    }
  } else {
    // Read from real MPU6050 and GPS
    // If pothole detected -> log to SD Card
  }
}
