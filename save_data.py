import serial
import csv
import time

# Replace with your ESP8266 port (e.g., "COM3" for Windows, "/dev/ttyUSB0" for Linux/macOS)
ESP_PORT = "COM5"
BAUD_RATE = 115200
CSV_FILE = "groundwater_data.csv"

# Open serial connection
ser = serial.Serial(ESP_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow ESP8266 to reset

# Open CSV file for writing
with open(CSV_FILE, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Water_Level_1 (cm)", "Water_Level_3 (cm)"])  # CSV Header

    while True:
        try:
            line = ser.readline().decode("utf-8").strip()
            if line and "Timestamp" not in line:  # Ignore header line from ESP8266
                print("Received:", line)
                data = line.split(",")  # Split CSV data
                writer.writerow(data)  # Save to file
                file.flush()  # Ensure data is written immediately
        except KeyboardInterrupt:
            print("\nStopping data collection.")
            break
        except Exception as e:
            print("Error:", e)

# Close serial connection
ser.close()
