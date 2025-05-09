README please

Set up virtual environment in order to install face_recognition module. Virtual environment was necessary to
install face_recognition module on raspberry pi

command line:
sudo apt update
sudo apt install python3-venv
python3 -m venv --system-site-packages myenv
source myenv/bin/activate
pip install dlib face_recognition

face_recognition module
sudo apt update
sudo apt install -y build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev libboost-python-dev python3-pip

Run main.py to use the facial recognition program which detects a known or unknown user and notifies the user.
Run ObjectDetector.py to use the object detection program which detects if the presence of a threat is detected on camera,
gun, bat or knife, and notifies the user. "person" was left in the threat list for testing purposes.
