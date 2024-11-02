# power.py
import serial
import time

# Adjust the port and baudrate to match your setup
SERIAL_PORT = "/dev/cu.usbserial-10"  # Replace with the correct port
BAUD_RATE = 9600

def power_monitor():
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        time.sleep(2)  # Allow Arduino to reset

        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").strip()
                try:
                    voltage = float(line)
                    # Return 1 if voltage is 0 (power is on), otherwise 0
                    power_status = 1 if voltage == 0 else 0
                    yield power_status
                except ValueError:
                    print("Error parsing voltage data")
