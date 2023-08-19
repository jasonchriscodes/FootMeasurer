from gpiozero import Servo
from time import sleep 

servo = Servo(17,min_pulse_width=0.5/1000, max_pulse_width=2.4/1000)

try: 
    while True:
        servo.value=-1
        sleep(0.5)
        servo.value=0
        sleep(0.5)
        servo.value=1
        sleep(0.5)
except KeyboardInterrupt:
    print("Program stopped")