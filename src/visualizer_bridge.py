import csv
import time
import serial
import asyncio
import json
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import threading

app = FastAPI()

# Configuration
SERIAL_PORT = 'rfc2217://localhost:4000'
BAUD_RATE = 115200
DATA_FILE = 'data/large_drive_data.csv'
DELAY = 0.5  # Adjust for visual speed

# Global state for connected clients
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def library_connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# Background simulation task
async def run_simulation():
    print(f"Connecting to Wokwi at {SERIAL_PORT}...")
    try:
        ser = serial.serial_for_url(SERIAL_PORT, baudrate=BAUD_RATE, timeout=0.1)
    except Exception as e:
        print(f"Serial connection failed: {e}")
        return

    print("Connected! Waiting for boot...")
    await asyncio.sleep(2)

    if not os.path.exists(DATA_FILE):
        print(f"Data file {DATA_FILE} not found!")
        return

    print("Starting continuous simulation loop...")
    
    while True:
        with open(DATA_FILE, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ts = row.get('timestamp', '0')
                ax = row.get('accel_x', '0')
                ay = row.get('accel_y', '0')
                az = float(row.get('accel_z', '0'))
                lat = row.get('lat', '0')
                lon = row.get('lon', '0')
                
                # Send to Arduino
                data_str = f"DATA:{ts},{ax},{ay},{az},{lat},{lon}\n"
                ser.write(data_str.encode('utf-8'))
                
                # Prepare data for Frontend
                packet = {
                    "type": "telemetry",
                    "timestamp": ts,
                    "accel_z": az
                }
                await manager.broadcast(json.dumps(packet))
                
                # Check for alerts from Arduino
                while ser.in_waiting > 0:
                    line = ser.readline().decode('utf-8').strip()
                    if "POTHOLE DETECTED" in line:
                        alert_packet = {
                            "type": "alert",
                            "message": line,
                            "timestamp": ts
                        }
                        await manager.broadcast(json.dumps(alert_packet))
                        print(f"ALERT: {line}")
                
                await asyncio.sleep(DELAY)
        
        print("Dataset reached end. Restarting loop...")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(run_simulation())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.library_connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Serve the dashboard
if os.path.exists('dashboard'):
    app.mount("/", StaticFiles(directory="dashboard", html=True), name="dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
