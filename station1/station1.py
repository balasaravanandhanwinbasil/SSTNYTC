import pyhula
import time
import cv2
import numpy as np
from hula_video import hula_video
from tflite_detector import tflite_detector
import threading

uapi = pyhula.UserApi()

stop_thread = False
def blockheight():
    global groundheight
    global stop_thread

    while not stop_thread:
        blockheight = groundheight - uapi.get_plane_distance()
        print(f"""
              Height of object: {blockheight}
              Height of Object from drone: {uapi.get_plane_distance()}
        """)
        time.sleep(0.01)

def detect_blue(frame):
    # Define HSV range for blue color
    frame = video.get_video()
    Lblue= np.array([30, 255, 100])
    Ublue = np.array([30, 116, 255])
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
def bluealign():
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
                print("bluealigned!")
                time.sleep(0.1)
        time.sleep(0.1)
        uapi.single_fly_forward(50)
        cv2.destroyAllWindows()
        video.stoprecording()
        video.close()


def detect_red(frame):
    # Define HSV range for red color
    frame = video.get_video()
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



def redalign():
       for i in range(50):
        frame = video.get_video()
        center_x, center_y, frame = detect_red(frame)
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
                print("redaligned!")
                time.sleep(0.1)
        time.sleep(0.1)
        uapi.single_fly_forward(50)
        cv2.destroyAllWindows()
        video.stoprecording()
        video.close()

    

if not uapi.connect():
    print('connect error')
else:
    print("connected")

    uapi.Plane_cmd_camera_angle(2,90)
    video = hula_video(hula_api=uapi,display=False)
    detector = tflite_detector(model="model3.tflite",label="label.txt")
    video.video_mode_on()

    uapi.single_fly_takeoff()
    i = 0
    result = uapi.single_fly_recognition_Qrcode(1,90)
    while i < 10 and result['result'] == False:
        time.sleep(0.1)
        i += 1
        result = uapi.single_fly_recognition_Qrcode(mode = 0, qr_id = 0)

    if result['result'] == True:
        uapi.single_fly_straight_flight(x = result['x'], y = result['y'], z = 0)

    #move forward and measure height of first box
    groundheight = uapi.get_plane_distance()
    frame = video.get_video()
    

    uapi.Plane_cmd_camera_angle(2,90)
    uapi.single_fly_forward(distance=90) #adjust
    detect_blue(frame)
    bluealign()
    height_thread = threading.Thread(target=blockheight) 
    height_thread.start()

    time.sleep(0.1)


    stop_thread = True
    
    print("PHASE 1 COMPLETE")
    time.sleep(2)

    #get past the 2nd block
    detect_red(frame)
    redalign()
    uapi.single_fly_forward(distance=40)

    print("PHASE 2 COMPLETE")

    #detect IMDA logo
    time.sleep(3)
    needgodown = True
    for i in range(50):
        frame = video.get_video()
        object_found, frame = detector.detect(frame)
        if not object_found is None:
            print(F"Found object: {object_found}")
            uapi.single_fly_lamplight(134,40,158,2,1)
            needgodown = False
            uapi.single_fly_touchdown()
            break
        else:
            uapi.single_fly_forward(distance = 2.5)
        cv2.imshow("Detection", frame)
        cv2.waitKey(1)
        time.sleep(0.1)
    cv2.destroyAllWindows()
    video.close()
    print("PHASE 3 COMPLETE")
    if needgodown:
        uapi.single_fly_touchdown()
