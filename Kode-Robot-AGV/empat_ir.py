import pigpio
import time

# Inisialisasi pigpio
pi = pigpio.pi()
if not pi.connected:
    exit()

ir_pins = [22, 23]
# Mengatur pin s  ensor sebagai input
for pin in ir_pins:
    pi.set_mode(pin, pigpio.INPUT)

def logika_empat_ir():
    ir_bits = ""
    global hasil_empat_ir
    for pin in ir_pins:
        if pi.read(pin):
            ir_bits += "0"  # putih
        else:
            ir_bits += "1"  # hitam

    if ir_bits == "11":
        hasil_empat_ir = "11"
    else:
        hasil_empat_ir = "Belum sesuai"
    #print("hasil: ", ir_bits)
    return hasil_empat_ir

# while True:
#     logika_empat_ir()
#     time.sleep(2)