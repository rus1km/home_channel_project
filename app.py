import time
from alerts import get_air_raid_alert_status
from weather import get_air_quality_index
from telegram import send_message, update_pinned_message

def main():
    previous_alert_status = None  # Initialize to track alert status changes
    previous_aqi_status = None    # Initialize to track AQI updates

    while True:
        # Fetch air raid alert status and AQI
        current_alert_status = get_air_raid_alert_status(31)
        current_aqi = get_air_quality_index()

        if current_aqi != previous_aqi_status and current_aqi > 3:
            send_message("Якість повітря погіршилась.")
        
        if current_alert_status != previous_alert_status:
            # Send message on status change
            if current_alert_status == "alert":
                send_message("🚨 Оголошено повітряну тривогу!")
            elif current_alert_status == "no_alert":
                send_message("✅ Відбій повітряної тривоги.")

        # Combined message
        full_message = f"📢: {current_alert_status} 💨:{current_aqi}"

        # Update the pinned message only if there's a status change
        if current_alert_status != previous_alert_status or current_aqi != previous_aqi_status:
            update_pinned_message(full_message)
            previous_alert_status = current_alert_status
            previous_aqi_status = current_aqi

        # Wait before checking again
        time.sleep(30)


if __name__ == "__main__":
    main()