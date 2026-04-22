
import network
import espnow
import time
import ubinascii

# CONFIG: Other device's MAC
OTHER = "64:E8:33:83:BE:3C"  # <-- CHANGE THIS

# Setup
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.disconnect()

# ESP-NOW
e = espnow.ESPNow()
e.active(True)
peer = ubinascii.unhexlify(OTHER.replace(':', ''))
e.add_peer(peer)

number = 0  # Current number

print("Ready! My MAC:", ubinascii.hexlify(wlan.config('mac'), ':').decode().upper())

while True:
    # Check for incoming
    try:
        host, msg = e.recv(0)
        if msg:
            number = int(msg.decode()) + 1
            print("Got", msg.decode(), "-> Sending", number)
            e.send(peer, str(number))
    except:
        pass
    
    # If number is 0, start the game
    if number == 0:
        number = 1
        print("Starting with", number)
        e.send(peer, str(number))
    
    time.sleep(5)  # 5 second intervals
    
    
    
    