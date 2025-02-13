import pigpio
import time

# Mendefinisikan pin GPIO untuk relay
relay_pin = 20

# Menghubungkan ke daemon pigpio
pi = pigpio.pi()

# Memastikan pigpio berhasil terhubung
if not pi.connected:
    exit()

# Mengatur relay_pin sebagai output
pi.set_mode(relay_pin, pigpio.OUTPUT)

def unlock_solenoid():
    """Mematikan solenoid (mengunci kembali)"""
    pi.write(relay_pin, 0)
    #print("Lepas")

def lock_solenoid():
    """Mengaktifkan solenoid (membuka kunci)"""
    pi.write(relay_pin, 1)
    #print("Mengunci")

def main():
    try:
        # Pastikan solenoid dalam kondisi lepas saat pertama kali dijalankan
        unlock_solenoid()
        
        while True:
            lock_solenoid()
            # time.sleep(3)  # Solenoid aktif selama 3 detik
            # unlock_solenoid()
            # time.sleep(3)
    except KeyboardInterrupt:
        # Membersihkan pengaturan GPIO sebelum keluar
        pi.stop()

if __name__ == "__main__":
    main()
