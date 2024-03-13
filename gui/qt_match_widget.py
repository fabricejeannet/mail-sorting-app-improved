from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from domain.match import Match
from utils.constants import *
import os
import logging


class MatchWidget(QWidget):

    def __init__(self, match:Match, parent=None):
        super(MatchWidget, self).__init__(parent)

        self.img_path = f"{os.getcwd()}/assets/img/"

        super().__init__(parent)

        #self.setFixedSize(140,30)
        self.setMaximumSize(364, 90)
        self.layout = QGridLayout()
        
        self.label_logo = QLabel() 
        self.label_logo.setMaximumWidth(64)
        self.label_logo.setPixmap(QtGui.QPixmap(self.img_path + f"logo_{match.domiciliary}.png"))
        logging.debug(f"logo : {self.img_path}logo_{match.domiciliary}.png")

                      
        self.layout.addWidget(self.label_logo,0,0,3,1)

        self.label_company_name = QLabel(self._get_empty_string_if_null(match.company_name))
        self.label_icon_company = QLabel() 
        self.label_icon_company.setMaximumSize(16, 16)
        self.label_icon_company.setPixmap(QtGui.QPixmap(self.img_path + "icon_company.png"))
        self.label_company_ratio = QLabel(self._get_ratio(match, COMPANY_NAME))
        self.layout.addWidget(self.label_icon_company,0,1,1,1)
        self.layout.addWidget(self.label_company_name,0,2,1,1)
        self.layout.addWidget(self.label_company_ratio,0,3,1,1)

        #if len(match.trademark) == 0 :
        self.label_trademark = QLabel(str(match.trademark))
        self.label_icon_trademark = QLabel() 
        self.label_icon_trademark.setMaximumSize(16, 16)
        self.label_icon_trademark.setPixmap(QtGui.QPixmap(self.img_path + "icon_trademark.png"))
        self.label_trademark_ratio = QLabel(self._get_ratio(match, TRADEMARK))
        self.layout.addWidget(self.label_icon_trademark,1,1,1,1)
        self.layout.addWidget(self.label_trademark,1,2,1,1)
        self.layout.addWidget(self.label_trademark_ratio,1,3,1,1)
    
        self.label_owner = QLabel(str(match.owner)) 
        self.label_icon_owner = QLabel() 
        self.label_icon_owner.setMaximumSize(16, 16)
        self.label_icon_owner.setPixmap(QtGui.QPixmap(self.img_path + "icon_owner.png"))
        self.label_owner_ratio = QLabel(self._get_ratio(match, OWNER))
        self.layout.addWidget(self.label_icon_owner,2,1,1,1)
        self.layout.addWidget(self.label_owner,2,2,1,1)
        self.layout.addWidget(self.label_owner_ratio,2,3,1,1)

        

    

        

        self.setLayout(self.layout)


    def _get_ratio(self, match:Match, column:str) -> str:
        if column in match.matching_ratio.keys():
            return f"{match.matching_ratio[column]}%"
        else:
            return "-" 


    def _get_empty_string_if_null(self, string_to_check) -> str :
        if not string_to_check:
            return ""
        return string_to_check