# power.py
import serial
import time

# Adjust the port and baud rate to match your setup
SERIAL_PORT = "/dev/cu.usbserial-10"  # Replace with the correct port
BAUD_RATE = 9600

def power_monitor():
    ser = None
    while True:
        if ser is None or not ser.is_open:
            # Try to connect to Arduino
            try:
                ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
                time.sleep(2)  # Allow Arduino to reset if just connected
                print("Arduino connected.")
            except serial.SerialException:
                print("Waiting for Arduino...")
                time.sleep(60)  # Wait before retrying
                continue  # Retry the loop

        # If connected, attempt to read data
        if ser.in_waiting > 0:
            line = ser.readline().decode("utf-8").strip()
            try:
                voltage = float(line)
                # Return 1 if voltage is 0 (power is on), otherwise 0
                power_status = 1 if voltage == 0 else 0
                yield power_status
            except ValueError:
                print("Error parsing voltage data")

        # Handle unexpected disconnections
        if not ser.is_open:
            print("Arduino disconnected.")
            ser = None
            time.sleep(5)  # Retry connection in a few seconds