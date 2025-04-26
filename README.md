# Security System Project

This project is a **smart security system** that uses **face recognition**, **object detection**, and **real-time notifications** via **email** and **text messages**.  
It also supports **video recording** and maintains a database of unknown faces.

## Features

- 🔍 **Face Recognition** — Identifies known individuals and alerts when unknown faces are detected.
- 🧠 **Object Detection** — Detects common objects using MobileNet SSD.
- ✉️ **Email and SMS Notifications** — Sends alerts when events are triggered.
- 🎥 **Video Recording** — Records footage when activity is detected.
- 🗄️ **Unknown Face Database** — Stores images of unknown individuals for later review.

## Project Structure

| File/Folder                  | Purpose |
| :---------------------------- | :------ |
| `main.py`                     | Main program to start the system |
| `FaceRecogniser.py`            | Face recognition functions |
| `ObjectDetector.py`            | Object detection using MobileNetSSD |
| `EmailNotifier.py`             | Email notification system |
| `TextNotifier.py`              | SMS notification system |
| `VideoRecorder.py`             | Video recording utilities |
| `DBM.py`                       | Database manager for unknown faces |
| `communication_manager.py`     | Handles sending alerts |
| `encoding_photo.py`            | Encodes face images for recognition |
| `data/`                        | Haarcascade model for face detection |
| `MobileNetSSD_deploy.caffemodel`, `MobileNetSSD_deploy.prototxt` | Object detection model files |
| `coco.names`                   | List of object classes |
| `unknown_faces.db`             | Database storing unknown faces |

## Requirements

- Python 3.7+
- Libraries:
  - `opencv-python`
  - `numpy`
  - `imutils`
  - `smtplib` (built-in)
  - `email` (built-in)
  - `sqlite3` (built-in)
  - `twilio` (for text messaging)

You can install the external libraries using:

```bash
pip install opencv-python numpy imutils twilio
```

## Setup

1. **Clone the repository** (or unzip the files).
2. **Set up email and SMS credentials** in the `keys.py` file:
   - Email server, email address, password.
   - Twilio account SID, auth token, and phone numbers.
3. **Add known face images** to the `encoding_images/` folder and encode them using `encoding_photo.py`.
4. **Run the main program**:

```bash
python main.py
```

## Notes

- Make sure your webcam is connected and accessible.
- Twilio setup is needed for SMS notification (you'll need a Twilio account).
- Configure thresholds (confidence levels) inside `FaceRecogniser.py` and `ObjectDetector.py` if needed.
- Modify notification messages and behaviors inside `communication_manager.py`.

## Future Improvements

- Add a web dashboard for remote monitoring.
- Improve face recognition accuracy with deep learning models.
- Expand object detection to custom classes.
