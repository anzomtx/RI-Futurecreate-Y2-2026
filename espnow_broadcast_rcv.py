# LISTENER (upload this to all receivers)
import network, espnow, time, ubinascii
e = espnow.ESPNow()
e.active(True)

print("Listening...")
while True:
    host, msg = e.recv()
    if msg:
        mac = ubinascii.hexlify(host, ':').decode().upper()
        print(f"{mac}: {msg.decode()}")