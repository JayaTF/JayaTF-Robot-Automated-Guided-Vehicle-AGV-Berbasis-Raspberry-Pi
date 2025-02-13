import time
from driver_logic import logika_driver
from sensor_logic2 import logika_sensor
import threading

# Inisialisasi variabel global
previous_error = 0
I_control = 0
base_speed = 20
max_speed_kiri = 255
max_speed_kanan = 255
kp = 1.000
ki = 0.000
kd = 4.000
setpoint = 0
running = False
pid_thread = None

def pid_control_slow():
    global previous_error, I_control, running
    while running:
        sensor_value = logika_sensor()
        error = setpoint - sensor_value

        P_control = kp * error
        I_control += ki * error
        D_control = kd * (error - previous_error)
        PID_control = P_control + I_control + D_control

        speed_kiri = base_speed + PID_control
        speed_kanan = base_speed - PID_control

        speed_kiri = max(0, min(speed_kiri, max_speed_kiri))
        speed_kanan = max(0, min(speed_kanan, max_speed_kanan))

        logika_driver(speed_kiri, speed_kanan)

        previous_error = error

        time.sleep(0.01)

def start_line_follower_slow():
    global running, pid_thread
    if not running:
        running = True
        pid_thread = threading.Thread(target=pid_control_slow)
        pid_thread.start()

def stop_line_follower_slow():
    global running, pid_thread
    if running:
        running = False
        if pid_thread:
            pid_thread.join()
        logika_driver(0, 0)