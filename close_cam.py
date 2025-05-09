from picamera2 import Picamera2
import cv2
import face_recognition
import os
import time
import numpy as np
from VideoRecorder import VideoRecorder
from FaceRecogniser import FaceRecogniser

# Ensure output directories exist
image_output = './images'
if not os.path.exists(image_output):
    os.makedirs(image_output)
video_output = "./videos"
if not os.path.exists(video_output):
    os.makedirs(video_output)
    

# Initialize Picamera2 and set the configuration
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))
picam2.start()
count = 0


cv2.destroyAllWindows()
picam2.stop()
