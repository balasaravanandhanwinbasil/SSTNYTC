import pyhula
import time
from hula_video import hula_video
from tflite_detector import tflite_detector
import cv2
import numpy as np

uapi = pyhula.UserApi()

if not uapi.connect():
    print('connect error')
else:
    print('success')
    video = hula_video(hula_api=uapi,display=False)
    detector = tflite_detector(model="model5.tflite",label="label.txt")
    video.video_mode_on()
    time.sleep(3)
    uapi.single_fly_takeoff()
    time.sleep(2)
    for i in range(50):
        frame = video.get_video()
        object_found, frame = detector.detect(frame)
        if not object_found is None:
            print(F"Found object: {object_found}")           
            if object_found['x'] > 640:
                uapi.single_fly_right(20)
            else:
                if object_found['x'] < 640:
                    uapi.single_fly_left(20)
            if object_found['y'] > 360:
                uapi.single_fly_back(20)
            else:
                if object_found['y'] < 360:
                    uapi.single_fly_forward(20)
            cv2.imshow("Detection", frame)
            cv2.waitKey(1)
            break
        time.sleep(0.1)
    cv2.destroyAllWindows()
    video.close()
    uapi.single_fly_touchdown()