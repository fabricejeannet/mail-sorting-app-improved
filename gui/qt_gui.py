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
from PyQt5.QtGui import QKeySequence


class QtGui(QApplication):

    new_match_signal = QtCore.pyqtSignal(Match)
    no_match_signal = QtCore.pyqtSignal()

    def __init__(self, camera) -> None:
        super().__init__([])

        self.csv_file_infos = None
        self.window = QWidget()
        self.window.setWindowTitle("MASAI")
        self.window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.stacked_widget = QStackedWidget()

        self.qpicamera2 = QGlPicamera2(camera, width=CAMERA_PREVIEW_WIDTH, height=CAMERA_PREVIEW_HEIGHT, keep_ar=False)
        self.qpicamera2.setFixedSize(CAMERA_PREVIEW_WIDTH, CAMERA_PREVIEW_HEIGHT)
        self.stacked_widget.addWidget(self.qpicamera2)
        
        self.keyboard_input_widget = QWidget()

        self.kb_vlayout = QVBoxLayout()
        self.kb_hlayout = QHBoxLayout()
        self.text_input = QLineEdit()
        self.text_input.returnPressed.connect(self._search)

        self.kb_vlayout.addWidget(self.text_input)

        self.keyboard_input_widget.setLayout(self.kb_vlayout)
        self.stacked_widget.addWidget(self.keyboard_input_widget)

        self.kb_button_widget = QWidget()
        self.kb_button_widget.setLayout(self.kb_hlayout)
        self.button_search = QPushButton("[Enter ⏎] Rechercher")
        self.button_search.setAutoDefault(True)

        self.button_search.clicked.connect(self._search)

        self.button_erase = QPushButton("[Ctrl + ⬅] Effacer")
        self.button_erase.clicked.connect(self._clear_text_input)
        self.button_erase.setAutoDefault(True)
        
        

        self.kb_hlayout.addWidget(self.button_erase)
        self.kb_hlayout.addWidget(self.button_search)

        self.kb_vlayout.addWidget(self.kb_button_widget)

        self.match_list_widget = QListWidget()
        self.match_list_widget.setMaximumSize(WINDOW_WIDTH - CAMERA_PREVIEW_WIDTH,600)


        self.label_infos = QLabel()
        self.label_infos.setMaximumHeight(20)
        
        self._init_main_buttons()
        self._init_window_layout()
        self._init_shortcuts()
        self._connect_signals()
        self._in_video_mode = True

        self.window.showMaximized()


    def _init_window_layout(self) -> None: 
        self.window_layout = QGridLayout()
        self.window.setLayout(self.window_layout)
        self.window_layout.addWidget(self.stacked_widget, 0, 0)
        self.window_layout.addWidget(self.match_list_widget,0,1,3,1)
        self.window_layout.addWidget(self.label_infos, 1,0,1,1)
        self.window_layout.addWidget(self.button_widget, 2,0,1,1)


    def _init_main_buttons(self) -> None:
        self.button_layout = QHBoxLayout()
        self.button_widget = QWidget()
        self.button_widget.setLayout(self.button_layout)
       
        self.toggle_mode_button = QPushButton("[F1] Changer de mode")
        self.toggle_mode_button.clicked.connect(self._toggle_input_mode)
        self.button_layout.addWidget(self.toggle_mode_button)
        self.button_layout.addWidget(QPushButton("Bouton 2"))
        self.button_layout.addWidget(QPushButton("Bouton 3"))



    def _init_shortcuts(self) -> None:
        ctrl_backspace = QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Backspace)
        erase_shortcut = QShortcut(ctrl_backspace, self.window)
        erase_shortcut.activated.connect(self._clear_text_input)

        f1 = QKeySequence(QtCore.Qt.Key_F1)
        toggle_input_mode_shortcut = QShortcut(f1, self.window)
        toggle_input_mode_shortcut.activated.connect(self._toggle_input_mode)


    def _connect_signals(self) -> None :
        self.new_match_signal.connect(self._add_match_widget)
        self.no_match_signal.connect(self._add_no_match_found_widget)


    def set_csv_file_info(self, infos) -> None :
        self.label_infos.setText(f"Fichier : {infos}")



    def _add_match_widget(self, match):
        logging.info(f"Adding widget for {match.company_name}")
        match_widget = MatchWidget(match)

        myQListWidgetItem = QListWidgetItem(self.match_list_widget)
        match_widget.setObjectName(f"match_widget_{self.match_counter}")

        myQListWidgetItem.setSizeHint(match_widget.sizeHint())
        
        if match.status == SUBSCRIBED:
            myQListWidgetItem.setBackground(QColor(GREEN)) 
        else:
            myQListWidgetItem.setBackground(QColor(RED))

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
        self.match_list_widget.clear()
        if self._in_video_mode :
            logging.debug("Video input mode.")
            self.stacked_widget.setCurrentIndex(0)
            post_event(EVENTS.START_MOTION_DETECTION)
            post_event(EVENTS.CAMERA_STEADY_EVENT)
        else : 
            logging.debug("Text input mode.")
            post_event(EVENTS.STOP_MOTION_DETECTION)
            self.stacked_widget.setCurrentIndex(1)
            self.text_input.setFocus()
        


    def _clear_text_input(self) :
        self.text_input.clear()
        self.text_input.setFocus()
        self.match_list_widget.clear()


    def _search(self) :
        post_event(EVENTS.PERFORM_MATCHING, self.text_input.text())

    