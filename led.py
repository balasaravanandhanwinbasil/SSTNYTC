import pyhula
import time

uapi = pyhula.UserApi()

if not uapi.connect():
    print("Connection error")
else:
    print('Connection to station by WiFi')
    uapi.single_fly_takeoff()
    time.sleep(1)
    uapi.single_fly_touchdown()
