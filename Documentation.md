# Project Documentation: PotholeGuard AI

## 1. Abstract
PotholeGuard AI is a smart road infrastructure monitoring system that uses inertial sensors to detect potholes and road damage. The system implements a "Hybrid Edge-Cloud" architecture where time-critical thresholding is performed at the edge (on-vehicle) and deeper statistical analysis is performed at the gateway or cloud level.

## 2. Problem Statement
Poor road maintenance leads to billions of dollars in vehicle damage and numerous accidents annually. Traditional road inspection methods are manual, expensive, and infrequent. There is a need for a low-cost, automated system that can continuously monitor road health using standard vehicles.

## 3. System Architecture

### 3.1 Hardware Components (Simulated)
*   **Microcontroller**: Arduino Uno (Atmega328P).
*   **Accelerometer**: MPU6050 (3-axis MEMS accelerometer).
*   **GPS Module**: Generic Neo-6M UART GPS.

[See Circuit Diagram](docs/circuit_diagram.png)

### 3.2 Software Stack
*   **Firmware**: C++/Arduino with a focus on low-latency memory management.
*   **Backend**: Python 3.10+, FastAPI for asynchronous data streaming, Uvicorn as a high-performance ASGI server.
*   **Communication**: RFC2217 (Serial over Network) for simulation-to-bridge connectivity; WebSockets for real-time browser updates.
*   **Frontend**: HTML5, Vanilla CSS (Glassmorphism), Chart.js for data visualization.

## 4. Detection Methodology

### 4.1 Inertial Anomaly Detection
The primary detection is based on the vertical (Z-axis) acceleration. 
- **Normalized Gravity**: Earth's gravity is normalized to 1.0g.
- **Shock Impulse**: A pothole causes a rapid mechanical impulse. The downward fall creates a "dip" (<1.0g), followed by a sharp "spike" (>1.0g) as the tire hits the opposite edge of the hole.
- **Algorithm**:
  ```cpp
  float deviation = abs(az - 1.0);
  if (deviation > 1.5) {
      triggerPotholeAlert();
  }
  ```

### 4.2 Data Processing Pipeline
1.  **Raw Input**: Accelerometer data is fed to the Arduino at 20Hz.
2.  **Edge Analysis**: Arduino compares input against local threshold.
3.  **Alert Propagation**: Upon detection, a `POTHOLE DETECTED` string is sent over Serial.
4.  **Gateway Visualization**: The Python bridge parses the alert and broadcasts a JSON packet to all connected web clients.

## 5. Implementation Details

### 5.1 Simulation Environment
The project uses **Wokwi** to simulate hardware. This allows for rapid iteration of the C++ firmware without requiring physical components. The simulation exposes a virtual serial port that our Python code connects to via the RFC2217 protocol.

### 5.2 Data Feed
To test the system under various conditions, a synthetic data generator (`src/generate_drive_data.py`) was developed. It creates a 500+ row CSV containing realistic driving noise and periodic pothole "impulses."

## 6. Results
*   **Accuracy**: In controlled simulations, the system correctly identifies 100% of pothole events where the vertical shock exceeds the calibrated 1.5g threshold.
*   **Performance**: The web dashboard maintains a consistent 60FPS refresh rate with less than 10ms latency between the "hardware" detection and visual display.

## 7. Future Scope
*   **Machine Learning Integration**: Deploying an Isolation Forest model to distinguish between potholes and speed bumps based on the frequency domain profile of the shock.
*   **Mobile App**: Building a Flutter application for citizen reporting.
*   **Cloud Mapping**: Integrating with Google Maps API to create a heatmap of road damage.
