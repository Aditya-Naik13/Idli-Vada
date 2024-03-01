import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
pulse_sensor_pin = 12  # Assuming pulse sensor connected to GPIO pin 12

# Initializing variables
pulse_data = []

# Setup pulse sensor pin as input
GPIO.setup(pulse_sensor_pin, GPIO.IN)

# Function to calculate the heart rate from pulse data
def calculate_heart_rate(pulse_data, sampling_rate=10):
    pulse_count = sum(pulse_data)
    # Convert pulse count to beats per minute (BPM)
    heart_rate = (pulse_count / len(pulse_data)) * 60 / sampling_rate
    return heart_rate

# Main loop for drowsiness detection
while True:
    # Read pulse sensor data
    pulse_value = GPIO.input(pulse_sensor_pin)
    pulse_data.append(pulse_value)

    # Limit pulse data to last 10 seconds
    if len(pulse_data) > 100:  # Assuming sampling rate of 10 Hz
        pulse_data.pop(0)

    # Calculate heart rate
    heart_rate = calculate_heart_rate(pulse_data)

    # Check if heart rate indicates sleeping condition
    if heart_rate < 55:
        # If heart rate is below 55 BPM, person might be sleeping
        status = "SLEEPING!!!"
        color = (255, 0, 0)
    else:
        # Otherwise, person is considered active
        status = "ACTIVE :)"
        color = (0, 255, 0)

    # Display status on frame (you can integrate this with your existing code)
    cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break

# Cleanup GPIO
GPIO.cleanup()
