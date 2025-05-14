from PyQt6.QtWidgets import (
    QApplication, QWidget, QFrame,
    QTableWidget, QTableWidgetItem,QLabel,QHeaderView,QGraphicsDropShadowEffect,QScrollArea
)
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor
import sys

class MyCustomFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.panel = QLabel(self)
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(0, 00, 1300, 850)
        self.panel.setStyleSheet("background-color: #F2F2E6;")  # apply color
        

        # Apply a white background
        
        self.table = QTableWidget(self)
        #row count
        self.table.setRowCount(3)  
        self.table.setColumnCount(3) 
        #sets the header text
        self.table.setHorizontalHeaderLabels(["Ticket ID", "Entry Time","Payment"])
        shadow = QGraphicsDropShadowEffect(self)

        #sets the shadow{
        shadow.setBlurRadius(20)
        shadow.setXOffset(5)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 100))  # semi-transparent black

        self.table.setGraphicsEffect(shadow)
        
        #}

        #sets the scrollbar for the table
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


         #set size for the height for the incrementer
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
       
        #adding text columns
        self.table.setItem(0, 0, QTableWidgetItem("Row 1, Column 1"))
        self.table.setItem(0, 1, QTableWidgetItem("Row 1, Column 2"))
        self.table.setItem(1, 0, QTableWidgetItem("Row 2, Column 1"))

       
        
        # 1) Turn on alternating rows…
        self.table.setAlternatingRowColors(True)

        #hides the line in the table
        self.table.setShowGrid(False)

# 2) Define your two colors via stylesheet (or via palette)
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
    
""")    
        #hides the incrementer on the left
        self.table.verticalHeader().hide()
        
        
        #sets the size of the table
        self.table.setGeometry(50, 100, 1180, 550)
