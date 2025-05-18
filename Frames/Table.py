from PyQt6.QtWidgets import (
    QApplication, QWidget, QFrame,
    QTableWidget, QTableWidgetItem,QLabel,QHeaderView,QGraphicsDropShadowEffect,QScrollArea,QPushButton, QLineEdit,QAbstractItemView
)
from PyQt6.QtCore import Qt, QRect, QSize
from PyQt6.QtGui import QColor,QPixmap,QIcon
import sys

class MyCustomFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        #initialization{
        self.panel = QLabel(self)
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(0, 0, 1300, 850) #change the position
        self.panel.setStyleSheet("background-color: #F2F2E6;")  # apply color
        

        #add button
        self.addbutton = QPushButton(" Add new", self.panel)
        self.addbutton.setGeometry(1000, 30, 120, 45)  # Adjust width for text + icon
        self.addbutton.clicked.connect(self.add_new)
        # Sets the add icon
        icon = QIcon("Icons/Add.png")
        self.addbutton.setIcon(icon)
        self.addbutton.setIconSize(QSize(14, 14))  # Adjust icon size as needed

        #search bar
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search...")
        self.search_bar.setGeometry(680, 30, 300, 45)
        

        self.deletebutton = QPushButton(" Delete", self.panel)
        self.deletebutton.setGeometry(200,30,100,45)
        self.deletebutton.clicked.connect(self.remove_val)
        #sets the remove icon
        removeicon = QIcon("Icons/Remove.png")
        self.deletebutton.setIcon(removeicon)
        self.deletebutton.setIconSize(QSize(14, 14))
        
        #sets the remove icon
        self.savebutton = QPushButton(" Save", self.panel)
        self.savebutton.setGeometry(50,30,100,45)
        self.savebutton.clicked.connect(self.save_value)
        #sets the remove icon
        saveicon = QIcon("Icons/import.png")
        self.savebutton.setIcon(saveicon)
        self.savebutton.setIconSize(QSize(14, 14))

        # Apply a white background
        self.table = QTableWidget(self)
        


        #}





        #row count
        self.table.setRowCount(10)  
        self.table.setColumnCount(5) 
        #sets the header text
        self.table.setHorizontalHeaderLabels(["Vehicle Type","Ticket ID", "Entry Time","Payment","Date"])
       

        #sets the shadow{
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setXOffset(1)
        shadow.setYOffset(1)
        shadow.setColor(QColor(0, 0, 0, 100))  # semi-transparent black

        self.table.setGraphicsEffect(shadow)
        
        

        #sets the scrollbar for the table
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


         #set size for the height for the row
        self.table.verticalHeader().setDefaultSectionSize(50)

        #set size for the width for row
        self.table.horizontalHeader().setFixedHeight(60)
        
        #sets the header size
        vh = self.table.verticalHeader()
        vh.setFixedWidth(50)
        
        #fill the whole frame
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch

)       
       
       
        # Only one selection at a time
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        #Clicking selects an entire column
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        #unable editing to tbale
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        #adding text columns
        self.table.setItem(0, 0, QTableWidgetItem("Row 1, Column 1"))
        self.table.setItem(0, 1, QTableWidgetItem("Row 1, Column 2"))
        self.table.setItem(1, 1, QTableWidgetItem("Row 2, Column 1"))
        self.table.setItem(2, 0, QTableWidgetItem("Row 3, Column 1"))
        self.table.setItem(2, 2, QTableWidgetItem("Row 3, Column 3"))
        self.table.setItem(3, 0, QTableWidgetItem("Row 4, Column 1"))
        self.table.setItem(4, 0, QTableWidgetItem("Row 5, Column 2"))
        

       
        
        # Turn on alternating rows…
        self.table.setAlternatingRowColors(True)

        #hides the line in the table
        self.table.setShowGrid(False)

        # Define your two colors via stylesheet (or via palette)
        self.table.setStyleSheet("""
    QTableWidget {
        background-color: #E8E7DD;            /* rows with even index (0,2,4…) */
        alternate-background-color: #F4F4ED;  /* rows with odd index (1,3,5…) */
        color: Black;
        border: none;
        border-radius: 15px;
         /* text color on black background */
    }
    QHeaderView::section {
        background-color: #F4F4ED;
        color: Black;
                                 border: none;
    }
    QTableWidget {
        border: none;
    }
        QTableWidget::item:selected {
        background-color: #464646;  /* Highlight background */
        color: black;              /* Highlight text color */
    }
   
    QTableWidget::item:focus {
    background-color: transparent;
    outline: none;              /* remove dotted outline */
}
                                 
    /* Remove the focus rectangle for any item */
QTableWidget::item {
    outline: none;         /* drop the dotted focus outline */
    border: none;          /* drop any cell border on focus */
}


QTableWidget::item:focus {
    outline: none;
    border: none;
}
   
    
""")    
        self.deletebutton.setStyleSheet("""
  QPushButton {
            font-family: "Neuton";
            font-size: 14pt;
            border-radius: 5px;
            background-color: #B35047;
            border: none;
            color:white
        }
        QPushButton:hover {
            background-color: #7D2E26;
            
        }




""")
        self.savebutton.setStyleSheet("""
  QPushButton {
            font-family: "Neuton";
            font-size: 10pt;
            border-radius: 5px;
            background-color: white;
            border: none;
            color:black
        }
        QPushButton:hover {
            background-color: #767575;
            
        }




""")

        #edits for the addbutton
        self.addbutton.setStyleSheet("""
        
        QPushButton {
            font-family: "Neuton";
            font-size: 14pt;
            border-radius: 5px;
            background-color: #313B69;
            border: none;
            color:white
        }
        QPushButton:hover {
            background-color: #1F2645;
            
        }
        """)
        self.search_bar.setStyleSheet("""
    QLineEdit {
        padding: 5px;
        font-size: 14pt;
        color: black;
        border-radius: 5px;
        background-color: white;
    }
""")
        
        #hides the incrementer on the left
        self.table.verticalHeader().hide()
        
        
        #sets the size of the table
        self.table.setGeometry(50, 100, 1180, 550)

    def add_new(self):
        print("clicked")
        self.table.clearSelection()#clears the cell
            # start with zero rows
        
            ##this is for the backend when adding value to the table
        #self.table.setRowCount(0)
     #   idx = self.table.rowCount()
      #  self.table.insertRow(idx)
       # for col, value in enumerate(data):
        #    self.table.setItem(idx, col, QTableWidgetItem(value))

    

    def remove_val(self):
        print("clicked")
        self.table.clearSelection()#clears the cell


    
        

    def save_value(self):
        self.table.clearSelection()#clears the cell
        print("clicked")
