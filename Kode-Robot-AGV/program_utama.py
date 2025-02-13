from LF_PID import line_follower_PID
from ultrasonik import distance
from driver_logic import logika_driver

import time
import pigpio
import RPi.GPIO as GPIO

pi = pigpio.pi()
if not pi.connected:
    exit()

try:
    while True:
        jarak = distance()
        print("Jarak:", jarak)
        
        if jarak <= 10:
            print("Stop")
            # Berhentikan motor (0, 0)
            logika_driver(0, 0)
        else:
            # Jalankan satu iterasi line follower PID
            line_follower_PID()  # Panggil fungsi line_follower_PID untuk satu iterasi
        

except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna")
    GPIO.cleanup()
    logika_driver(0, 0)
    pi.stop()
