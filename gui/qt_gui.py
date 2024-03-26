from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import *
from picamera2.previews.qt import QGlPicamera2
from gui.qt_match_widget import MatchWidget
from gui.qt_no_match_found_widget import NoMatchFoundWidget

from matcher.match import Match
import logging
from utils.constants import *
from event.event import post_event


class QtGui(QApplication):

    new_match_signal = QtCore.pyqtSignal(Match)
    no_match_signal = QtCore.pyqtSignal()

    def __init__(self, camera) -> None:
        super().__init__([])

        self.window = QWidget()
        self.window.setWindowTitle("MASAI")
        self.window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.window_layout = QGridLayout()
        self.window.setLayout(self.window_layout)

        self.stacked_widget = QStackedWidget()
        self.window_layout.addWidget(self.stacked_widget, 0, 0)


        self.qpicamera2 = QGlPicamera2(camera, width=CAMERA_PREVIEW_WIDTH, height=CAMERA_PREVIEW_HEIGHT, keep_ar=False)
        self.qpicamera2.setFixedSize(CAMERA_PREVIEW_WIDTH, CAMERA_PREVIEW_HEIGHT)
        self.stacked_widget.addWidget(self.qpicamera2)


        self.keyboard_input_widget = QWidget()

        self.kb_vlayout = QVBoxLayout()
        self.kb_hlayout = QHBoxLayout()
        self.text_input = QLineEdit()
        self.kb_vlayout.addWidget(self.text_input)

        self.keyboard_input_widget.setLayout(self.kb_vlayout)
        self.stacked_widget.addWidget(self.keyboard_input_widget)

        self.kb_button_widget = QWidget()
        self.kb_button_widget.setLayout(self.kb_hlayout)
        self.button_search = QPushButton("Rechercher")
        self.button_search.clicked.connect(self._search)

        self.button_erase = QPushButton("Effacer")
        self.button_erase.clicked.connect(self._clear_text_input)
        self.kb_hlayout.addWidget(self.button_erase)
        self.kb_hlayout.addWidget(self.button_search)

        self.kb_vlayout.addWidget(self.kb_button_widget)

        self.match_list_widget = QListWidget()
        self.match_list_widget.setMaximumSize(WINDOW_WIDTH - CAMERA_PREVIEW_WIDTH,600)
        self.window_layout.addWidget(self.match_list_widget,0,1,2,1)

        self._in_video_mode = True
        self.toggle_mode_button = QPushButton("Changer de mode")
        self.toggle_mode_button.clicked.connect(self._toggle_input_mode)
        self.button_layout = QHBoxLayout()
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_layout)
       
        self.button_layout.addWidget(self.toggle_mode_button)
        self.button_layout.addWidget(QPushButton("Bouton 2"))
        self.button_layout.addWidget(QPushButton("Bouton 3"))

        self.window_layout.addWidget(self.button_widget, 1,0,1,1)


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


    def _toggle_input_mode(self):
        self._in_video_mode = not self._in_video_mode
        if self._in_video_mode :
            self.stacked_widget.setCurrentIndex(0)
        else : 
            self.stacked_widget.setCurrentIndex(1)
            self.text_input.setFocus()
        logging.debug(f"In video mode {self._in_video_mode}")


    def _clear_text_input(self) :
        self.text_input.clear()
        self.text_input.setFocus()
        self.match_list_widget.clear()


    def _search(self) :
        post_event(EVENTS.PERFORM_MATCHING, self.text_input.text())

    