from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class Transactionsframe(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

     
        self.panel = QLabel(self)
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(0, 0, 1500, 900)
        self.panel.setStyleSheet("background-color: #F2F2E6;")  # apply color
        # Apply a white background
        #self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        #self.setStyleSheet("background-color: white;")
        
       