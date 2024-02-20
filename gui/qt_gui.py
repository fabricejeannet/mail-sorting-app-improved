from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget, QGridLayout, QLabel
from picamera2.previews.qt import QGlPicamera2
from gui.qt_match_widget import MatchWidget
from domain.match import Match
import logging


class QtGui(QApplication):

    new_match_signal = QtCore.pyqtSignal(Match)


    def __init__(self, camera) -> None:
        super().__init__([])
        self.qpicamera2 = QGlPicamera2(camera, width=426, height=240, keep_ar=False)

        self.window = QWidget()


        self.layout = QGridLayout()

        self.right_widget = QWidget()
        self.vbox_layout = QVBoxLayout()

        self.right_widget.setLayout(self.vbox_layout)

        self.label_1 = QLabel("QLabel 1")
        self.label_1.setStyleSheet("background-color: lightgreen") 

        self.layout.addWidget(self.qpicamera2, 0, 0)
        self.layout.setColumnStretch(0,0)
        self.layout.setRowStretch(0,0)

        self.layout.addWidget(self.right_widget,0,1,2,1)
        self.layout.addWidget(self.label_1,1,0,1,1)
        
        self.window.setWindowTitle("MASAI")
        self.window.resize(800, 600)
        self.window.setLayout(self.layout)


        self.new_match_signal.connect(self._add_match_widget)

        self.window.show()
        #self.window.showMaximized()


    def _add_match_widget(self, match):
        logging.info(f"Adding widget for {match.company_name}")
        result_widget = MatchWidget(match)
        result_widget.setStyleSheet("background-color: darkgrey") 
        result_widget
        self.vbox_layout.addWidget(result_widget)


    def display_results(self, matches) :
        self._clear_results_list() 
        for match in matches:
            self.new_match_signal.emit(match)


    def _clear_results_list(self) :
        for child, index in enumerate(self.vbox_layout.children()):
            item = self.vbox_layout.itemAt(index)
            self.vbox_layout.removeItem(index)
            item.deleteLater()
            
            

   