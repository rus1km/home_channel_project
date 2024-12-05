# Home Monitoring and Notification System

#### Video Demo: https://youtu.be/6lbNguspIQg

#### Description:

The **Home Monitoring and Notification System** is a real-time monitoring solution designed to enhance safety and awareness for the residents of an apartment complex. It combines three crucial features: monitoring air quality, air raid alerts, and power outages. The system uses a combination of hardware and software, including custom-built devices, Python scripts, APIs, and Docker, to deliver timely notifications to a dedicated Telegram channel. 

### Features:
1. **Air Quality Monitoring**: 
   - Fetches real-time air quality index (AQI) and temperature data from a nearby meteorological station via their API. 
   - If AQI exceeds healthy levels, a notification is sent to the Telegram channel, alerting users of potential health risks.
   - Data updates occur every hour for accuracy.

2. **Air Raid Alert Monitoring**: 
   - Subscribes to a local air raid alert system via API. 
   - The system checks for updates twice per minute and immediately notifies users in case of an air raid alert in Kyiv, ensuring preparedness and safety.

3. **Power Monitoring**:
   - Utilizes a custom-built hardware device comprising an Arduino Nano and a voltage sensor connected to a wall outlet.
   - Tracks power status in real-time and sends notifications about power outages or restorations to the Telegram channel.

---

### Project Structure:

- **`app.py`**: 
  - The main entry point of the application.
  - Manages the overall flow by coordinating air quality, air raid alerts, and power monitoring.
  - Implements multi-threading for handling real-time power monitoring alongside periodic checks for air quality and air raid alerts.

- **`alerts.py`**:
  - Handles integration with the local air raid alert API.
  - Fetches the status of air raid alerts for Kyiv and returns it as a binary value (1 for alert, 0 for no alert).

- **`weather.py`**:
  - Fetches air quality index (AQI) and temperature data from the meteorological station's API.
  - Formats and processes the data, providing both raw values and a color-coded AQI display for easy interpretation.

- **`power.py`**:
  - Manages real-time power monitoring by interfacing with the Arduino device via USB.
  - Detects changes in power status and yields updates as binary values (1 for power on, 0 for power off).

- **`telegram.py`**:
  - Contains helper functions to send messages and update pinned messages in the Telegram channel.
  - Acts as the notification backbone of the system.

- **`arduino`**:
  - Contains the Arduino sketch (code) for the voltage sensor device. This script enables the Arduino to send voltage readings to the server.

- **`requirements.txt`**:
  - Lists all Python dependencies required to run the project, such as `requests`, `dotenv`, and `pyserial`.

- **`.env`**:
  - Stores environment variables such as API keys, Telegram bot token, and other sensitive data. This file is ignored by version control for security.

---

### Design Decisions:

1. **Real-Time Notifications**:
   - The system prioritizes timely updates, leveraging multi-threading to handle air raid alerts and power monitoring simultaneously.

2. **Hardware Integration**:
   - A custom Arduino device was chosen for power monitoring due to its flexibility and cost-effectiveness. 
   - The design ensures the system can detect power status changes almost instantly.

3. **Docker Deployment**:
   - Docker was used to containerize the application for consistent deployment across different environments.
   - This choice simplifies dependencies and ensures smooth operation on the server.

4. **Telegram Integration**:
   - Telegram was chosen as the notification platform because of its ease of use, reliability, and accessibility.

5. **Error Handling**:
   - Robust error handling was implemented to deal with API issues, hardware disconnections, and unexpected inputs. This ensures the system remains functional even in adverse conditions.

---

### Challenges and Solutions:

1. **Cross-Platform USB Device Detection**:
   - Ensuring the Arduino device could be detected on any USB port and operating system was a key challenge. A dynamic port detection mechanism was implemented to address this.

2. **Multi-Threading for Real-Time Updates**:
   - Balancing real-time power monitoring with periodic API checks required careful threading design to avoid resource conflicts.

3. **API Integration**:
   - Differences in API response formats were handled by processing and validating data before use. Error handling ensures the application continues running even if API responses are delayed or invalid.

---

### How to Run the Project:

1. **Set Up Environment**:
   - Clone the repository from GitHub:
     ```bash
     git clone https://github.com/rus1km/home_channel_project.git
     cd home_channel_project
     ```
   - Install dependencies in a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

2. **Add Configuration**:
   - Create a `.env` file in the project directory and add the required API keys and other configurations.

3. **Run the Application**:
   - Directly on the host:
     ```bash
     python app.py
     ```
   - Using Docker:
     ```bash
     docker build -t home_monitoring_system .
     docker run -d --env-file .env --device /dev/ttyUSB0 home_monitoring_system
     ```

---

### Conclusion:

The *Home Monitoring and Notification System* is a comprehensive solution for real-time monitoring and notifications. It integrates multiple functionalities—air quality monitoring, air raid alerts, and power status—into a unified system. Designed to enhance safety and awareness, this project demonstrates the power of integrating hardware and software to solve real-world problems.

Feel free to explore the project on GitHub and reach out with suggestions or feedback!