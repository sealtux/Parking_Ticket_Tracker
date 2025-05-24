from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout,QTableWidget,QHeaderView,QAbstractItemView,QPushButton,QTableWidgetItem
from PyQt6.QtCore import Qt
import mysql.connector
from mysql.connector import Error
table = None


    
class savecustom(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

     
        self.panel = QLabel(self)
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(0, 0, 1300, 850) #change the position
        self.panel.setStyleSheet("background-color: #F2F2E6;")  # apply color


        