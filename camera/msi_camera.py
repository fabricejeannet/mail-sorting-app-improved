from picamera2 import Picamera2, MappedArray
from libcamera import Transform
import cv2
import numpy as np
import time
from event.event import post_event
from utils.constants import *
import threading
import logging


class MSICamera (Picamera2):

    def __init__(self) :
        super().__init__()
        self._configure()
        self.last_motion_time = time.time()
        self._motion_detection_started = False
        self._was_steady = False
        self.rgb_image = None
        self.set_logging(Picamera2.ERROR)

    def _configure(self) : 
        self.configure(self.create_preview_configuration(main={ "size": (CAMERA_PREVIEW_WIDTH, CAMERA_PREVIEW_HEIGHT)}, transform=Transform(hflip=1, vflip=1)))


    def start_motion_detection(self) -> None:
        logging.debug("Starting motion detection.")
        self._motion_detection_started = True
        thread_movement_detection = threading.Thread(target=self._motion_detection)
        thread_movement_detection.start()


    def stop_motion_detection(self) -> None:
        self._motion_detection_started = False
        logging.debug("Motion detection stopped.")


    def _motion_detection(self) -> None :
        frame_count = 0
        previous_frame = None
        logging.debug("Motion detection started.")

        while self._motion_detection_started:

            if not self._motion_detection_started :
                break

            frame_count += 1

            # 1. Load image; convert to RGB
        
            self.rgb_image = cv2.cvtColor(self.capture_array(), cv2.COLOR_BGR2RGB)

            if ((frame_count % 2) == 0):

                # 2. Prepare image; grayscale and blur
                prepared_frame = cv2.cvtColor(self.rgb_image, cv2.COLOR_BGR2GRAY)
                prepared_frame = cv2.GaussianBlur(src=prepared_frame, ksize=(5,5), sigmaX=0)
            
                # 3. Set previous frame and continue if there is None
                if (previous_frame is None):
                    # First frame; there is no previous one yet
                    previous_frame = prepared_frame
                    continue
                
                # calculate difference and update previous frame
                diff_frame = cv2.absdiff(src1=previous_frame, src2=prepared_frame)
                previous_frame = prepared_frame

                # 4. Dilute the image a bit to make differences more seeable; more suitable for contour detection
                kernel = np.ones((3, 3))
                diff_frame = cv2.dilate(diff_frame, kernel, 1)

                # 5. Only take different areas that are different enough (>30 / 255)
                thresh_frame = cv2.threshold(src=diff_frame, thresh=20, maxval=255, type=cv2.THRESH_BINARY)[1]

                contours, _ = cv2.findContours(image=thresh_frame, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)

                motion_found = False
                '''
                index = 0
                while not motion_found and index < len(contours) - 1:
                    contour = contours[index]
                    motion_found = cv2.contourArea(contour) > MOTION_DETECTION_THRESHOLD
                    index += 1
                '''

                for contour in contours:
                    if cv2.contourArea(contour) < 50:
                        # too small: skip!
                        continue
                    motion_found = True

                if motion_found :                    
                    self.last_motion_time = time.time()
                    if self._was_steady : 
                        post_event(EVENTS.MOTION_DETECTED_EVENT)
                    self._was_steady = False
                else :
                    if not self._was_steady and time.time() - self.last_motion_time >= STEADY_TIMEOUT:
                        post_event(EVENTS.CAMERA_STEADY_EVENT)
                        self._was_steady = True
                
                