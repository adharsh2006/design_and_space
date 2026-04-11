# PotholeGuard AI: Real-time Edge-AI Pothole Detection

![Pothole Detection Dashboard](docs/demonstration.gif)

## 📌 Project Overview

**PotholeGuard AI** is a professional-grade automated pothole detection system designed for real-time road surface monitoring. By leveraging **Edge Computing** on a simulated Arduino Uno and a modern **Web Dashboard**, the system identifies hazardous road conditions with near-zero latency.

This project demonstrates the powerful combination of **Mechanical Engineering (Sensors)**, **Embedded Systems (Arudino)**, and **Modern Software (FastAPI/WebSockets)** to solve real-world infrastructure problems.

---

## 🛠️ System Architecture

The project employs a multi-stage architecture to balance speed and intelligence:

1.  **Sensor Layer (Edge)**: An Arduino Uno (simulated in Wokwi) reads data from an MPU6050 Accelerometer. It performs high-speed Z-axis anomaly detection using a precision threshold algorithm.
2.  **Gateway Layer (Bridge)**: A Python-based FastAPI bridge connects to the simulated hardware, streams telemetry data, and broadcasts alerts.
3.  **Visualization Layer (Dashboard)**: A clean, light-mode web dashboard provides real-time analytics, showing acceleration shocks and historical detection logs.

---

## 🚀 Key Features

*   **Real-time Telemetry**: 60FPS live acceleration graphing using Chart.js.
*   **Edge-Processed Alerts**: Instant "Pothole Detected" identification powered by Arduino.
*   **Continuous Simulation**: Built-in data looping for long-duration demonstrations.
*   **Professional Aesthetics**: Sophisticated, light-mode dashboard suitable for industrial presentations.
*   **Sub-ms Latency**: Local processing on the simulated "car" ensures no danger is missed.

---

## 📂 Project Architecture & File Roles

To ensure a successful submission, here is a detailed breakdown of the project files and their specific roles:

### 🎮 Hardware Simulation (Wokwi)
*   `pothole_detector/`: Contains the **Arduino Source Code** (`.ino`). This is the "Brain" on the vehicle that performs real-time shock detection.
*   `diagram.json`: The **Circuit Map**. Defines how the Arduino, MPU6050 Accelerometer, and GPS are wired together.
*   `wokwi.toml`: The **Simulation Config**. Configures the Wokwi CLI to run the compiled firmware.

### 🧠 Backend & Intelligence (Python)
*   `src/visualizer_bridge.py`: The **Nerve Center**. It bridges the gap between the virtual hardware (Wokwi) and the visual dashboard.
*   `src/generate_drive_data.py`: The **Data Sim Tool**. Generates the 500+ row synthetic dataset for testing.

### 📊 Monitoring Dashboard (Frontend)
*   `dashboard/index.html`: The **Visual Interface**. Displays the real-time Z-axis graph, threshold lines, and detection status alerts.

### 📄 Documentation & Media
*   `README.md`: Overview and installation guide.
*   `Documentation.md`: Deep technical documentation.
*   `docs/circuit_diagram.png`: Engineering illustration of the hardware.
*   `docs/demonstration.webp`: Video demonstration of the system in action.

### 💾 Data Storage
*   `data/large_drive_data.csv`: The primary dataset for simulation.

---

## 🛠️ Getting Started

### Prerequisites

*   Python 3.8+
*   Wokwi CLI (Installation: `npm install -g wokwi-cli`)

### Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/adharsh2006/design_and_space.git
    cd design_and_space
    ```
2.  **Install Python Dependencies**:
    ```bash
    pip install fastapi uvicorn websockets pyserial
    ```
3.  **Set Up Wokwi Token**:
    Obtain a token from [wokwi.com/dashboard/ci](https://wokwi.com/dashboard/ci) and set it in your environment:
    ```bash
    $env:WOKWI_CLI_TOKEN="your_token_here"
    ```

### Running the Simulation

1.  **Start the Wokwi Simulation**:
    ```bash
    .\wokwi-cli.exe
    ```
2.  **Start the Backend Bridge**:
    ```bash
    python src/visualizer_bridge.py
    ```
3.  **View the Dashboard**:
    Open [http://localhost:8000](http://localhost:8000) in your web browser.

---

## 🖥️ Detection Logic

The system identifies potholes by measuring the deviation of vertical acceleration (**Az**) from standard gravity (**1.0g**):
*   **Threshold**: `|Az - 1.0| > 1.5g`
*   **Edge Logic**: Processed on the Arduino to minimize communication delay.
*   **AI Insight**: In a production environment, this data is further analyzed using Isolation Forest models to filter false positives like speed bumps.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**Developed for the Pothole Detection Mini-Project Submission.**
