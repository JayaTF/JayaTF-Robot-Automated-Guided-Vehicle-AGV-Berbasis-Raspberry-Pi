import time
from driver_logic import logika_driver
from sensor_logic import logika_sensor
import threading
#import pandas as pd

# Inisialisasi variabel global
previous_error = 0
I_control = 0
base_speed = 40
max_speed_kiri = 255
max_speed_kanan = 255
kp = 2.000
ki = 0.000
kd = 4.000
setpoint = 0
running = False
pid_thread = None


def pid_control():
    global previous_error, I_control, filtered_error, running
    while running:
        # Lakukan pembacaan sensor
        sensor_value = logika_sensor()

        # Hitung nilai error
        error = setpoint - sensor_value

    # Hitung kontrol PID berdasarkan nilai error
        P_control = kp * error
        I_control += ki * error
        D_control = kd * (error - previous_error)
        PID_control = P_control + I_control + D_control

        # Hitung kecepatan kiri dan kanan
        speed_kiri = base_speed + PID_control
        speed_kanan = base_speed - PID_control

        # Batasi kecepatan maksimum dan minimum
        speed_kiri = max(0, min(speed_kiri, max_speed_kiri))
        speed_kanan = max(0, min(speed_kanan, max_speed_kanan))

        # Kirim nilai ke logika driver
        logika_driver(speed_kiri, speed_kanan)

        # Update previous_error untuk iterasi berikutnya
        previous_error = error

        time.sleep(0.01)  # Delay kecil untuk memberikan waktu CPU untuk tugas lain
        

def start_line_follower():
    global running, pid_thread
    running = True
    pid_thread = threading.Thread(target=pid_control)
    pid_thread.start()

def stop_line_follower():
    global running, pid_thread
    running = False
    P_control = 0
    I_control = 0
    D_control = 0
    PID = 0
    logika_driver(0, 0)
    if pid_thread:
        pid_thread.join()

                
