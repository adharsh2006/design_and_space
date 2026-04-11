import csv
import time
import serial
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Pothole Detection Data Feeder")
    parser.add_argument('--port', type=str, default='rfc2217://localhost:4000', help='Serial port to connect to (e.g., COM1 or rfc2217://localhost:4000 for Wokwi)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate')
    parser.add_argument('--file', type=str, default='data/real_drive_data.csv', help='Path to real driving CSV dataset')
    parser.add_argument('--delay', type=float, default=1.0, help='Delay between sending rows in seconds')
    args = parser.parse_args()

    print(f"Connecting to {args.port} at {args.baud} baud...")
    
    try:
        # Pyserial supports tcp sockets via "socket://host:port" format
        ser = serial.serial_for_url(args.port, baudrate=args.baud, timeout=1)
    except Exception as e:
        print(f"Failed to connect: {e}")
        print("Make sure Wokwi or Proteus is running and the port is available.")
        return

    print("Connected! Waiting 2 seconds for Arduino to boot...")
    time.sleep(2)
    
    if not os.path.exists(args.file):
        print(f"Dataset file {args.file} not found!")
        return

    print(f"Starting to feed data from {args.file}...")
    
    with open(args.file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Read data from CSV
            ts = row.get('timestamp', '0')
            ax = row.get('accel_x', '0')
            ay = row.get('accel_y', '0')
            az = row.get('accel_z', '0')
            lat = row.get('lat', '0')
            lon = row.get('lon', '0')
            
            # Format: DATA:timestamp,ax,ay,az,lat,lon\n
            data_str = f"DATA:{ts},{ax},{ay},{az},{lat},{lon}\n"
            print(f"Sending: {data_str.strip()}")
            ser.write(data_str.encode('utf-8'))
            
            # Check for any alerts coming back from Arduino
            while ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if line:
                    if "POTHOLE DETECTED" in line:
                        print(f"\n[ALERT] => {line}")
                        # Log to file
                        with open("potholes_logged.txt", "a") as logf:
                            logf.write(line + "\n")
                    else:
                        print(f"[ARDUINO MSG]: {line}")
            
            time.sleep(args.delay)
            
    print("Finished feeding dataset.")
    ser.close()

if __name__ == '__main__':
    main()
