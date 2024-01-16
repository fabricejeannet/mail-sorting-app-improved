from gui.qt_gui import QtGui
from camera.camera import MSICamera
from event.event import subscribe
from utils.constants import *
from utils.logging_filter import MyFilter
import logging


class App():
    
    def __init__(self) -> None:

        logging.basicConfig(filename='masai.log', encoding='utf-8', level=logging.INFO)
        logging.getLogger().addFilter(MyFilter())

        logging.info("Initializing camera")
        self.motion_counter = 0
        self.steady_counter = 0
        self.camera = MSICamera()
        subscribe(EVENTS.MOTION_DETECTED_EVENT, self._handle_motion_detected_event)
        subscribe(EVENTS.CAMERA_STEADY_EVENT, self._handle_camera_steady_event)

        self.gui = QtGui(self.camera)
        self.camera.start()
        self.camera.start_motion_detection()

        self.gui.exec()


    def _handle_motion_detected_event(self, data) :
        self.motion_counter += 1
        self.gui.label_0.setText("Motion detected #" + str(self.motion_counter))
        #self.camera._motion_detection_started = False
        logging.debug("MOTION_DECTED_EVENT #"  + str(self.motion_counter))
        print("Motion detected #" + str(self.motion_counter))


    def _handle_camera_steady_event(self, data) :
        self.steady_counter += 1
        self.gui.label_0.setText("Steady #" + str(self.steady_counter))
        #self.camera._motion_detection_started = False
        logging.debug("CAMERA_STEADY_EVENT #"  + str(self.steady_counter))
        print("CAMERA_STEADY_EVENT #" + str(self.steady_counter))


app = App()

