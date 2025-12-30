import network
import ubinascii

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
mac = wlan.config('mac')

print("MAC:", ubinascii.hexlify(mac, ':').decode().upper())