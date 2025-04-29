#imports
import pyhula
import time
from hula_video import hula_video
from tflite_detector import tflite_detector
import cv2
import numpy as np
import threading


uapi = pyhula.UserApi()

rotating = 0


def rotate_half():
    #semicircle
    while rotating:
        uapi.single_fly_radius_around(radius=40)

def qrCodeAlign():
    i = 0
    result = uapi.single_fly_recognition_Qrcode(0,0)
    while i < 10 and result['result'] == False:
        time.sleep(0.1)
        i += 1
        result = uapi.single_fly_recognition_Qrcode(mode = 0, qr_id = 0)

    if result['result'] == True:
        uapi.single_fly_straight_flight(x = result['x'], y = result['y'], z = 0)

if not uapi.connect():
    #check if connected, or reconnect if this message pops up
    print('connect error')
else:
    print("connected")

    #begin stream
    video = hula_video(hula_api=uapi,display=False)
    detector = tflite_detector(model="model3.tflite",label="label.txt")
    video.video_mode_on()
    
    #take off
    uapi.single_fly_takeoff()
    #make the camera face forward
    uapi.Plane_cmd_camera_angle(0,0)

    qrCodeAlign()
 
    # go back down a bit after takeoff
    uapi.single_fly_down(height=50)

    #2 circles and 1 semicircle
    uapi.single_fly_forward(distance=45)
    start_timer = time.time()
    uapi.single_fly_radius_around(radius=50)
    end_timer = time.time() #1
    looptime = end_timer - start_timer
    halflooptime = 0.5 * looptime
    uapi.single_fly_radius_around(radius=50)

    rotating = True
    half_thread = threading.Thread(target = rotate_half)
    half_thread.start()
    print(halflooptime)
    time.sleep(halflooptime)
    rotating = False

    #align to QR code
    qrCodeAlign()

    #try to detect google logo
    for i in range(13):
        frame = video.get_video()
        object_found, frame = detector.detect(frame)
        if not object_found is None:
            print(F"Found object: {object_found}")
            uapi.single_fly_lamplight(134,40,158,2,1)
            needgodown = False
        cv2.imshow("Detection", frame)
        cv2.waitKey(1)
        time.sleep(0.2)
        uapi.single_fly_up(height=10)
    cv2.destroyAllWindows()
    video.close()
    
    #prepare to land
    uapi.single_fly_back(distance=10)
    uapi.single_fly_up(height = 110) 
    uapi.single_fly_forward(distance=25) 
    uapi.Plane_cmd_camera_angle(2,90)

    #land
    i = 0
    result = uapi.single_fly_recognition_Qrcode(0,0)
    while i < 10 and result['result'] == False:
        time.sleep(0.1)
        i += 1
        result = uapi.single_fly_recognition_Qrcode(mode = 0, qr_id = 0)

    if result['result'] == True:
        uapi.single_fly_straight_flight(x = result['x'], y = result['y'], z = 0)
        uapi.single_fly_touchdown(led = {'r':255,'g':0,'b':0,'mode':1})
    else:
        uapi.single_fly_touchdown()  
