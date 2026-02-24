# main.py - Weather Display for ESP32 with SH1106 OLED
import network
import urequests
import json
import random
import time
import machine
from machine import Pin, I2C
import sh1106

# Wi-Fi Configuration
WIFI_SSID = "HUAWEI_B311_8F43_Guest"
WIFI_PASSWORD = ""

# API Configuration
API_URL = "https://api.data.gov.sg/v1/environment/2-hour-weather-forecast"

# Initialize I2C and OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)
addr = 0x3C
oled = sh1106.SH1106(128, 64, i2c, addr=addr)

def connect_wifi():
    """Connect to Wi-Fi network"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"Connecting to {WIFI_SSID}...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        # Wait for connection (max 10 seconds)
        for _ in range(50):
            if wlan.isconnected():
                break
            time.sleep(0.2)
    
    if wlan.isconnected():
        print(f"Connected! IP: {wlan.ifconfig()[0]}")
        return True
    else:
        print("Failed to connect to Wi-Fi")
        return False

def fetch_weather_data():
    """Fetch weather data from Singapore Government API"""
    try:
        print("Fetching weather data...")
        response = urequests.get(API_URL)
        
        if response.status_code == 200:
            data = json.loads(response.text)
            response.close()
            return data
        else:
            print(f"API Error: {response.status_code}")
            response.close()
            return None
            
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

def parse_weather_data(json_data):
    """Parse JSON data and extract forecasts"""
    try:
        if json_data and "items" in json_data:
            items = json_data["items"]
            if items and len(items) > 0:
                forecasts = items[0].get("forecasts", [])
                
                # Create a list of location-forecast tuples
                weather_data = []
                for forecast in forecasts:
                    area = forecast.get("area", "Unknown")
                    weather = forecast.get("forecast", "N/A")
                    
                    # Clean up forecast text (remove time indicators)
                    if " (Day)" in weather:
                        weather = weather.replace(" (Day)", "")
                    if " (Night)" in weather:
                        weather = weather.replace(" (Night)", "")
                    
                    weather_data.append((area, weather))
                
                return weather_data
    except Exception as e:
        print(f"Error parsing data: {e}")
    
    return []

def select_random_locations(weather_data, count=2):
    """Select random locations from the weather data"""
    if len(weather_data) < count:
        return weather_data[:] if weather_data else []
    
    # MicroPython doesn't have random.sample, so we implement it manually
    selected = []
    indices = list(range(len(weather_data)))
    
    for i in range(count):
        # Pick a random index from remaining indices
        idx = random.randint(0, len(indices) - 1)
        selected_idx = indices.pop(idx)
        selected.append(weather_data[selected_idx])
    
    return selected

def display_weather(oled, location1, location2):
    print (location1)
    print (location2)

    """Display two locations and their weather on OLED"""
    oled.fill(0)  # Clear display
    
    # Display location 1 (top half)
    loc1_name = location1[0][:16]  # Truncate to 16 chars
    loc1_weather = location1[1][:16]  # Truncate to 16 chars
    
    oled.text(loc1_name, 0, 0)
    oled.text(loc1_weather, 0, 10)
    
    # Display location 2 (bottom half)
    loc2_name = location2[0][:16]  # Truncate to 16 chars
    loc2_weather = location2[1][:16]  # Truncate to 16 chars
    
    oled.text(loc2_name, 0, 35)
    oled.text(loc2_weather, 0, 45)
    
    oled.show()

def display_error(oled, message):
    print (message)

    """Display error message on OLED"""
    oled.fill(0)
    oled.text("ERROR", 40, 0)
    oled.hline(0, 10, 128, 1)
    
    # Split long messages
    if len(message) > 21:
        lines = [message[i:i+21] for i in range(0, len(message), 21)]
        for i, line in enumerate(lines[:3]):  # Max 3 lines
            oled.text(line, 0, 15 + i*10)
    else:
        oled.text(message, 0, 25)
    
    oled.text("Retrying...", 20, 50)
    oled.show()

def display_welcome(oled):
    """Display welcome screen"""

    oled.fill(0)
    oled.text("Singapore", 20, 10)
    oled.text("Weather", 25, 20)
    oled.text("Display", 30, 30)

    oled.show()

def main():
    # Connect to Wi-Fi
    if not connect_wifi():
        display_error(oled, "Wi-Fi Failed")
        time.sleep(5)
        machine.reset()
    
    # Display welcome screen
    display_welcome(oled)
    
    json_data = fetch_weather_data()
    
    if json_data:
        weather_data = parse_weather_data(json_data)
        
        if weather_data:
            # Select two random locations
            selected_locations = select_random_locations(weather_data, 2)
            
            if len(selected_locations) == 2:
                # Display the selected locations
                display_weather(oled, selected_locations[0], selected_locations[1])
                
                # Print to console for debugging
                print(f"\nSelected Locations:")
                print(f"1. {selected_locations[0][0]}: {selected_locations[0][1]}")
                print(f"2. {selected_locations[1][0]}: {selected_locations[1][1]}")
            else:
                display_error(oled, "Insufficient data")
        else:
            display_error(oled, "No weather data")
    else:
        display_error(oled, "Failed to fetch data")


if __name__ == "__main__":
    main()
    
    
    
    