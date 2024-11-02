import threading
import time
from alerts import get_air_raid_alert_status
from weather import get_air_quality_index
from telegram import send_message, update_pinned_message
from power import power_monitor

# Set up the interval for checking air raid and AQI updates
CHECK_INTERVAL = 30  # Adjust as needed
CURRENT_STATUS = {
    "alert": 0,
    "power": None,
    "aqi": None
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
    previous_aqi_status = None

    while True:
        try:
            # Fetch air raid alert status and AQI
            CURRENT_STATUS["alert"] = get_air_raid_alert_status()
            CURRENT_STATUS["aqi"] = get_air_quality_index()

            # Send air raid alert message if there's a change
            if CURRENT_STATUS["alert"] != previous_alert_status:
                alert_message = "🚨 Air Raid Alert!" if CURRENT_STATUS["alert"] == 1 else "✅ Air Raid Over."
                send_message(alert_message)
                previous_alert_status = CURRENT_STATUS["alert"]
                update_message()

            # Send AQI message if AQI changes significantly
            if CURRENT_STATUS["aqi"] != previous_aqi_status:
                if CURRENT_STATUS["aqi"] >= 3:
                    send_message("💨 Air quality has worsened.")
                previous_aqi_status = CURRENT_STATUS["aqi"]
                update_message()

            # Wait before the next check for alerts and AQI
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print(f"Error in monitor_alerts_and_aqi: {e}")

def update_message():
    # Update the pinned message with current statuses only
    full_message = (
        f"📢 - {'🚨' if CURRENT_STATUS['alert'] == 1 else '✅'} | "
        f"💨 - {CURRENT_STATUS['aqi']} | "
        f"🔌 - {'🔋' if CURRENT_STATUS['power'] == 1 else '🪫'}"
    )
    update_pinned_message(full_message)

def main():
    # Start the power monitoring in a separate thread for real-time response
    power_thread = threading.Thread(target=monitor_power)
    power_thread.daemon = True
    power_thread.start()

    # Start the main loop for alerts and AQI
    monitor_alerts_and_aqi()

if __name__ == "__main__":
    main()