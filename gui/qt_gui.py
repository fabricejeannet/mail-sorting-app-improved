from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QListWidget, QListWidgetItem, QScrollBar
from picamera2.previews.qt import QGlPicamera2
from gui.qt_match_widget import MatchWidget
from domain.match import Match
import logging
from utils.constants import *


class QtGui(QApplication):

    new_match_signal = QtCore.pyqtSignal(Match)


    def __init__(self, camera) -> None:
        super().__init__([])
        self.qpicamera2 = QGlPicamera2(camera, width=426, height=240, keep_ar=False)

        self.window = QWidget()
        self.window_layout = QGridLayout()

        self.list_widget = QListWidget(self.window)
        self.list_widget.setMaximumSize(374,600)

        self.scrollbar = QScrollBar(self.window)
        self.scrollbar.sliderMoved.connect(self.list_widget.setCurrentRow)

        self.label_1 = QLabel("QLabel 1")
        self.label_1.setMaximumSize(374,200)
        self.label_1.setStyleSheet("background-color: lightgreen") 

        self.window_layout.addWidget(self.qpicamera2, 0, 0)
        self.window_layout.setColumnStretch(0,0)
        self.window_layout.setRowStretch(0,0)

        self.window_layout.addWidget(self.list_widget,0,1,2,1)
        self.window_layout.addWidget(self.label_1,1,0,1,1)
        
        self.window.setWindowTitle("MASAI")
        self.window.resize(800, 600)
        self.window.setLayout(self.window_layout)


        self.new_match_signal.connect(self._add_match_widget)

        self.window.show()
        self.window.showMaximized()


    def _add_match_widget(self, match):
        logging.info(f"Adding widget for {match.company_name}")

        result_widget = MatchWidget(match)
        #result_widget.setStyleSheet("background-color: darkgrey")
                                    
        myQListWidgetItem = QListWidgetItem(self.list_widget)
        myQListWidgetItem.setSizeHint(result_widget.sizeHint())
        if match.status == SUBSCRIBED:
            myQListWidgetItem.setBackground(QColor("#43DE4F"))
        else:
            myQListWidgetItem.setBackground(QColor("#E37B83"))

        
        
        self.list_widget.addItem(myQListWidgetItem)
        self.list_widget.setItemWidget(myQListWidgetItem, result_widget)


    def display_results(self, matches) :
        self.list_widget.clear()
        self.scrollbar.setMaximum(len(matches))
        self.scrollbar.sliderMoved.connect(self.list_widget.setCurrentRow)
 
        for match in matches:
            self.new_match_signal.emit(match)


    def _clear_results_list(self) :
        for item in self.list_widget.items():
            self.list_widget.removeItemWidget(item)

   