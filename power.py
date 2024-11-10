# power.py
import serial
import serial.tools.list_ports
import time

# Baud rate and sleep constants
BAUD_RATE = 9600
SLEEP_TIME = 5  # Interval for retrying port connection

def find_arduino_port():
    """Scan for Arduino port by checking available USB ports."""
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        try:
            ser = serial.Serial(port.device, BAUD_RATE, timeout=1)
            # Try reading a line to confirm the connection
            line = ser.readline().decode("utf-8").strip()
            if line.replace(".", "", 1).isdigit():  # Expecting numeric data
                ser.close()
                return port.device  # Return the port if valid data is found
            ser.close()
        except (OSError, serial.SerialException):
            continue
    return None

def power_monitor():
    ser = None
    while True:
        if ser is None or not ser.is_open:
            # Attempt to locate and connect to Arduino
            port = find_arduino_port()
            if port:
                try:
                    ser = serial.Serial(port, BAUD_RATE, timeout=1)
                    time.sleep(2)  # Allow Arduino to reset
                    print(f"Arduino connected on {port}.")
                except serial.SerialException:
                    print(f"Failed to open port {port}. Retrying...")
                    time.sleep(SLEEP_TIME)
                    continue
            else:
                print("No Arduino detected. Scanning again...")
                time.sleep(SLEEP_TIME)
                continue

        # If connected, read data continuously
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").strip()
                voltage = float(line)
                # Determine power status based on voltage reading
                power_status = 1 if voltage == 0 else 0
                yield power_status
        except ValueError:
            print("Received non-numeric data. Ignoring line.")
        except serial.SerialException:
            print("Arduino disconnected unexpectedly.")
            ser = None  # Reset connection to retry
            time.sleep(SLEEP_TIME)