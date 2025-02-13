from LF_PID import start_line_follower, stop_line_follower
from ultrasonik import distance, setup_pins
from driver_logic import logika_driver
from empat_ir import logika_empat_ir
from duaRFID import Baca_jenis_barang, Baca_lokasi

import time
import pigpio
import RPi.GPIO as GPIO

pi = pigpio.pi()
if not pi.connected:
    exit()

# Set GPIO mode
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

setup_pins()  # Setup pins at the beginning

# Variabel status untuk melacak apakah sudah membaca jenis barang dan mengunci keranjang
sudah_membaca_barang = False

def handle_obstacle():
    print("Stop")
    stop_line_follower()
    logika_driver(0, 0)
    if sudah_membaca_barang:
        print("Menunggu halangan hilang...")
        while True:
            try:
                jarak = distance()
                if jarak > 10:
                    print("Halangan hilang, melanjutkan mencari tag...")
                    start_line_follower()
                    break
            except ValueError:
                print("Input tidak valid. Masukkan angka untuk jarak.")

try:
    #start_line_follower()  # Mulai thread PID
    while True:
        try:
            jarak = distance()
            print("Jarak:", jarak)
            time.sleep(0.1)

            if jarak <= 10:
                handle_obstacle()
            else:
                #start_line_follower()  # Mulai thread PID
                if not sudah_membaca_barang:
                    print("Robot berjalan mengikuti garis...")
                    start_line_follower()  # Mulai thread PID
                    

                    while True:
                        try:
                            baca_empat_IR = logika_empat_ir()
                            print(f"hasil:  {baca_empat_IR}")
                            time.sleep(0.1)
                            
                            if baca_empat_IR == "0000":
                                print("Deteksi 0000.")
                            
                                stop_line_follower()  # Hentikan PID kontrol
                                logika_driver(0, 0)  # Hentikan motor
                                time.sleep(1)  # Tambahkan penundaan singkat untuk memastikan motor berhenti

                                print("Baca jenis barang")
                                jenis_barang = Baca_jenis_barang()

                                print("Kunci keranjang")
                                time.sleep(2)  # Menghentikan eksekusi program selama 2 detik
                                sudah_membaca_barang = True
                                #start_line_follower()  # Mulai ulang PID kontrol
                                break  # Keluar dari loop membaca 4 IR setelah mendeteksi "0000"
                            else:
                                print("Masukkan nilai 4 IR lagi...")
                                jarak = distance()
                                print("Jarak:", jarak)
                                time.sleep(0.1)
                                if jarak <= 10:
                                    handle_obstacle()
                                    break
                                else:
                                    print("Jalan lagi")
                                    #start_line_follower() 
                                    
                                    
                        except ValueError:
                            print("Input tidak valid. Masukkan nilai 4 IR.")

                if sudah_membaca_barang:
                    print("Mencari tag yang sesuai...")
                    start_line_follower()  # Mulai ulang PID kontrol
                    while True:
                        try:
                            tag_bawah = Baca_lokasi()
                            if tag_bawah == "Lokasi A" and jenis_barang =="Barang A":
                                print("Stop")
                                stop_line_follower()  # Hentikan PID kontrol
                                logika_driver(0, 0)  # Hentikan motor

                                print("Lepas keranjang")
                                time.sleep(5)  # Menghentikan eksekusi program selama 5 detik
                                sudah_membaca_barang = False

                                print("Melanjutkan berjalan sambil membaca 4 IR...")
                                #start_line_follower()  # Mulai ulang PID kontrol
                                break
                            elif tag_bawah == "Lokasi B" and jenis_barang =="Barang B":
                                print("Stop")
                                stop_line_follower()  # Hentikan PID kontrol
                                logika_driver(0, 0)  # Hentikan motor
                                print("Lepas keranjang")
                                time.sleep(5)  # Menghentikan eksekusi program selama 5 detik
                                sudah_membaca_barang = False

                                print("Melanjutkan berjalan sambil membaca 4 IR...")
                                #start_line_follower()  # Mulai ulang PID kontrol
                                break
                            else:
                                print("Tag tidak dikenali, lanjutkan memeriksa...")
                        except ValueError:
                            print("Input tidak valid. Masukkan tag yang benar.")
        except ValueError:
            print("Input tidak valid. Masukkan angka untuk jarak.")
            logika_driver(0, 0)
            stop_line_follower()
            GPIO.cleanup()
            pi.stop()
            break  # keluar dari loop utama untuk menghentikan program
except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna")
    logika_driver(0, 0)
    stop_line_follower()
    GPIO.cleanup()
    pi.stop()