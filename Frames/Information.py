from PyQt6.QtWidgets import (
    QFrame, QLabel, QVBoxLayout, QTableWidget, QHeaderView,
    QAbstractItemView, QPushButton, QTableWidgetItem,QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap,QColor
import mysql.connector
from mysql.connector import Error
import os

table = None

class savecustom(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Use QFrame for the panel
        self.panel = QFrame(self)
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(0, 0, 1300, 850)
        self.panel.setStyleSheet("background-color: #F2F2E6;")

        # Header labels
        self.questionlabel = QLabel("Do You Have Questions?", self.panel)
        self.questionlabel.setGeometry(580, 50, 1000, 70)
        self.questionlabel.setStyleSheet("font-size: 40px; font-weight: bold; color: #333;")

        self.secquestionlabel = QLabel("We have answers (well, most of the times)", self.panel)
        self.secquestionlabel.setGeometry(538+80, 120, 1000, 70)
        self.secquestionlabel.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        # Image
        self.image_label = QLabel(self.panel)
        self.image_label.setGeometry(568, 150, 500, 500)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load and display image
        image_path = os.path.abspath("Icons/faqs.png")  # or change to faqs.jpg if needed
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
        else:
            scaled_pixmap = pixmap.scaled(
                500, 500,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

        # Bring text labels to front
        self.questionlabel.raise_()
        self.secquestionlabel.raise_()

      
        self.choice1 = QFrame(self.panel)
        self.choice1.setGeometry(0, 300, 350, 60)
        self.information1 = QLabel("What is this app for?", self.choice1)
        self.information1.setGeometry(0, 0, 300, 50)
        
        self.information1.setStyleSheet("""
    QLabel {
        font-size: 14pt;
        color: black;
    }
""")    
        self.choice1button = QPushButton( self)
        self.choice1button.setGeometry(0, 300, 350, 60)   
        self.choice1button.setStyleSheet("QPushButton { background-color: Transparent; border: none;}")
        self.choice1button.clicked.connect(self.openfaqs)

        self.frame1 = QFrame(self.panel)
        self.frame1.setGeometry(0, 0, 500, 180)
        self.frame1.setStyleSheet("QFrame { background-color: #FFFFFF; border: none;}")
        self.framelabel1 = QLabel(
    "How to use the application?\n\n"
    "The Parking Ticket Management Application is designed to \nhelp users efficiently organize,"
    "update, and monitor parking \n tickets within a secure and user-friendly interface.",
    self.frame1
)
        self.framelabel1.setStyleSheet("""
    QLabel {
        font-size: 14pt;
        color: black;
    }
""")    
        self.frame1button = QPushButton("Back",self.frame1)
        self.frame1button.setGeometry(380, 140, 100, 30)
        self.frame1button.setStyleSheet("QPushButton { background-color: #D8D8D8; border: none;}")
        self.frame1button.clicked.connect(self.on_cancel)
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(2)
        shadow2.setOffset(2, 2)  # Slight vertical shadow
        shadow2.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black
        self.frame1.setGraphicsEffect(shadow2)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(2)
        shadow.setOffset(0.0, 2.0)  # Slight vertical shadow
        shadow.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black

        self.choice1.setGraphicsEffect(shadow)



        self.choice2 = QFrame(self.panel)
        self.choice2.setGeometry(0, 370, 350, 60)
        self.information2 = QLabel("How to switch to Moderator mode?", self.choice2)
        self.information2.setGeometry(0, 0, 300, 50)

        self.choice2button = QPushButton( self)
        self.choice2button.setGeometry(0, 370, 350, 60)   
        self.choice2button.setStyleSheet("QPushButton { background-color: Transparent; border: none;}")
        self.choice2button.clicked.connect(self.openfaqs2)


        self.information2.setStyleSheet("""
    QLabel {
        font-size: 14pt;
        color: black;
    }
""")    
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(2)
        shadow2.setOffset(0.0, 2.0)  # Slight vertical shadow
        shadow2.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black

        self.choice2.setGraphicsEffect(shadow2)


        self.choice3 = QFrame(self.panel)
        self.choice3.setGeometry(0, 440, 350, 60)
        self.information3 = QLabel("What does shift do?", self.choice3)
        self.information3.setGeometry(0, 0, 300, 50)

        self.choice3button = QPushButton( self)
        self.choice3button.setGeometry(0, 440, 350, 60)   
        self.choice3button.setStyleSheet("QPushButton { background-color: Transparent; border: none;}")
        self.choice3button.clicked.connect(self.openfaqs3)

        self.information3.setStyleSheet("""
    QLabel {
        font-size: 14pt;
        color: black;
    }
""")    
        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(2)
        shadow3.setOffset(0.0, 2.0)  # Slight vertical shadow
        shadow3.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black

        self.choice3.setGraphicsEffect(shadow3)
        self.frame1.hide()
        self.frame1.raise_()
        


    def openfaqs(self):
        self.frame1.show()
        print("hello")

    def openfaqs2(self):
        print("Opening FAQs for Moderator mode...")

    def openfaqs3(self):
        print("Opening FAQs for shift...")

    def on_cancel(self):
    # hide the add‑frame
        self.frame1.hide()
    # re‑enable the Add button
        