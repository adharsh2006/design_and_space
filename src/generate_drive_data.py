import csv
import random
import time

def generate_data(num_rows=500):
    filename = 'data/large_drive_data.csv'
    
    # Starting coordinates (San Francisco)
    lat = 37.7749
    lon = -122.4194
    timestamp = 1682000000.0
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'accel_x', 'accel_y', 'accel_z', 'lat', 'lon']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for i in range(num_rows):
            # Normal driving noise
            ax = round(random.uniform(-0.05, 0.05), 2)
            ay = round(random.uniform(-0.05, 0.05), 2)
            az = round(random.uniform(0.95, 1.05), 2)
            
            # Inject Potholes periodically (roughly every 40-50 rows)
            if i > 0 and i % 45 == 0:
                # Strong spike
                az = round(random.uniform(2.6, 4.5), 2)
                ax = round(random.uniform(-0.5, 0.5), 2)
            elif i > 0 and (i - 1) % 45 == 0:
                # Aftershock/Dip
                az = round(random.uniform(-0.5, 0.5), 2)
            
            # Progress GPS slightly
            lat += 0.0001
            lon += 0.00005
            timestamp += 1.0
            
            writer.writerow({
                'timestamp': f"{timestamp:.1f}",
                'accel_x': f"{ax:.2f}",
                'accel_y': f"{ay:.2f}",
                'accel_z': f"{az:.2f}",
                'lat': f"{lat:.5f}",
                'lon': f"{lon:.5f}"
            })

    print(f"Successfully generated {num_rows} rows in {filename}")

if __name__ == "__main__":
    generate_data()
