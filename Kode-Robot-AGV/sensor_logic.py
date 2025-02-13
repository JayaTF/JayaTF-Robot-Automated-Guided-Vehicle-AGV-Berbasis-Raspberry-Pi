import pigpio
import time

#inisialisasi pigpio
pi = pigpio.pi()
if not pi.connected:
    exit()

sensor_pins = [2, 3, 4, 14, 15]
#mengatur pin sensor sebagai output
for pin in sensor_pins:
    pi.set_mode(pin, pigpio.INPUT)
    
def logika_sensor():
    sensor_bits = ""
    global NilaiPosisi
    for pin in sensor_pins:
        if pi.read(pin):
            sensor_bits += "0"  # putih
        else:
            sensor_bits += "1"  # hitam
            
            
    if sensor_bits == "11100":
        NilaiPosisi = 25
    elif sensor_bits == "10000":
        NilaiPosisi = 20
    elif sensor_bits == "11000":
        NilaiPosisi = 15
    elif sensor_bits == "01000":
        NilaiPosisi = 10
    elif sensor_bits == "01100":
        NilaiPosisi = 5
    elif sensor_bits == "00100":  # setpoint
        NilaiPosisi = 0
    elif sensor_bits == "00110":
        NilaiPosisi = -5
    elif sensor_bits == "00010":
        NilaiPosisi = -10
    elif sensor_bits == "00011":
        NilaiPosisi = -15
    elif sensor_bits == "00001":
        NilaiPosisi = -20
    elif sensor_bits == "00111":
        NilaiPosisi = -25
    elif sensor_bits == "11111" or sensor_bits == "00000":
        NilaiPosisi = NilaiPosisi  # No change in error
    else:
        NilaiPosisi = NilaiPosisi  # No change in error for any other case
    #print(error)
    return NilaiPosisi


       




