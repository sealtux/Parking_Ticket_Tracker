from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout,QTableWidget,QHeaderView,QAbstractItemView,QPushButton,QTableWidgetItem
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
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
        self.questionlabel = QLabel("Do You Have Questions?", self.panel)

        self.questionlabel.setGeometry(400, 50, 1000, 70)  # Set position and size
        self.questionlabel.setStyleSheet("font-size: 40px; font-weight: bold; color: #333;")
        
        self.secquestionlabel = QLabel("We have answers (well, most of the times)", self.panel)
        self.secquestionlabel.setGeometry(438, 120, 1000, 70)  # Set position and size
        self.secquestionlabel.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        self.image_label = QLabel(self.panel)
        self.image_label.setGeometry(378, 100, 500, 500)  # Same size as frame or adjusted
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load and set the image
        import os
        pixmap = QPixmap(os.path.abspath("Icons/faqs.png"))
        if pixmap.isNull():
            print("❌ Failed to load image: Icons/faqs.png")
        else:
            scaled_pixmap = pixmap.scaled(
                500, 500,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        self.questionlabel.raise_()
        self.secquestionlabel.raise_()