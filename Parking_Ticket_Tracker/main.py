from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QVBoxLayout
import sys

# Import from the subfolder
from second_ui.Addstudentevent import addstud  # required

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from stud_table import student_table


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(400, 100, 600, 700)

        self.button = QPushButton("Add Student", self)
        self.button.setGeometry(20, 80, 60, 60)
        self.button.clicked.connect(self.openaddstudbutton)

        self.Addstudentevent = None  # reference of the file
        
       

        Vehicle = QFrame(self)
        Ticket = QFrame(self)
        ButtonFrame = QFrame(self)
        Vehicle.setGeometry(35, 160, 250, 250)  
        Ticket.setGeometry(320, 160, 250, 250)
        ButtonFrame.setGeometry(0, 600, 600, 200)
        
        #StyleSheets for button
        ButtonFrame.setStyleSheet("""
            QFrame{
                background-color: #FCFCFC;
                border: 1px solid #1E1E1E;
                
            }
                     
        """)
        Vehicle.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 15px;
                border: 1px solid #1E1E1E;
            }
        """)
        Ticket.setStyleSheet("""
                background-color: #FFFFFF;
                border-radius:15px;
                border: 1px solid #1E1E1E;
        """)


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
