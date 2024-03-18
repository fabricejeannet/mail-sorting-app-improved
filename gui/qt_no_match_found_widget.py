from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from matcher.match import Match
from utils.constants import *

class NoMatchFoundWidget(QWidget):
    
    def __init__(self, parent=None):
        super(NoMatchFoundWidget, self).__init__(parent)
        super().__init__(parent)

        self.layout = QGridLayout()

        self.label_icon = QLabel() 
        self.label_icon.setMaximumWidth(64)
        self.label_icon.setPixmap(QtGui.QPixmap(ICON_NO_MATCH_FOUND))
        self.layout.addWidget(self.label_icon,0,0,1,1)

        self.label_message = QLabel(f"Aucune correspondance trouvée.")
        self.layout.addWidget(self.label_message, 0,1,1,1)
        self.setLayout(self.layout)
