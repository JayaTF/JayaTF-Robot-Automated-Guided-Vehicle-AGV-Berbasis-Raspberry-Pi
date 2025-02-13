import paho.mqtt.client as mqtt
import threading
import time
import RPi.GPIO as GPIO

from ultrasonik import distance
from empat_ir import logika_empat_ir
from baca_lokasi import Baca_jenis_barang, Baca_lokasi
from sensor_logic import logika_sensor

# Variabel global untuk menghentikan thread
stop_thread = False

# Fungsi untuk mengirim data ke MQTT
def publish_data():
    client = mqtt.Client(protocol=mqtt.MQTTv311)  # Menggunakan versi protokol terbaru
    
    # Callback untuk koneksi
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

    client.on_connect = on_connect

    client.connect("broker.emqx.io", 1883, 60)
    client.loop_start()  # Memulai loop jaringan MQTT

    global stop_thread
    while not stop_thread:
        
        ultrasonik_data = distance()
        ir_atasrobot = logika_empat_ir()
#         barang = Baca_jenis_barang()
#         lokasi = Baca_lokasi()
        posisi = logika_sensor()
        
        
        client.publish("sensor/rfid/jaya/ultrasonik", ultrasonik_data)
        client.publish("sensor/rfid/jaya/empatir", ir_atasrobot)
#         client.publish("sensor/rfid/jaya/barang", barang)
#         client.publish("sensor/rfid/jaya/lokasi", lokasi)
        client.publish("sensor/rfid/jaya/posisi", posisi)
        
        time.sleep(0.5)
    
    client.loop_stop()  # Menghentikan loop jaringan MQTT setelah loop utama selesai

# Jalankan fungsi publish_data dalam thread terpisah
def start_thread():
    publish_thread = threading.Thread(target=publish_data)
    publish_thread.start()
    return publish_thread

# Fungsi untuk menghentikan thread
def stop_thread_func():
    global stop_thread
    stop_thread = True

if __name__ == "__main__":
    thread = start_thread()
    
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        stop_thread_func()
        thread.join()
        print("Thread stopped and program terminated.")
        GPIO.cleanup()

