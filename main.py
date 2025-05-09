from picamera2 import Picamera2
import cv2
import face_recognition
import os
import time
import numpy as np
from datetime import datetime
from TextNotifier import TextNotifier
from FaceRecogniser import FaceRecogniser
from VideoRecorder import VideoRecorder
from EmailNotifier import EmailNotifier
from DBM import DatabaseManager

# Ensure output directories exist
image_output = './images'
if not os.path.exists(image_output):
    os.makedirs(image_output)
video_output = "./videos"
if not os.path.exists(video_output):
    os.makedirs(video_output)
    
face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')
# Mean frame value, movement_threshold for motion detection
last_mean = 0
movement_threshold = 20
# Track last time motion detected to delay stopping recording 
last_motion_time = None
first_motion_time = None
record_duration = 5
# Flag variables
recording, motion_detected, unknown_detected = False, False, False
writer = None
face_locations, face_names = None, None
frame_skip = 5
# Define fps and frame size for VideoWriter
fps = 6
frame_size = (640, 480)

# Frame rate tracking variables
frame_count = 0
fps_start_time = time.time()
fps = 0  # Initialize fps with a default value

# Calculate mean difference on frames
def movement(frame, last_mean):
    mean_difference = np.abs(np.mean(frame) - last_mean)
#    print(f"Mean difference: {mean_difference} Last mean: {last_mean} time: {time.strftime('%H:%M:%S', time.localtime())}")
    if mean_difference > movement_threshold:
        return True, np.mean(frame)  # Update last_mean
    return False, last_mean

# draw larger rectangle on user face for better user view
def adj_detect_face(img):
    face_img = img.copy()
    min_face_size=(200, 200)
    face_rects = face_cascade.detectMultiScale(face_img, scaleFactor=1.2, minNeighbors=5)

    for (x, y, w, h) in face_rects:
        # Visualising the face rectangle
        cv2.rectangle(face_img, (x-15, y-30), (x + w+15, y + h+30), (255, 255, 255), 10)
#        if w >= min_face_size[0] and h >= min_face_size[1] and photo_taken_flag == False:
#            photo_taken_flag = True
    return face_img

# Initialize Picamera2 and set the configuration
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))
picam2.start()
count = 0

base_frame = picam2.capture_array()
last_mean = np.mean(base_frame)

recogniser = FaceRecogniser()
emailer = EmailNotifier()
texter = TextNotifier()
db = DatabaseManager("10.62.135.55", "root", "password", "raspberrypi")
unknown_count = 0

while True:
    # Capture frame using picam then pass frame through face detection function
    frame = picam2.capture_array()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #frame = adj_detect_face(frame)
    # Calculate FPS every 10 frames
    frame_count += 1
    if frame_count >= 10:
        elapsed_time = time.time() - fps_start_time
        fps = frame_count / elapsed_time
        fps_start_time = time.time()
        frame_count = 0

    # Displays current time
    cv2.putText(frame, f"{time.strftime('%H:%M:%S', time.localtime())}", (10, 400), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
    # Displays frames per second
    cv2.putText(frame, f"FPS: {fps:.2f}", (500, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

    motion_detected, last_mean = movement(gray_frame, last_mean)

    if motion_detected:
        last_motion_time = time.time()
        if not recording:
            print("NOW RECORDING!")
            recording = True
            # Generate the timestamped file path
            file_path = f"{image_output}/img-{datetime.now().strftime('-%y%m%d-%H%M%S')}.png"

    if motion_detected:
        # Detect and recognize faces in the frame
        face_locations, face_labels = recogniser.identify_faces(frame)

        # Display results
        for (top, right, bottom, left), label in zip(face_locations, face_labels):
            if label == "Unknown":
                # Draw rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Display label below the face
                cv2.putText(frame, label, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                unknown_detected = True
                print(f"{label} detected!")
            else:
                # Draw rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                # Display label below the face
                cv2.putText(frame, label, (left, bottom + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                print(f"{label} detected!")
                
          
    if unknown_detected and unknown_count == 0:
        face = frame.copy()
        cv2.imwrite(file_path, face)
        #texter.message_user()
        texter.test_message("Warning, there is an intruder! Sheep is coming")
        # AUT firewall blocks email from being sent, code verified on home network
        # emailer.send_email("vinnielimbrick@gmail.com", "Person detected", "An unidentified person has been detected at your door. See attachment for further information", file_path)
        db.log_unknown_face(file_path)
        unknown_count += 1
        print("unknown detected")
    
    if recording and (time.time() - last_motion_time >= record_duration):
        print(f"Recording stopped: {file_path}")
        recording = False
        unknown_detected = False
        unknown_count = 0

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()

