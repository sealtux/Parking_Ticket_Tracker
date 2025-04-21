from PyQt6.QtWidgets import QWidget, QLabel,QLineEdit,QComboBox
from PyQt6.QtGui import QFont
from stud_table import student_table

class addstud(QWidget):
    def __init__(self):
        super().__init__()

        # Set the title here!
        self.setWindowTitle("Adding a Student")

        self.setGeometry(350, 200, 750, 500)
        


        #firstname
        self.firstname = QLineEdit(self)
        self.firstname.setGeometry(170,160,180,40)
        firstnamelabel= QLabel("First Name", self)
        firstnamelabel.move(180,140)
        font = QFont()
        font.setFamily('Arial')
        font.setWeight(QFont.Weight.Bold)
        font.setPointSize(12) 
        #font.setItalic(True)  
        firstnamelabel.setFont(font) 

        #lastname
        self.lastname = QLineEdit(self)
        self.lastname.setGeometry(360,160,180,40)
        lastnamelabel= QLabel("Last Name", self)
        lastnamelabel.move(370,140)
        font1 = QFont()
        font1.setFamily('Arial')
        font1.setWeight(QFont.Weight.Bold)
        font1.setPointSize(12) 
        #font.setItalic(True)  
        lastnamelabel.setFont(font1) 
        
        self.idnum = QLineEdit(self)
        self.idnum.setGeometry(550,160,180,40)
        idnumlabel = QLabel("ID Number",self)
        idnumlabel.move(560,140)
        font2 = QFont()
        font2.setFamily('Arial')
        font2.setWeight(QFont.Weight.Bold)
        font2.setPointSize(12)
        idnumlabel.setFont(font2)
        #yearlevel
        self.yearlevel =QComboBox(self)
        self.yearlevel.setGeometry(170,250,180,40)
        self.yearlevel.addItems([" ","1st Year","2nd Year","3rd Year", "4th Year"])
        yearlevellabel = QLabel("Year Level",self)
        yearlevellabel.move(180,230)
        font3 = QFont()
        font3.setFamily('Arial')
        font3.setWeight(QFont.Weight.Bold)
        font3.setPointSize(12)
        yearlevellabel.setFont(font3)

        self.Gender = QComboBox(self)
        self.Gender.setGeometry(360,250,180,40)
        self.Gender.addItems([" ","Male","Female"])

        #Program code
        self.Programcode = QComboBox(self)
        self.Programcode.setGeometry(550,250,180,40)