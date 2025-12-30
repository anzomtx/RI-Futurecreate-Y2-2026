
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
API_URL = "https://uselessfacts.jsph.pl/api/v2/facts/random"

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

def fetch_data():
    """Fetch weather data from Singapore Government API"""
    try:
        print("Fetching data...")
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

def parse_fact_data(json_data):
    """Parse JSON data and extract the fact text"""
    try:
        # Check if we have valid JSON data with a 'text' field
        if json_data and "text" in json_data:
            fact_text = json_data.get("text", "No fact found")
            
            # Return as a list with one tuple to match the expected format
            return [("Random Fact", fact_text)]
        else:
            print("No fact found")
            return []
            
    except Exception as e:
        print(f"Error parsing data: {e}")
        return []

def wrap_text(text, max_chars=16):
    """Split text into lines that fit the OLED display (16 chars per line)"""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        # Check if adding this word would exceed the line length
        if len(' '.join(current_line + [word])) <= max_chars:
            current_line.append(word)
        else:
            # Save current line and start a new one
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def display_fact(oled, fact_tuple):
    print(fact_tuple)
    """Display a fact on the OLED with proper wrapping"""
    # Extract the label and fact text from the tuple
    label, fact_text = fact_tuple
    
    oled.fill(0)  # Clear display
    
    # Display the label
    oled.text("Random Fact:", 0, 0)
    
    # Wrap the fact text into lines of ~16 characters
    wrapped_lines = wrap_text(fact_text, 16)
    
    # Display up to 7 lines (OLED has 8 rows total, first row is for label)
    max_lines = min(len(wrapped_lines), 7)
    for i in range(max_lines):
        # Start at y=10 (row 1) and increment by 8 pixels per line
        oled.text(wrapped_lines[i], 0, 10 + i*8)
    
    # If text is too long, add "..." indicator
    if len(wrapped_lines) > 7:
        oled.text("...", 110, 58)
    
    oled.show()

def display_fact_pages(oled, fact_tuple, page_duration=4):
    print(fact_tuple)
    
    """Display long facts across multiple pages"""
    label, fact_text = fact_tuple
    wrapped_lines = wrap_text(fact_text, 16)
    
    # Show 7 lines per page (1 for label + 6 for content)
    lines_per_page = 6
    total_pages = (len(wrapped_lines) + lines_per_page - 1) // lines_per_page
    
    for page in range(total_pages):
        oled.fill(0)
        oled.text(f"Fact {page+1}/{total_pages}", 0, 0)
        
        start_line = page * lines_per_page
        end_line = min(start_line + lines_per_page, len(wrapped_lines))
        
        for i in range(start_line, end_line):
            line_y = 10 + (i - start_line) * 8
            oled.text(wrapped_lines[i], 0, line_y)
        
        oled.show()
        time.sleep(page_duration)  # Wait before showing next page
        
def display_error(oled, message):
    print (message)
    #return

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


def main():
    # Connect to Wi-Fi
    if not connect_wifi():
        display_error(oled, "Wi-Fi Failed")
        time.sleep(5)
        machine.reset()
    
     # Main loop
    last_update = 0
    update_interval = 30  # 5 minutes in seconds
    
    while True:
        current_time = time.time()
        
        if current_time - last_update >= update_interval:
            json_data = fetch_data()
            
            if json_data:
                data = parse_fact_data(json_data)
                
                if data:
                    #display_fact(oled, data[0])
                    display_fact_pages(oled, data[0])
                else:
                    display_error(oled, "Insufficient data")
            else:
                display_error(oled, "Failed to fetch data")

        time.sleep(1)

if __name__ == "__main__":
    main()
    
    
    
    
