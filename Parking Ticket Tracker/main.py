from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,QHeaderView
import sys

# Import from the subfolder
from second_ui.Addstudentevent import addstud  # required

from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from stud_table import student_table


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(550, 200, 800, 500)

        self.button = QPushButton("Add Student", self)
        self.button.setGeometry(20, 80, 60, 60)
        self.button.clicked.connect(self.openaddstudbutton)

        self.Addstudentevent = None #reference of the file

        #table
        self.table = student_table(self, headers=["ID number","First Name","Last Name" ,"Year Level","Gender","Program Code" ])
        self.table.setGeometry(160, 90, 602, 350)
        self.table.setRowHeight(100, 100)
        self.table.horizontalHeader().setFixedHeight(50)
   
   
    def openaddstudbutton(self):
        self.Addstudentevent = addstud()
        self.Addstudentevent.show()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
