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
    detector = tflite_detector(model="model3.tflite",label="label.txt")
    video.video_mode_on()
    video.startrecording()
    time.sleep(3)
    uapi.single_fly_takeoff()
    time.sleep(2)
    for i in range(50):
        frame = video.get_video()
        object_found, frame = detector.detect(frame)
        if not object_found is None:
            print(F"Found object: {object_found}")
        cv2.imshow("Detection", frame)
        cv2.waitKey(1)
        time.sleep(0.1)
    cv2.destroyAllWindows()
    video.close()
    video.stoprecording()
    uapi.single_fly_touchdown()
