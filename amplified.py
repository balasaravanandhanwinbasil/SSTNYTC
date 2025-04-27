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
