# Import dependencies
import cv2
import numpy as np
from measure import FootSizeMeasurer
from gender_recognizer import GenderRecognizer
import threading
from time import sleep, time, time_ns
import queue
from constant import * 
import cv2
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Servo

factory = PiGPIOFactory()

servo = Servo(17,min_pulse_width=0.5/1000, max_pulse_width=2.4/1000, pin_factory=factory)

MODE_GENDER_RECOGNITION = 0
MODE_FOOT_MEAUSUREMENT = 1
MODE_IDLE = 2

mode = MODE_GENDER_RECOGNITION

# Initialization
measurer = FootSizeMeasurer(
    paper_hsv_min = (0, 0, 200), 
    paper_hsv_max = (180, 255, 255)
)

face1 = "assets/models/opencv_face_detector.pbtxt"
face2 = "assets/models/opencv_face_detector_uint8.pb"
gen1 = "assets/models/gender_deploy.prototxt"
gen2 = "assets/models/gender_net.caffemodel"

recognizer = GenderRecognizer(
    face1 = face1,
    face2 = face2,
    gender1 = gen1,
    gender2 = gen2
)

frame_buffer = queue.Queue()
display_buffer = queue.Queue()

stop_all = False
next = False
is_loading = False

def read_frame():
    global next, stop_all
    print("[INFO]\tRead frame started.")
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame_buffer.put(frame)
            sleep(1/30)
        else:
            break

        if next or stop_all:
            break

    cap.release()
    print("[INFO]\tRead frame finished.")

def measure_foot_size(gender_int):
    global is_loading
    print("[INFO]\tMeasure foot size started.")

    # Move camera down
    servo.value = -0.1

    sleep(5)

    is_loading = False

    with display_buffer.mutex:
        display_buffer.queue.clear()

    sleep(0.1)

    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, image = cap.read()
        if ret:
            image = cv2.rotate(image, cv2.ROTATE_180)
            # Measure foot size
            is_valid, image_result = measurer.get_foot_size(image, gender_int)

            display_buffer.put(image_result)

            if is_valid: break

    cap.release()
    
    print("[INFO]\tMeasure foot size finished.")

def show_progress_bar(frame):
    global is_loading, stop_all
    h, w, _ = frame.shape

    cap = cv2.VideoCapture('assets/loading.gif')

    while is_loading:
        ret, img = cap.read()
        if ret:
            img_h, img_w, _ = img.shape

            x = int((w - img_w)/2)
            y = int((h - img_h)/2)

            frame [y:y+img_h, x:x+img_w:] = img[:,:,:]

            frame = cv2.putText(frame, 
                            f'Loading', 
                            (int(w/2) - 60, int(h/2) - 110), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            1, (255, 255, 255), 2, cv2.LINE_AA)
            
            display_buffer.put(frame)
            sleep(0.02)

        else:
            cap = cv2.VideoCapture('assets/loading.gif')
        if stop_all:
            break
    
    cap.release()

def recognize_gender():
    global next, is_loading, stop_all
    print("[INFO]\tRecognize gender started.")

    count = 0
    while True:
        if not frame_buffer.empty():
            frame = frame_buffer.get()
            #display_buffer.put(frame)
            is_valid, out_frame, gender_int = recognizer.predict(frame)
            display_buffer.put(out_frame)

            count += 1
            print(f"Frame processed: {count}")
            
            if is_valid and count > 10:
                thread = threading.Thread(target = measure_foot_size, args=(gender_int,))
                thread.start()
                next = True

        if next:
            progress_thread = threading.Thread(target = show_progress_bar, args=(frame,))
            progress_thread.start()
            is_loading = True
            break
        
        if stop_all:
            break

    print("[INFO]\tRecognize gender finished.")

def display():
    global stop_all, is_loading
    while True:
        if not display_buffer.empty():
            frame = display_buffer.get()

            h, w, _ = frame.shape 

            ratio = 620 / h

            frame = cv2.resize(frame, (int(w * ratio), int(h * ratio)))
            cv2.imshow("Frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_all = True
            break

read_frame_thread = threading.Thread(target=read_frame)
recognize_gender_thread = threading.Thread(target=recognize_gender)
read_frame_thread.start()
recognize_gender_thread.start()

servo.value = -0.8
display()

# cap = cv2.VideoCapture("assets/videos/video6.mov")
# while cap.isOpened():
#     start_time = time_ns()

#     ret, frame = cap.read()
#     if ret:

#         if mode == MODE_GENDER_RECOGNITION:
#             is_valid, frame, gender_int = recognizer.predict(frame)
#             #if is_valid:
#                 #mode = MODE_IDLE
#                 # TODO: Move camera down
#                 # TODO: When camera has already at desired position, change current mode to foot measurement
#             #    pass
#             cv2.imshow("Frame", frame)

#         elif mode == MODE_FOOT_MEAUSUREMENT:
#             # TODO: Capture image
#             # TODO: Measure foot size
#             pass
#         elif mode == MODE_IDLE:
#             cv2.imshow("Frame", frame)
#     else:
#         break

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     end_time = time_ns()

#     execution_time_ms = (end_time - start_time) / 1000000
#     print(f"Execution Time: {execution_time_ms} ms")

# cap.release()
# cv2.destroyAllWindows()

