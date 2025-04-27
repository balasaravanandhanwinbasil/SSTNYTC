import pyhula
import time
from hula_video import hula_video
from datetime import datetime, timedelta
import cv2
import numpy as np
from amplified import detect_blue

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
    for i in range(50):
        center_x, center_y, frame = detect_blue(video.get_video())
        cv2.imshow("Ball Detection", frame)   
        cv2.waitKey(1)
        time.sleep(0.5)
    cv2.destroyAllWindows()
    video.stoprecording()
    video.close()
    uapi.single_fly_touchdown()
