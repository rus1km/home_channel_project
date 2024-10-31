import time
from alerts import get_air_raid_alert_status
from weather import get_air_quality_index
from telegram import send_message

def main():
    previous_alert_status = None  # Initialize to track alert status changes
    previous_aqi_status = None    # Initialize to track AQI updates

    while True:
        # Fetch current alert status
        current_alert_status = get_air_raid_alert_status()
        
        # Check if the status has changed
        if current_alert_status != previous_alert_status:
            # Send message on status change
            if current_alert_status == "alert":
                send_message("🚨 Оголошено тривогу в м. Києві!")
            elif current_alert_status == "no_alert":
                send_message("✅ Відбій повітряної тривоги.")
            
            # Update previous status
            previous_alert_status = current_alert_status

        # Check air quality index every 30 seconds
        current_aqi = get_air_quality_index()
        if current_aqi != previous_aqi_status:
            if current_aqi is not None:
                send_message(f"🌍 Поточний індекс якості повітря: {current_aqi}")
            previous_aqi_status = current_aqi

        # Wait before the next check
        time.sleep(30)


if __name__ == "__main__":
    main()