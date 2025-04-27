import pyhula
import time
from hula_video import hula_video
from tflite_detector import tflite_detector
import cv2
import numpy as np

uapi = pyhula.UserApi()

def detect_blue(frame):
    # Define HSV range for blue color
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
    print('connect error')
else:
    print('success')
    video = hula_video(hula_api=uapi,display=False)
    video.video_mode_on()
    video.startrecording()
    time.sleep(3)
    uapi.single_fly_takeoff()
    time.sleep(2)
    for i in range(50):
        frame = video.get_video()
        center_x, center_y, frame = detect_blue(frame)
        print(center_x,center_y)
        if not center_x == None:
            while 50 < center_x and center_x > 10 and 50 < center_y and center_y < 10 :        
                if center_x > 640:
                    uapi.single_fly_right(20)
                else:
                    if center_x < 640:
                        uapi.single_fly_left(20)
                if center_y > 360:
                    uapi.single_fly_back(20)
                else:
                    if center_y < 360:
                        uapi.single_fly_forward(20)
                cv2.imshow("Detection", frame)
                cv2.waitKey(1)
                print(center_x, center_y)
                time.sleep(0.1)
        time.sleep(0.1)
    uapi.single_fly_forward(50)
    cv2.destroyAllWindows()
    video.stoprecording()
    video.close()
    uapi.single_fly_touchdown()