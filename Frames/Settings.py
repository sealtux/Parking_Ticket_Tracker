from PyQt6.QtWidgets import (
    QFrame, QLabel, QVBoxLayout, QTableWidget, QHeaderView,
    QAbstractItemView, QPushButton, QTableWidgetItem,QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap,QColor
import mysql.connector
from mysql.connector import Error
import os


class Transactionsframe(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        pointbreak = 50
     
        self.panel = QFrame(self)
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(0, 0, 1300, 850)
        self.panel.setStyleSheet("background-color: #F2F2E6;")

       
       

        self.secquestionlabel = QLabel("Accounts", self.panel)
        self.secquestionlabel.setGeometry(260, 320-pointbreak, 500, 20)
        self.secquestionlabel.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        # Image
        

        # Load and display image
        
        self.image_label = QLabel(self.panel)
        self.image_label.setGeometry(200, 150-pointbreak, 200, 200)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load and display image
        image_path = os.path.abspath("Icons/user.png")  # or change to faqs.jpg if needed
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
        else:
            scaled_pixmap = pixmap.scaled(
                100, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        # Bring text labels to front
        

        

        # version Load and display image
        self.label2 = QLabel("Version abouts", self.panel)
        self.label2.setGeometry(520, 320-pointbreak, 500, 20)
        self.label2.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        self.version = QLabel(self.panel)
        self.version.setGeometry(500, 150-pointbreak, 200, 200)
        self.version.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        # Load and display image
        image_pathversion = os.path.abspath("Icons/version.png")  # or change to faqs.jpg if needed
        pixmapver = QPixmap(image_pathversion)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
        else:
            scaled_pixmap = pixmapver.scaled(
                100, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.version.setPixmap(scaled_pixmap)

           
        
        self.label3 = QLabel("Language", self.panel)
        self.label3.setGeometry(855, 320-pointbreak, 500, 30)
        self.label3.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        self.language = QLabel(self.panel)
        self.language.setGeometry(800, 150-pointbreak, 200, 200)
        self.language.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        # Load and display image
        image_pathlanguage = os.path.abspath("Icons/language.png")  # or change to faqs.jpg if needed
        pixmaplang = QPixmap(image_pathlanguage)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
        else:
            scaled_pixmap = pixmaplang.scaled(
                100, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.language.setPixmap(scaled_pixmap)

        self.label4 = QLabel("Updates", self.panel)
        self.label4.setGeometry(870, 600-pointbreak, 500, 30)
        self.label4.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        self.refresh = QLabel(self.panel)
        self.refresh.setGeometry(810, 430-pointbreak, 200, 200)
        self.refresh.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        # Load and display image
        ref = os.path.abspath("Icons/reload.png")  # or change to faqs.jpg if needed
        pixmapupdate = QPixmap(ref)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
        else:
            scaled_pixmap = pixmapupdate.scaled(
                100, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.refresh.setPixmap(scaled_pixmap)
        

        self.label5 = QLabel("Themes", self.panel)
        self.label5.setGeometry(565, 600-pointbreak, 200, 30)
        self.label5.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        self.themes = QLabel(self.panel)
        self.themes.setGeometry(500, 430-pointbreak, 200, 200)
        self.themes.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        # Load and display image
        con = os.path.abspath("Icons/contrast.png")  # or change to faqs.jpg if needed
        pixmaptheme = QPixmap(con)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
        else:
            scaled_pixmap = pixmaptheme.scaled(
                100, 100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.themes.setPixmap(scaled_pixmap)




        self.label6 = QLabel("Connected Devices", self.panel)
        self.label6.setGeometry(255, 600-pointbreak, 100, 30)
        self.label6.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")

        self.network = QLabel(self.panel)
        self.network.setGeometry(250, 430-pointbreak, 100, 200)
        self.network.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        # Load and display image
        network = os.path.abspath("Icons/web.png")  # or change to faqs.jpg if needed
        pixmapnet = QPixmap(network)
        if pixmap.isNull():
            print(f"Failed to load image: {image_path}")
        else:
            scaled_pixmap = pixmapnet.scaled(
                120, 120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.network.setPixmap(scaled_pixmap)
        


        self.Settings = QLabel("Settings", self.panel)
        self.Settings.setGeometry(80,48, 200, 50)
        
        self.Settings.setStyleSheet("""QLabel{
                                    
        font-size: 30pt;
        color: black;
        background-color: transparent;
                                    }""")


        self.settingbar =  QFrame(self.panel)
        self.settingbar.setGeometry(0, 0, 1300, 120)
        self.settingbar.setStyleSheet("background-color: #D8D8D8;")
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setXOffset(1)
        shadow.setYOffset(1)
        shadow.setColor(QColor(0, 0, 0, 100))  # semi-transparent black

        self.settingbar.setGraphicsEffect(shadow)


        self.secquestionlabel.raise_()
        self.label2.raise_()
        self.label3.raise_()
        self.label4.raise_()
        self.label5.raise_()
        self.label6.raise_()
        self.Settings.raise_()
