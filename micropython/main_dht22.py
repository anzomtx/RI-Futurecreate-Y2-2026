
import machine
import time
import dht

DHT22_PIN = 23 # The ESP32 pin GPIO21 connected to the DHT22 sensor

# Initialize the DHT22 sensor
DHT22 = dht.DHT22(machine.Pin(DHT22_PIN))

# Read data from the sensor every 2 seconds
while True:
    try:
        DHT22.measure()
        temp = DHT22.temperature()  # Gets the temperature in Celsius
        humidity = DHT22.humidity()  # Gets the relative humidity in %
        print("Temperature: {:.2f}°C, Humidity: {:.2f}%".format(temp, humidity))
    except OSError as e:
        print("Failed to read from DHT22 sensor:", e)

    time.sleep(2)
