import threading
import time
import pigpio
import RPi.GPIO as GPIO
from LF_PID2 import start_line_follower, stop_line_follower
from LF_PID_slow import start_line_follower_slow, stop_line_follower_slow
from sensor_logic2 import logika_sensor_biner
from ultrasonik import distance, setup_pins
from driver_logic import logika_driver
from empat_ir import logika_empat_ir
from duaRFID import Baca_jenis_barang, Baca_lokasi
from solenoiddor import unlock_solenoid, lock_solenoid
from ambil_data import start_ambil_data, stop_ambil_data

pi = pigpio.pi()
if not pi.connected:
    exit()

# Set GPIO mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

setup_pins()  # Setup pins at the beginning

# Variabel status untuk melacak apakah sudah membaca jenis barang dan mengunci keranjang
sudah_membaca_barang = False
jenis_barang = None
program_running = True  # Flag untuk mengendalikan loop utama

def obstacle_thread():
    global program_running
    while program_running:
        try:
            jarak = distance()
            if 0 < jarak <= 10:
                print("Halangan terdeteksi, robot berhenti...")
                stop_line_follower()
                logika_driver(0, 0)
                
                while distance() <= 10:
                    print("Menunggu halangan hilang...")
                    time.sleep(1)
                
                print("Halangan hilang, melanjutkan operasi...")
                start_line_follower()
            time.sleep(0.1)
        except ValueError:
            print("Input tidak valid. Masukkan angka untuk jarak.")

def rfid_thread():
    global sudah_membaca_barang, jenis_barang, program_running
    unlock_solenoid()
    while program_running:
        if not sudah_membaca_barang:
            start_line_follower()  # Mulai thread PID
            start_ambil_data()
            while program_running:
                try:

                    if logika_sensor_biner() == "11111":
                        time.sleep(0.5)
                        stop_line_follower()
                        logika_driver(0, 0)
                        time.sleep(1)
                        start_line_follower_slow()

                    baca_empat_IR = logika_empat_ir()
                    if baca_empat_IR == "11":
                        stop_line_follower_slow()  # Hentikan PID kontrol
                        logika_driver(0, 0)  # Hentikan motor
                        time.sleep(1)  # Tambahkan penundaan singkat untuk memastikan motor berhenti
                        
                        lock_solenoid()
                        print("Kunci keranjang")
                        time.sleep(1)  # Menghentikan eksekusi program selama 2 detik
                        
                        print("Baca jenis barang")
                        jenis_barang = Baca_jenis_barang()
                        time.sleep(1)

                        sudah_membaca_barang = True
                        break  # Keluar dari loop membaca 4 IR setelah mendeteksi "11"
                except ValueError:
                    print("Input tidak valid. Masukkan nilai 4 IR.")
        else:
            print("Mencari tag yang sesuai...")
            start_line_follower()  # Mulai ulang PID kontrol
            while program_running:
                try:
                    tag_bawah = Baca_lokasi()
                    if (jenis_barang == "Barang A" and tag_bawah == "Lokasi A") or (jenis_barang == "Barang B" and tag_bawah == "Lokasi B"):
                        stop_line_follower()  # Hentikan PID kontrol
                        logika_driver(0, 0)  # Hentikan motor
                        time.sleep(1)
                        unlock_solenoid()
                        print("Lepas keranjang")
                        time.sleep(5)  # Menghentikan eksekusi program selama 5 detik
                        sudah_membaca_barang = False
                        break
                    else:
                        print("Tag tidak dikenali, lanjutkan memeriksa...")
                except ValueError:
                    print("Input tidak valid. Masukkan tag yang benar.")

try:
    # Buat thread untuk obstacle dan RFID
    thread_ultrasonik = threading.Thread(target=obstacle_thread)
    thread_rfid = threading.Thread(target=rfid_thread)

    # Mulai thread
    thread_ultrasonik.start()
    thread_rfid.start()

    # Tunggu thread selesai (hingga program dihentikan)
    thread_ultrasonik.join()
    thread_rfid.join()

except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna")
    program_running = False  # Set flag untuk menghentikan loop di dalam thread
    logika_driver(0, 0)
    stop_line_follower()
    stop_line_follower_slow()
    stop_ambil_data()
    GPIO.cleanup()
    pi.stop()
