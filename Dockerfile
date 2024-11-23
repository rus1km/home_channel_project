# Use an official Python runtime as the base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Add permissions for the serial device (optional, see step 3 for full access)
RUN apt-get update && apt-get install -y minicom

# Command to run the application
CMD ["python", "app.py"]