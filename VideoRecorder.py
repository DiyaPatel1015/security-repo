import cv2
import time
from datetime import datetime

class VideoRecorder:
    def __init__(self, video_path=None, frame_size=(640, 480), fps=6):
        #if video_path is None:
        #    video_path = f"./videos/video-{datetime.now().strftime('%y%m%d-%H%M%S')}.mp4"
        self.video_path = video_path
        self.frame_size = frame_size
        self.fps = fps
        self.writer = None
        self.recording = False

    def start_recording(self):
        if not self.recording:
            video_path = f"./videos/video-{datetime.now().strftime('%y%m%d-%H%M%S')}.mp4"
            self.recording = True
            self.video_path = video_path
            self.writer = cv2.VideoWriter(self.video_path, cv2.VideoWriter_fourcc(*'mp4v'), self.fps, self.frame_size)
            self.start_recording_time = time.time()
            #self.video_path = f"./videos/video-{datetime.now().strftime('%y%m%d-%H%M%S')}.mp4"
            print(f"Recording started: {self.video_path}")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.end_recording_time = time.time()
            self.writer.release()
            print(f"Recording stopped: {self.video_path}")

    def write_frame(self, frame):
        if self.recording:
            self.writer.write(frame)

    def is_recording(self):
        return self.recording
