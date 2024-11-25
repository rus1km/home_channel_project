# power.py
import logging
import serial
import serial.tools.list_ports
import time

# Baud rate and sleep constants
BAUD_RATE = 9600
SLEEP_TIME = 5  # Interval for retrying port connection

def find_arduino_port():
    """Scan for Arduino port with a fallback for known port."""
    KNOWN_PORT = '/dev/ttyUSB0'
    ports = list(serial.tools.list_ports.comports())
    logging.info("Available ports:", [port.device for port in ports])  # Debugging line

    # Check known port first
    if KNOWN_PORT in [port.device for port in ports]:
        return KNOWN_PORT

    # Fallback to automatic detection
    for port in ports:
        try:
            ser = serial.Serial(port.device, BAUD_RATE, timeout=1)
            line = ser.readline().decode("utf-8").strip()
            if line.replace(".", "", 1).isdigit():
                ser.close()
                return port.device
            ser.close()
        except (OSError, serial.SerialException):
            continue
    return None

def power_monitor():
    ser = None
    port = find_arduino_port()
    while True:
        if ser is None or not ser.is_open:
            try:
                ser = serial.Serial(port, BAUD_RATE, timeout=1)
                time.sleep(2)  # Allow Arduino to reset
                logging.info(f"Arduino connected on {port}.")
            except serial.SerialException:
                logging.info(f"Failed to open port {port}. Retrying...")
                time.sleep(SLEEP_TIME)
                continue

        # If connected, read data continuously
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode("utf-8").strip()
                voltage = float(line)
                power_status = 1 if voltage == 0 else 0
                yield power_status
        except ValueError:
            logging.info("Received non-numeric data. Ignoring line.")
        except serial.SerialException:
            logging.info("Arduino disconnected unexpectedly.")
            ser = None  # Reset connection to retry
            time.sleep(SLEEP_TIME)