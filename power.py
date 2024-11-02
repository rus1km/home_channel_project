# power.py
import serial
import time

# Adjust the port and baudrate to match your setup
SERIAL_PORT = "/dev/cu.usbserial-10"  # Replace with the correct port, e.g., "/dev/ttyUSB0" on Linux or "COM3" on Windows
BAUD_RATE = 9600

def read_voltage():
    # Open serial port
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)  # Allow time for Arduino to reset and start sending data

        while True:
            # Read a line of data from the serial port
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").strip()
                print(f"Voltage reading: {line}")  # Print or save the reading as needed

try:
    read_voltage()
except KeyboardInterrupt:
    print("Program stopped.")