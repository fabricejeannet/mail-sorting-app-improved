from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from domain.match import Match
from utils.constants import *
import os

class MatchWidget(QWidget):

    def __init__(self, match:Match, parent=None):
        super(MatchWidget, self).__init__(parent)

        self.img_path = f"{os.getcwd()}/assets/img/"

        super().__init__(parent)

        #self.setFixedSize(140,30)
        self.setMaximumHeight(90)

        self.layout = QGridLayout()
        self.label_company_name = QLabel(self._get_empty_string_if_null(match.company_name))
        self.label_trademark = QLabel(str(match.trademark))
        self.label_owner = QLabel(str(match.owner)) 

        self.label_logo = QLabel() 
        self.label_logo.setMaximumWidth(64)
        self.label_logo.setPixmap(QtGui.QPixmap(self.img_path + f"logo_{match.domiciliary}.png"))

        self.label_icon_company = QLabel() 
        self.label_icon_company.setMaximumSize(16, 16)
        self.label_icon_company.setPixmap(QtGui.QPixmap(self.img_path + "icon_company.png"))

        self.label_icon_trademark = QLabel() 
        self.label_icon_trademark.setMaximumSize(16, 16)
        self.label_icon_trademark.setPixmap(QtGui.QPixmap(self.img_path + "icon_trademark.png"))

        self.label_icon_owner = QLabel() 
        self.label_icon_owner.setMaximumSize(16, 16)
        self.label_icon_owner.setPixmap(QtGui.QPixmap(self.img_path + "icon_owner.png"))

        self.label_ratio = QLabel("80%")
        self.label_ratio.setMaximumWidth(40)

        self.layout.addWidget(self.label_logo,0,0,3,1)

        self.layout.addWidget(self.label_icon_company,0,1,1,1)
        self.layout.addWidget(self.label_company_name,0,2,1,1)

        self.layout.addWidget(self.label_icon_trademark,1,1,1,1)
        self.layout.addWidget(self.label_trademark,1,2,1,1)

        self.layout.addWidget(self.label_icon_owner,2,1,1,1)
        self.layout.addWidget(self.label_owner,2,2,1,1)

        self.layout.addWidget(self.label_ratio,0,3,3,1)

        self.setLayout(self.layout)

    def _get_logo(self, domiciliary):
        return self.img_path + "logo_{domiciliary}.png"
        
    def _get_empty_string_if_null(self, string_to_check) -> str :
        if not string_to_check:
            return ""
        return string_to_check