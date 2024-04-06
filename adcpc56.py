import smbus
import time

# Define PCF8591 address and channels
PCF8591_I2C_ADDR = 0x48
ADC_CHANNEL = 0  # Adjust this based on your setup

# Initialize I2C bus
bus = smbus.SMBus(1)

def read_adc(channel):
    """Read data from ADC"""
    bus.write_byte(PCF8591_I2C_ADDR, channel)
    bus.read_byte(PCF8591_I2C_ADDR)  # Dummy read to update ADC
    return bus.read_byte(PCF8591_I2C_ADDR)

try:
    while True:
        # Read analog data from the specified channel
        analog_value = read_adc(ADC_CHANNEL)

        # Convert analog data to meaningful value (e.g., heart rate)
        # You may need to calibrate this conversion based on your heart rate module's specifications

        print("Analog Value:", analog_value)
        time.sleep(1)  # Wait for a second before reading again

except KeyboardInterrupt:
    print("Program terminated")
