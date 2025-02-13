import pigpio
import time

# Inisialisasi pigpio
pi = pigpio.pi()
if not pi.connected:
    exit()
    
motor_pins_pwm = [18, 19, 12,13] #18, 19 roda kanan dan 12,13 roda kiri
#motor_pins_enable = [20, 21]

for pin_pwm in motor_pins_pwm:
    pi.set_mode(pin_pwm, pigpio.OUTPUT)
    
# for pin_enable in motor_pins_enable:
#     pi.set_mode(pin_enable, pigpio.OUTPUT)

# Enable motor driver
# pi.write(motor_pins_enable[0], 1)
# pi.write(motor_pins_enable[1], 1)

pwm_frekuensi = 1000  # 1 kHz PWM frequency

# Set PWM frequency
for pwm in motor_pins_pwm:
    pi.set_PWM_frequency(pwm, pwm_frekuensi)
    
def logika_driver(kecepatan_kiri, kecepatan_kanan):
    if kecepatan_kiri < 0:
        # Kiri mundur
        if kecepatan_kiri < -255:
            kecepatan_kiri = -255
        pi.set_PWM_dutycycle(motor_pins_pwm[2], 0)
        pi.set_PWM_dutycycle(motor_pins_pwm[3], -kecepatan_kiri)
    else:
        # Kiri maju
        if kecepatan_kiri > 255:
            kecepatan_kiri = 255
        pi.set_PWM_dutycycle(motor_pins_pwm[2], kecepatan_kiri)
        pi.set_PWM_dutycycle(motor_pins_pwm[3], 0)
    
    if kecepatan_kanan < 0:
        # Kanan mundur
        if kecepatan_kanan < -255:
            kecepatan_kanan = -255
        pi.set_PWM_dutycycle(motor_pins_pwm[1], 0)
        pi.set_PWM_dutycycle(motor_pins_pwm[0], -kecepatan_kanan)
    else:
        # Kanan maju
        if kecepatan_kanan > 255:
            kecepatan_kanan = 255
        pi.set_PWM_dutycycle(motor_pins_pwm[1], kecepatan_kanan)
        pi.set_PWM_dutycycle(motor_pins_pwm[0], 0)

