from gui.qt_gui import QtGui
from camera.msi_camera import MSICamera
from camera.msi_image import MSIImage
from event.event import subscribe
from utils.constants import *
from utils.logging_filter import MyFilter
from ocr.msi_ocr import MSIOcr
import numpy as np


import time
import logging


class App():
    
    def __init__(self) -> None:

        logging.basicConfig(filename='masai.log', encoding='utf-8', level=logging.INFO)
        #logging.getLogger().addFilter(MyFilter())

        logging.info("Initializing camera")
        self.motion_counter = 0
        self.steady_counter = 0
        self.camera = MSICamera()
        subscribe(EVENTS.MOTION_DETECTED_EVENT, self._handle_motion_detected_event)
        subscribe(EVENTS.CAMERA_STEADY_EVENT, self._handle_camera_steady_event)

        self.gui = QtGui(self.camera)
        self.camera.start()
        self.camera.start_motion_detection()
        #self.camera.set_overlay(self.camera.overlay)

        self.msi_ocr = MSIOcr()
        self.gui.exec()


    def _handle_motion_detected_event(self, data) :
        self.motion_counter += 1
        self.gui.label_0.setText("Motion detected #" + str(self.motion_counter))
        logging.debug("MOTION_DECTED_EVENT #"  + str(self.motion_counter))


    def _handle_camera_steady_event(self, data) :
        self.steady_counter += 1
        self.gui.label_0.setText("Steady #" + str(self.steady_counter))
        logging.debug("CAMERA_STEADY_EVENT #"  + str(self.steady_counter))
        start = time.time()
        self._perform_ocr()
        end = time.time()
        logging.info(f"Time : {round(end - start,2)}s")


    def _perform_ocr(self) -> None :
        if self.camera.rgb_image is None:
            return
        image = MSIImage(self.camera.rgb_image)
        ocr_results = self.msi_ocr.perform_on(image.rgb_image)
        for result in ocr_results:
            overlay = np.zeros((426, 240, 4), dtype=np.uint8)
            overlay[np.array(result.bounding_box)] = (255, 0, 0, 64) # reddish
            self.camera.super().set_overlay(overlay)



app = App()

