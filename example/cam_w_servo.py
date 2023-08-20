import cv2
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo, Device
from time import sleep, time

factory = PiGPIOFactory()

servo = Servo(17,min_pulse_width=0.5/1000, max_pulse_width=2.4/1000, pin_factory=factory)

cap = cv2.VideoCapture(0)

t = time()
a = False

servo.value = -0.8
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        if time() - t > 5 and not a:
            a = True
            servo.value = -0.1
            print("Move down")
        
        cv2.imshow("Frame", frame)
    else:
        break

    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == ord('w'):
        a = False
        t = time()
        servo.value = -0.8

cap.release()
cv2.destroyAllWindows()
