from picamera2 import Picamera2
import cv2
import face_recognition
import os

# Ensure output directories exist
image_output = './encoding_images'
if not os.path.exists(image_output):
    os.makedirs(image_output)


# Initialize Picamera2 and set the configuration
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"}))
picam2.start()

print("Press 's' to take snap and 'q' to quit")

while True:
	#Capture frame using picam then pass frame through face detection function
    frame = picam2.capture_array()
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        saved_face = input('Enter person\'s name')
        output_path = os.path.join(image_output, f'{saved_face}.png')
        cv2.imwrite(output_path, frame)
        print(f"Image saved at{image_output}")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.stop()
