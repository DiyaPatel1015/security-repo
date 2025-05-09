import numpy as np
import cv2
from picamera2 import Picamera2
import os
import requests  # For making HTTP requests
from DBM import DatabaseManager
from datetime import datetime
from TextNotifier import TextNotifier

# File paths
prototxt_path = "MobileNetSSD_deploy.prototxt"
model_path = "MobileNetSSD_deploy.caffemodel"

# Check if files exist
if not os.path.isfile(prototxt_path):
    print(f"Prototxt file not found: {prototxt_path}")
    exit()
if not os.path.isfile(model_path):
    print(f"Model file not found: {model_path}")
    exit()

db = DatabaseManager("10.62.135.55", "root", "password", "raspberrypi")
txt = TextNotifier()

# Initialize the camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))
picam2.start()

# Load the model
try:
    net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)
except Exception as e:
    print(f"Error loading model: {e}")
    exit()


# Load class labels
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
           "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
           "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
           "sofa", "train", "tvmonitor", "knife", "gun", "bat"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

# Function to call the police
def call_police():
    # Replace with actual service/API call to emergency services
    print("Calling the police... (This is a placeholder function)")

# Function to notify the user
def notify_user():
    # Replace with actual user notification method (SMS, app notification, etc.)
    txt.test_message("THREAT DETECTED. POLICE NOTIFIED. RUN AND HIDE.")

identified = False

# Loop to continuously capture frames
try:
    while True:
        # Capture frame
        frame = picam2.capture_array()
        height, width = frame.shape[:2]

        # Prepare the frame for the model
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        net.setInput(blob)
        detections = net.forward()

        # Process detections
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.2:  # Confidence threshold
                class_id = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                (startX, startY, endX, endY) = box.astype("int")
                label = f"{CLASSES[class_id]}: {confidence:.2f}"

                # Draw bounding box and label on the frame
                cv2.rectangle(frame, (startX, startY), (endX, endY), COLORS[class_id], 2)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[class_id], 2)

                # Check for threatening objects, 'person' used for testing purposes
                if CLASSES[class_id] in ["gun", "knife", "bat", "person"]:
                    if identified == False:
                        file_path = f"incidents/img-{datetime.now().strftime('-%y%m%d-%H%M%S')}.png"
                        cv2.imwrite(file_path, frame)
                        identified = True
                        db.log_weapon(class_id, file_path)
                        print("Threat detected! Initiating emergency procedures...")
                        call_police()
                        notify_user()
                        
        # Show the output frame
        cv2.imshow("MobileNet SSD Object Detection", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

finally:
    # Cleanup
    picam2.stop()
    cv2.destroyAllWindows()
