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
from domain.matcher import Matcher
from domain.csv_file import CsvFile


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
        self.ocr_results = []

        #TODO Implémenter la recherche du dernier CSV du répoertoire
        self.matcher = Matcher(CsvFile("/home/fabrice/Public/csv/Clients (49).csv"))

        self.gui.exec()


    def _handle_motion_detected_event(self, data) :
        self.motion_counter += 1
        logging.debug("MOTION_DECTED_EVENT #"  + str(self.motion_counter))
        overlay = self._get_overlay()
        overlay[0:32, 0:32] = self.motion_detected_icon
        self.gui.qpicamera2.set_overlay(overlay)


    def _handle_camera_steady_event(self, data) :
        self.steady_counter += 1
        logging.debug("CAMERA_STEADY_EVENT #"  + str(self.steady_counter))
        start = time.time()
        self._perform_ocr()
        matching_results = self._perform_matching()
        self.gui.display_results(matching_results)
        end = time.time()
        logging.info(f"Total duration : {round(end - start,2)}s")


    def _perform_ocr(self) -> None :
        if self.camera.rgb_image is None:
            return
        msi_image = MSIImage(self.camera.rgb_image)
       
        ocr_start_time = time.time()
        self.ocr_results = self.msi_ocr.perform_on(msi_image.prepared_image)
        ocr_end_time = time.time()
        logging.info(f"OCR duration : {round(ocr_end_time - ocr_start_time,2)}s")

        overlay_start_time = time.time()
        overlay = self._get_overlay()

        for result in self.ocr_results:
            logging.info(f"[{result.line}]\tx = {result.x}\ty = {result.y}\tw= {result.w}\th = {result.h}")
            cv2.rectangle(overlay, (result.x + CROPPED_IMAGE_TOP_LEFT_CORNER[0], result.y + CROPPED_IMAGE_TOP_LEFT_CORNER[1]), (result.x + result.w +CROPPED_IMAGE_TOP_LEFT_CORNER[0], result.y + result.h + CROPPED_IMAGE_TOP_LEFT_CORNER[1]), color=(255, 0, 0,64), thickness=2)
            cv2.putText(img=overlay, text=result.line, org=(result.x + CROPPED_IMAGE_TOP_LEFT_CORNER[0], result.y - 3 + CROPPED_IMAGE_TOP_LEFT_CORNER[1]), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1, color=(0, 0, 255,100), thickness=2)

        self.gui.qpicamera2.set_overlay(overlay)
        overlay_end_time = time.time()
        logging.info(f"Overlay duration : {round(overlay_end_time - overlay_start_time,2)}s")


    def _get_overlay(self) :
        overlay = np.zeros((CAMERA_PREVIEW_HEIGHT, CAMERA_PREVIEW_WIDTH, 4), dtype=np.uint8)
        cv2.rectangle(overlay, (CROPPED_IMAGE_TOP_LEFT_CORNER[0], CROPPED_IMAGE_TOP_LEFT_CORNER[1]), (CROPPED_IMAGE_BOTTOM_RIGHT_CORNER[0], CROPPED_IMAGE_BOTTOM_RIGHT_CORNER[1]), color=(0, 255, 0,100), thickness=2)
        return overlay


    def _perform_matching(self):
        logging.info("Searching for matchs in DB")
        matching_start_time = time.time()
        matching_results = self.matcher.get_match_for_ocr_results(self.ocr_results)
        for result in matching_results:
            logging.info(result)
        matching_end_time = time.time()
        logging.info(f"Matching duration : {round(matching_end_time - matching_start_time,2)}s")
        return matching_results


app = App()

