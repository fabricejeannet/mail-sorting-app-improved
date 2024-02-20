from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from domain.match import Match
from utils.constants import *
import os

class MatchWidget(QWidget):

    def __init__(self, match:Match, parent=None):
        super().__init__(parent)

        #self.setFixedSize(140,30)
        self.setStyleSheet("background-color: yellow") 

        self.layout = QGridLayout()
        self.label_company_name = QLabel(self._get_empty_string_if_null(match.company_name))
        self.label_trademark = QLabel(str(match.trademark))
        self.label_owner = QLabel(str(match.owner)) 

        self.label_logo = QLabel() 
        self.label_logo.setPixmap(QtGui.QPixmap(self._get_logo(self._get_empty_string_if_null(match.domiciliary))))

        self.label_ratio = QLabel("80%")

        self.layout.addWidget(self.label_logo,0,0,3,1)
        self.layout.addWidget(self.label_company_name,0,1,1,1)
        self.layout.addWidget(self.label_trademark,1,1,1,1)
        self.layout.addWidget(self.label_owner,2,1,1,1)
        self.layout.addWidget(self.label_ratio,0,2,3,1)
        self.setLayout(self.layout)

    def _get_logo(self, domiciliary):
        return os.path.abspath(f"{os.getcwd()}/assets/img/logo_{domiciliary}.png")
        
    def _get_empty_string_if_null(self, string_to_check) -> str :
        if not string_to_check:
            return ""
        return string_to_check