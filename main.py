from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QVBoxLayout
import os,sys

# Import from the subfolder
from second_ui.Addstudentevent import addstud  # required

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QGraphicsDropShadowEffect,QLabel
from stud_table import student_table
from PyQt6.QtGui import QPalette, QColor,QFont,QPixmap


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(0, 0, 1521, 1000) #window's size

        button = QPushButton("Menu", self)# this adds a button for the menu
        button.setGeometry(0, 95, 250, 35)
        button.clicked.connect(self.openaddstudbutton)
        
        #icons for the button
        #>the menu icon
        menuicon = QLabel(self)
        menuicon.setGeometry(40,100,25,20)
        pixmap = QPixmap("Menu.png")
        menuicon.setPixmap(pixmap)
        menuicon.setScaledContents(True)
        
      

        self.Addstudentevent = None  # reference of the file
        
       #background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window,QColor('#FFFFFF'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)



       





        dashboard = QFrame(self)
        cornerboard = QFrame(self)
        
        dashboard.setGeometry(0, 0, 2000, 80) # this adds a frame on top of the screen

        cornerboard.setGeometry(0, 0, 250, 1000)# this adds a frame on the left side of the screen
        

        
        #StyleSheets for Frame
        #boarder-radius:15px; this is used to add corners on your frame
        dashboard.setStyleSheet("""
            QFrame {
                background-color: #21293D;
                
                
            }
        """)
        #StyleSheets for Frame
        cornerboard.setStyleSheet("""
            QFrame{
            background-color: #21293D;
            
            background-position: 20px 30px;
            }
        """)
        
        #Made the button transparent and added a hover 
        button.setStyleSheet("""
        QPushButton {
            font-family: "Neuton";
            font-size: 14pt;
            color: #6D6B6B;
            background: transparent;
            border: none;
        }
        QPushButton:hover {
            color: #FFFFFF;
        }
        """)

        
        dashboard.raise_()
        button.raise_()
        menuicon.raise_()

        # table
        # self.table = student_table(self, headers=["ID number","First Name","Last Name" ,"Year Level","Gender","Program Code"])
        # self.table.setGeometry(160, 90, 602, 350)
        # self.table.setRowHeight(100, 100)
        # self.table.horizontalHeader().setFixedHeight(50)
   
         # this adds the frame to the layout

    def openaddstudbutton(self):
        self.Addstudentevent = addstud()
        self.Addstudentevent.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
