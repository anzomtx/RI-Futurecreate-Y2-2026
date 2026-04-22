# BROADCASTER (upload this to sender)
import network, espnow, time
e = espnow.ESPNow()
e.active(True)
broadcast = b'\xff\xff\xff\xff\xff\xff'
e.add_peer(broadcast)

n = 1
while True:
    e.send(broadcast, str(n))
    print("Sent:", n)
    n += 1
    time.sleep(5)