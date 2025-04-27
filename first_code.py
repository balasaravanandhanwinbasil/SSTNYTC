import threading
import time
import numpy as np
import signal
import cv2
import sys
import pyhula
import ctypes
from collections import deque
import os
from hula_video import hula_video




def detect_blue(frame):
    # Define HSV range for blue color
    Lblue = np.array([100, 150, 70])
    Ublue = np.array([140, 255, 255])
    
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Create a mask for blue color
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
        cv2.drawContours(frame, [largest_contour], -1, (255, 0, 0), 3)  # Blue color
        cv2.circle(frame, (center_x, center_y), 5, (0, 255, 0), -1)  # Green dot at center
        
        return center_x, center_y, frame
    else:
        return None, None, frame
    


    import pyhula
import time
from hula_video import hula_video
from datetime import datetime, timedelta
import cv2
import numpy as np

uapi = pyhula.UserApi()


if not uapi.connect():
    print('connect error')
else:
    print('success')
    video = hula_video(hula_api=uapi,display=False)
    video.video_mode_on()
    video.startrecording() 
    uapi.single_fly_takeoff()
    time.sleep(2)
    for i in range(100):
        frame = video.get_video()
        cv2.putText(frame, 'GROUP SST', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 50, 0), 2) 
        cv2.imshow("Ball Detection", frame)       
        cv2.waitKey(1)
        time.sleep(0.5)
    cv2.destroyAllWindows()
    video.stoprecording()
    video.close()
    uapi.single_fly_touchdown()

