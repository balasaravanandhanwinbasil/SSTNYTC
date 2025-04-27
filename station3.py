import pyhula
import time
import cv2
import numpy as np
from hula_video import hula_video
from tflite_detector import tflite_detector
import threading

uapi = pyhula.UserApi()

def detect_blue(frame):
    # Define HSV range for blue color
    Lblue= np.array([0, 100, 100])
    Ublue = np.array([140, 255, 255])
    
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for red color
    mask_blue = cv2.inRange(hsv, Lblue, Ublue)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Draw the detected contour and center
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)  # Green dot at center
        
        return center_x, center_y, frame
    else:
        return None, None, frame

def detect_red(frame):
    # Define HSV range for red color
    Lblue = np.array([100, 150, 70])
    Ublue = np.array([140, 255, 255])
    
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for blue color
    mask_red = cv2.inRange(hsv, Lblue, Ublue)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        center_x = x + w // 2
        center_y = y + h // 2
        
        # Draw the detected contour and center
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)  # Green dot at center
        
        return center_x, center_y, frame
    else:
        return None, None, frame

if not uapi.connect():
    print("no")
else:
    print("yes")

    video = hula_video(hula_api=uapi,display=False)
    video.video_mode_on()

    uapi.single_fly_takeoff()
    
    uapi.single_fly_forward(distance=50)
    uapi.plane_cmd_camera_angle(0,30)

    i = 0
    result = uapi.single_fly_recognition_Qrcode(0,0)
    while i < 10 and result['result'] == False:
        time.sleep(0.1)
        i += 1
        result = uapi.single_fly_recognition_Qrcode(mode = 0, qr_id = 0)

    if result['result'] == True:
        uapi.single_fly_straight_flight(x = result['x'], y = result['y'], z = 0)

    #DETECT BLUE BALL
    for i in range(30):
        center_x, center_y, frame = detect_blue(video.get_video())
        print("DETECTING BLUE BALL...")
        cv2.imshow("Blue Detection", frame)
        cv2.waitKey(1)
        print(center_x, center_y)
        time.sleep(0.5)

    #DETECT RED BALL
    for i in range(30):
        center_x, center_y, frame = detect_red(video.get_video())
        print("DETECTING RED BALL...")
        cv2.imshow("Red Detection", frame)
        cv2.waitKey(1)
        print(center_x, center_y)
        time.sleep(0.5) 

    uapi.single_fly_right(distance=20)
    uapi.single_fly_forward(distance=70)
    uapi.single_fly_down(height = 10)

    for _ in range(5):
        uapi.single_fly_forward(distance = 10)

    uapi.single_fly_back(distance=55)
    uapi.single_fly_left(distance = 55)

    for _ in range(5):
        uapi.single_fly_forward(distance = 10)



        