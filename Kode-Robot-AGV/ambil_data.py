import time
from sensor_logic import logika_sensor
import threading
running = False

def ambil_data():
    while running:
        data_sensor = logika_sensor()
        print(data_sensor)
        time.sleep(0.5)  # Delay kecil untuk memberikan waktu CPU untuk tugas lain
        

def start_ambil_data():
    global running, ambil_data_thread
    running = True
    ambil_data_thread = threading.Thread(target=ambil_data)
    ambil_data_thread.start()

def stop_ambil_data():
    global running, ambil_data_thread
    running = False
    if ambil_data_thread:
        ambil_data_thread.join()

                

