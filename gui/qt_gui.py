from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QListWidget, QListWidgetItem, QScrollBar
from picamera2.previews.qt import QGlPicamera2
from gui.qt_match_widget import MatchWidget
from gui.qt_no_match_found_widget import NoMatchFoundWidget

from matcher.match import Match
import logging
from utils.constants import *


class QtGui(QApplication):

    new_match_signal = QtCore.pyqtSignal(Match)
    no_match_signal = QtCore.pyqtSignal()

    def __init__(self, camera) -> None:
        super().__init__([])
        self.qpicamera2 = QGlPicamera2(camera, width=CAMERA_PREVIEW_WIDTH, height=CAMERA_PREVIEW_HEIGHT, keep_ar=False)
        self.qpicamera2.setFixedSize(CAMERA_PREVIEW_WIDTH, CAMERA_PREVIEW_HEIGHT)
        
        self.window = QWidget()
        self.window_layout = QGridLayout()

        self.match_list_widget = QListWidget()
        self.match_list_widget.setMaximumSize(WINDOW_WIDTH - CAMERA_PREVIEW_WIDTH,600)
        self.window_layout.addWidget(self.match_list_widget,0,1,2,1)

        self.window_layout.addWidget(self.qpicamera2, 0, 0)
        
        self.window.setWindowTitle("MASAI")
        self.window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.window.setLayout(self.window_layout)

        self.new_match_signal.connect(self._add_match_widget)
        self.no_match_signal.connect(self._add_no_match_found_widget)

        self.window.show()
        self.window.showMaximized()


    def _add_match_widget(self, match):
        logging.info(f"Adding widget for {match.company_name}")
        match_widget = MatchWidget(match)

        myQListWidgetItem = QListWidgetItem(self.match_list_widget)
        match_widget.setObjectName(f"match_widget_{self.match_counter}")

        myQListWidgetItem.setSizeHint(match_widget.sizeHint())
        
        if match.status == SUBSCRIBED:
            #match_widget.setObjectName("subscribed")
            myQListWidgetItem.setBackground(QColor("#43DE4F")) 
        else:
            myQListWidgetItem.setBackground(QColor("#E37B83"))
            #match_widget.setObjectName("unsubscribed")

        self.match_list_widget.addItem(myQListWidgetItem)
        self.match_list_widget.setItemWidget(myQListWidgetItem, match_widget)


    def display_matches(self, matches) :
        self.match_counter = 0
        self.match_list_widget.clear()
        for match in matches:
            self.new_match_signal.emit(match)


    def display_no_match_found(self) :
        self.no_match_signal.emit()


    def _add_no_match_found_widget(self):
        logging.info(f"Adding widget for no match found")

        self.match_list_widget.clear()

        no_match_found_widget = NoMatchFoundWidget()
        myQListWidgetItem = QListWidgetItem(self.match_list_widget)
        myQListWidgetItem.setSizeHint(no_match_found_widget.sizeHint())
  
        self.match_list_widget.addItem(myQListWidgetItem)
        self.match_list_widget.setItemWidget(myQListWidgetItem, no_match_found_widget)
    