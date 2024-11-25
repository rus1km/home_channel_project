import threading
import time
import logging
from alerts import get_air_raid_alert_status
from weather import get_air_quality_index, get_aqi_display
from telegram import send_message, update_pinned_message
from power import power_monitor

# Set up the interval for checking air raid and AQI updates
CHECK_INTERVAL = 30.0            # Check air raid alert every 30 seconds
AQI_CHECK_INTERVAL = 3600.0    # Check AQI and temperature every 1 hour

CURRENT_STATUS = {
    "alert": 0,
    "power": None,
    "aqi": None,
    "temp": None
}

def monitor_power():
    previous_power_status = None
    power_gen = power_monitor()

    # Continuous loop to check power changes in real time
    for current_power_status in power_gen:
        CURRENT_STATUS["power"] = current_power_status
        if current_power_status != previous_power_status:
            power_message = "🔋 Power restored." if current_power_status == 1 else "🪫 Power outage detected."
            send_message(power_message)
            previous_power_status = current_power_status
            update_message()

def monitor_alerts_and_aqi():
    previous_alert_status = 0
    previous_aqi_status = 0
    last_aqi_check = 0.0

    while True:
        try:
            # Check air raid alert status
            CURRENT_STATUS["alert"] = get_air_raid_alert_status()
            if CURRENT_STATUS["alert"] != previous_alert_status:
                alert_message = "🚨 Air Raid Alert!" if CURRENT_STATUS["alert"] == 1 else "✅ Air Raid Over."
                send_message(alert_message)
                previous_alert_status = CURRENT_STATUS["alert"]
                update_message()

            # Check AQI and temperature if an hour has passed since the last check
            current_time = time.time()
            if current_time - last_aqi_check >= AQI_CHECK_INTERVAL:
                aqi_data = get_air_quality_index()

                # Ensure aqi_data is valid and contains the expected keys
                if aqi_data and "aqi" in aqi_data and "temperature" in aqi_data:
                    CURRENT_STATUS["aqi"] = aqi_data["aqi"]
                    CURRENT_STATUS["temp"] = aqi_data["temperature"]
                    logging.info(f"Updated AQI: {CURRENT_STATUS['aqi']}")
                    logging.info(f"Updated temp: {CURRENT_STATUS['temp']}")

                    # Send AQI message if AQI is at an unhealthy level
                    if CURRENT_STATUS["aqi"] >= 100 and CURRENT_STATUS["aqi"] > previous_aqi_status:
                        send_message(f"💨 Air quality has worsened. AQI {CURRENT_STATUS['aqi']}")
                    elif CURRENT_STATUS["aqi"] < 100 and previous_aqi_status >= 100: 
                        send_message(f"😊 Air quality has improved. AQI {CURRENT_STATUS['aqi']}")
                    previous_aqi_status = CURRENT_STATUS["aqi"]
                else:
                    logging.error("Invalid AQI data received. Setting defaults.")
                    CURRENT_STATUS["aqi"] = "N/D"
                    CURRENT_STATUS["temp"] = "N/D"

                last_aqi_check = current_time  # Update last AQI check time
                update_message()

            # Wait before the next air raid alert check
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            logging.error(f"Error in monitor_alerts_and_aqi: {e}")
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt: 
            logging.info("Shutting down monitor.")

def update_message():
    # Update the pinned message with current statuses only
    aqi_display = get_aqi_display(CURRENT_STATUS["aqi"])
    full_message = (
        f"📢 {'🚨' if CURRENT_STATUS['alert'] == 1 else '✅'} | "
        f"🔌 {'🔋' if CURRENT_STATUS['power'] == 1 else '🪫'} | "
        f"💨 {aqi_display} | "
        f"🌡️ {CURRENT_STATUS['temp']}°C"
    )
    update_pinned_message(full_message)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Save logs to a file
        logging.StreamHandler()          # Print logs to the terminal
    ]
)

def main():
    # Start the power monitoring in a separate thread for real-time response
    power_thread = threading.Thread(target=monitor_power)
    power_thread.daemon = True
    power_thread.start()

    # Start the main loop for alerts and AQI
    monitor_alerts_and_aqi()

if __name__ == "__main__":
    main()