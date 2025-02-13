import RPi.GPIO as GPIO
from mfrc522 import MFRC522
import time
import threading

class DualMFRC522:
    def __init__(self):
        self.reader1 = MFRC522(bus=0, device=0)
        self.reader2 = MFRC522(bus=0, device=1)

    def read(self, reader):
        (status, TagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

        if status != reader.MI_OK:
            return None

        (status, uid) = reader.MFRC522_Anticoll()

        if status != reader.MI_OK:
            return None

        card_id = int.from_bytes(bytes(uid), byteorder='big')
        return card_id

def Baca_jenis_barang():
    reader = DualMFRC522()
    jenis_barang = None

    try:
        while not jenis_barang:
            id1 = reader.read(reader.reader1)

            if id1:
                print(f"Reader 1 ID: {id1}")
                if id1 == 907723015181:
                    jenis_barang = "Barang A"
                elif id1 == 426037153686:
                    jenis_barang = "Barang B"
                else:
                    jenis_barang = "Tidak diketahui"
                print(f"Jenis Barang: {jenis_barang}")

            time.sleep(0.1)
    finally:
        GPIO.cleanup()

    return jenis_barang

def Baca_lokasi():
    reader = DualMFRC522()
    lokasi = None
    try:
        while not lokasi:
            id2 = reader.read(reader.reader2)

            if id2:
                print(f"Reader 2 ID: {id2}")
                if id2 == 838310704876:
                    lokasi = "Lokasi A"
                elif id2 == 153515341457:
                    lokasi = "Lokasi B"
                elif id2 == 429347321530:
                    lokasi = "Lokasi Pengambilan Barang"
                else:
                    lokasi = "Tidak diketahui"
                print(f"Lokasi: {lokasi}")

            time.sleep(0.1)
    finally:
        GPIO.cleanup()

    return lokasi


if __name__ == "__main__":
    jenis_barang = Baca_jenis_barang()
    lokasi = Baca_lokasi()
    print(f"Jenis Barang: {jenis_barang}\n Lokasi: {lokasi}")
