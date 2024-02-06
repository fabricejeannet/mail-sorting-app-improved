from gui.qt_gui import QtGui
from camera.msi_camera import MSICamera
from camera.msi_image import MSIImage
from event.event import subscribe
from utils.constants import *
from utils.logging_filter import MyFilter
from ocr.msi_ocr import MSIOcr
import numpy as np
import cv2
import time
import logging
import os


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
        self.gui.qpicamera2.set_overlay(self._get_overlay())


        self.motion_detected_icon = cv2.imread(os.path.abspath(f"{os.getcwd()}/assets/img/icon_motion_detected.png"), cv2.IMREAD_UNCHANGED)
        self.msi_ocr = MSIOcr()
        self.gui.exec()


    def _handle_motion_detected_event(self, data) :
        self.motion_counter += 1
        self.gui.label_0.setText("Motion detected #" + str(self.motion_counter))
        logging.debug("MOTION_DECTED_EVENT #"  + str(self.motion_counter))
        overlay = self._get_overlay()
        overlay[0:32, 0:32] = self.motion_detected_icon
        self.gui.qpicamera2.set_overlay(overlay)


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
        msi_image = MSIImage(self.camera.rgb_image)
        ocr_results = self.msi_ocr.perform_on(msi_image.prepared_image)
        overlay = self._get_overlay()

        for result in ocr_results:
            logging.info(f"[{result.line}]\tx = {result.x}\ty = {result.y}\tw= {result.w}\th = {result.h}")
            cv2.rectangle(overlay, (result.x + TOP_LEFT_CORNER[0], result.y + TOP_LEFT_CORNER[1]), (result.x + result.w +TOP_LEFT_CORNER[0], result.y + result.h + TOP_LEFT_CORNER[1]), color=(255, 0, 0,64), thickness=2)
            cv2.putText(img=overlay, text=result.line, org=(result.x + TOP_LEFT_CORNER[0], result.y - 3 + TOP_LEFT_CORNER[1]), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=(0, 0, 255,100), thickness=2)

        self.gui.qpicamera2.set_overlay(overlay)
        

    def _get_overlay(self) :
        overlay = np.zeros((CAMERA_PREVIEW_HEIGHT, CAMERA_PREVIEW_WIDTH, 4), dtype=np.uint8)
        cv2.rectangle(overlay, (TOP_LEFT_CORNER[0], TOP_LEFT_CORNER[1]), (BOTTOM_RIGHT_CORNER[0], BOTTOM_RIGHT_CORNER[1]), color=(0, 255, 0,100), thickness=2)
        return overlay

app = App()

