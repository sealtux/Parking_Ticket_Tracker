from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QVBoxLayout
import os,sys

# Import from the subfolder



from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QGraphicsDropShadowEffect,QLabel

from PyQt6.QtGui import QPalette, QColor,QFont,QPixmap

from PyQt6.QtCore import QTimer
from PyQt6.QtCore import Qt,QSize

from PyQt6.QtGui import QMovie

from Frames.Table import MyCustomFrame
from Frames.saves import savecustom
from Frames.transaction import Transactionsframe


class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(0, 0, 1521, 1000) #window's size

        self._init_bars()
        self._init_sidebar()
       
       
          #background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window,QColor('#FFFFFF'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        self.panel = QLabel(self)
        
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(248, 78, 1500, 900)
        self.panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.panel.setStyleSheet("background-color: white;")


        #table frame
        self.frame1 = MyCustomFrame(self)
        self.frame1.setGeometry(248, 78, 1500, 900)
       

        #saves frame
        self.saveframe = savecustom(self)
        self.saveframe.setGeometry(248, 78, 1500, 900)


        self.trasactframe = Transactionsframe(self)
        self.trasactframe.setGeometry(248, 78, 1500, 900)

        #default hide
        self.panel.show()
        self.frame1.hide()
        self.saveframe.hide()
        self.trasactframe.hide()




    
     


    def show_home(self):
      self.frame1.hide()
      self.panel.show()
      self.saveframe.hide()
      self.trasactframe.hide()
      print("button clicked")
    


    #insert the table frame here 
    def show_table(self):
        self.panel.hide()
        self.frame1.show()
        self.saveframe.hide()
        self.trasactframe.hide()
        print("button clicked1")
       


    def show_saves(self):
        self.panel.hide()
        self.frame1.hide()
        self.saveframe.show()
        self.trasactframe.hide()
        print("button clicked2")


    def show_transaction(self):
        self.panel.hide()
        self.panel.hide()
        self.frame1.hide()
        self.saveframe.hide()
        self.trasactframe.show()
        print("button clicked3")
    
    


    



    def _init_bars(self):
        self.dashboard = QFrame(self)
        self.dashboard.setGeometry(0, 0, 2000, 80)
        self.dashboard.setStyleSheet("QFrame { background-color: #21293D; }")
        self.cornerboard = QFrame(self)
        self.cornerboard.setGeometry(0, 0, 250, 1000)
        self.cornerboard.setStyleSheet("QFrame { background-color: #21293D; }")

        


        


    def _init_sidebar(self):

        #sets the logo
        logotext = QLabel(self)
        logotext.setText("Ticket Pad")
        logotext.setGeometry(100,-2,200,100)
        logoicon = QLabel(self)
        logoicon.setGeometry(0,0,110,100)
        logomap = QPixmap("Icons/Logo.png")
        logoicon.setPixmap(logomap)
        logoicon.setScaledContents(True)
        


        # Home button

        button = QPushButton("Home", self)# this adds a button to the home page
        button.setGeometry(0, 95, 250, 35)
        button.clicked.connect(self.show_home)
        #> Home icon
        Homeicon = QLabel(self)
        Homeicon.setGeometry(40,100,25,20)
        pixmap = QPixmap("Icons/Home.png")
        Homeicon.setPixmap(pixmap)
        Homeicon.setScaledContents(True)


        # Tables button

        Tablebutton = QPushButton("Tables",self.cornerboard) #this adds a button to the table page
        Tablebutton.setGeometry(0,170,250,35)
        Tablebutton.clicked.connect(self.show_table)#this adds a function to a button when being clicked
        #> table icon
        Tableicon = QLabel(self)
        Tableicon.setGeometry(40,176,25,20)
        tableiconmap = QPixmap("Icons/Table.png")
        Tableicon.setPixmap(tableiconmap)
        Tableicon.setScaledContents(True)
        


        #Save button

        Savebutton = QPushButton("Saves",self.cornerboard)
        Savebutton.setGeometry(0,240,250,35)
        Savebutton.clicked.connect(self.show_saves)
        #> save icon
        saveicon = QLabel(self)
        saveicon.setGeometry(40,245,25,20)
        saveiconmap = QPixmap("Icons/Saves.png")
        saveicon.setPixmap(saveiconmap)
        saveicon.setScaledContents(True)


        #Transaction button

        Transaction = QPushButton("        Transactions",self.cornerboard)
        Transaction.setGeometry(0,310,250,35)
        Transaction.clicked.connect(self.show_transaction)
        #> transaction
        transactionicon = QLabel(self)
        transactionicon.setGeometry(40,315,25,20)
        transactionmap = QPixmap("Icons/Money.png")
        transactionicon.setPixmap(transactionmap)
        transactionicon.setScaledContents(True)


        
        





        # this is for the style for the home button  
        #StyleSheets for Frame
        #boarder-radius:15px; this is used to add corners on your frame
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

        Transaction.setStyleSheet("""
        
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
        
        Tablebutton.setStyleSheet("""
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
        Savebutton.setStyleSheet("""
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

        logotext.setStyleSheet("""
        QLabel{
        font-family: "Kavoon";
        font-size: 20pt;
        color: #FFFFFF;                     
}
 """)



   
     
       
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
