from LF_PID2 import start_line_follower, stop_line_follower , pid_control
from ultrasonik import distance, setup_pins
from driver_logic import logika_driver
from empat_ir import logika_empat_ir
from duaRFID import Baca_jenis_barang, Baca_lokasi
from solenoiddor import unlock_solenoid, lock_solenoid
import pandas as pd
from ambil_data import start_ambil_data, stop_ambil_data
from node_red_tes import start_thread, stop_thread_func

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
        time.sleep(1)
        while True:
            try:
                jarak = distance()
                if jarak > 15:
                    print("Halangan hilang, melanjutkan mencari tag...")
                    start_line_follower()
                    break
            except ValueError:
                print("Input tidak valid. Masukkan angka untuk jarak.")

try:
    #start_line_follower()  # Mulai thread PID
    while True:
        try:
            unlock_solenoid()
            jarak = distance()
#             print("Jarak:", jarak)
            time.sleep(0.1)

            if 0 < jarak <= 15:
                handle_obstacle()
            else:
                #start_line_follower()  # Mulai thread PID
                if not sudah_membaca_barang:
                   # print("Robot berjalan mengikuti garis...")
                    start_line_follower()  # Mulai thread PID
                    start_ambil_data()
                    #start_thread()
                    

                    while True:
                        try:
                            baca_empat_IR = logika_empat_ir()
                            #print(f"hasil:  {baca_empat_IR}")
                            time.sleep(0.1)
                            
                            if baca_empat_IR == "11":
                                print("Deteksi 11.")
                            
                                stop_line_follower()  # Hentikan PID kontrol
                                logika_driver(0, 0)  # Hentikan motor
                                time.sleep(0.5 )  # Tambahkan penundaan singkat untuk memastikan motor berhenti
                                
                                lock_solenoid()
                                print("Kunci keranjang")
                                time.sleep(2)  # Menghentikan eksekusi program selama 2 detik
                                
                                print("Baca jenis barang")
                                jenis_barang = Baca_jenis_barang()
                                time.sleep(2) 

                                
                                sudah_membaca_barang = True
                                #start_line_follower()  # Mulai ulang PID kontrol
                                break  # Keluar dari loop membaca 4 IR setelah mendeteksi "0000"
                            else:
                               # print("Masukkan nilai 4 IR lagi...")
                                jarak = distance()
                                #print("Jarak:", jarak)
                                time.sleep(0.1)
                                if 0 < jarak <= 15:
                                    handle_obstacle()
                                    break
                                else:
                                    pass
                                   # print("Jalan lagi")
                                    #start_line_follower() 
                                    
                                    
                        except ValueError:
                            print("Input tidak valid. Masukkan nilai 4 IR.")
                            

                if sudah_membaca_barang:
                    print("Mencari tag yang sesuai...")
                    start_line_follower()  # Mulai ulang PID kontrol
                    while True:
                        
                        jarak = distance()
                        print("Jarak:", jarak)
                        time.sleep(0.1)
                        if 0 < jarak <= 15:
                            handle_obstacle()
                        
                        try:

                            tag_bawah = Baca_lokasi()
                            
                            
                            if jenis_barang == "Barang A" and tag_bawah == "Lokasi A":
                                print("Stop")
                                stop_line_follower()  # Hentikan PID kontrol
                                logika_driver(0, 0)  # Hentikan motor
                                
                                unlock_solenoid()
                                print("Lepas keranjang")
                                time.sleep(5)  # Menghentikan eksekusi program selama 5 detik
                                sudah_membaca_barang = False

                                print("Melanjutkan berjalan sambil membaca 4 IR...")
                                #start_line_follower()  # Mulai ulang PID kontrol
                                break
                            
                            elif jenis_barang == "Barang B" and tag_bawah == "Lokasi B":
                                print("Stop")
                                stop_line_follower()  # Hentikan PID kontrol
                                logika_driver(0, 0)  # Hentikan motor

                                unlock_solenoid()
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
            #stop_ambil_data()
            #stop_thread_func()
            GPIO.cleanup()
            pi.stop()
            break  # keluar dari loop utama untuk menghentikan program
except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna")
    logika_driver(0, 0)
    stop_line_follower()
    stop_ambil_data()
    #stop_thread_func()
#     
#     df = pd.DataFrame(data, columns=['Jarak'])
#     # Menyimpan DataFrame ke file Excel
#     df.to_excel('data_ultrasonik.xlsx', index=False)
#     print("Data telah disimpan ke file data_ultrasonik.xlsx")
    
    GPIO.cleanup()
    pi.stop()
