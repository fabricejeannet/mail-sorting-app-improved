from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QGridLayout, QLabel
from picamera2.previews.qt import QGlPicamera2

class QtGui(QApplication):

    def __init__(self, camera) -> None:
        super().__init__([])
        self.qpicamera2 = QGlPicamera2(camera, width=426, height=240, keep_ar=False)

        self.window = QWidget()


        self.layout = QGridLayout()

        self.label_0 = QLabel("QLabel 0")
        self.label_0.setStyleSheet("background-color: blue") 
        self.label_0.resize(374,240)
        
        self.label_1 = QLabel("QLabel 1")
        self.label_1.setStyleSheet("background-color: lightgreen") 

        self.layout.addWidget(self.qpicamera2, 0, 0)
        self.layout.addWidget(self.label_0,0,1,2,1)
        self.layout.addWidget(self.label_1,1,0,1,1)

        self.window.setWindowTitle("MASAI")
        self.window.resize(800, 600)
        self.window.setLayout(self.layout)

        self.window.show()
        #self.window.showMaximized()

   