# power.py
import serial
import serial.tools.list_ports
import time

# Baud rate for Arduino connection
BAUD_RATE = 9600
SLEEP_TIME = 30

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        try:
            ser = serial.Serial(port.device, BAUD_RATE, timeout=1)
            # Read a few lines to check for expected numeric output (voltage values)
            line = ser.readline().decode("utf-8").strip()
            for _ in range(3):  # Read multiple times to confirm
                if line.replace(".", "", 1).isdigit():  # Confirm it's a float-like string
                    ser.close()
                    return port.device  # Return the detected port
                line = ser.readline().decode("utf-8").strip()
            ser.close()
        except (OSError, serial.SerialException):
            continue
    return None

def power_monitor():
    ser = None
    while True:
        if ser is None or not ser.is_open:
            # Try to find and connect to Arduino on any port
            port = find_arduino_port()
            if port is not None:
                try:
                    ser = serial.Serial(port, BAUD_RATE, timeout=1)
                    time.sleep(2)  # Allow Arduino to reset if just connected
                    print(f"Arduino connected on {port}.")
                except serial.SerialException:
                    print("Failed to open port. Retrying...")
                    time.sleep(SLEEP_TIME)  # Wait before retrying
                    continue
            else:
                print("Waiting for Arduino on any USB port...")
                time.sleep(5)
                continue

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
            time.sleep(SLEEP_TIME)  # Retry connection in a few seconds
