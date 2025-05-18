from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout,QTableWidget,QHeaderView,QAbstractItemView,QPushButton
from PyQt6.QtCore import Qt
class savecustom(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

     
        self.panel = QLabel(self)
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(0, 0, 1300, 850) #change the position
        self.panel.setStyleSheet("background-color: #F2F2E6;")  # apply color


        #table part{

        #adds a table
        self.table = QTableWidget(self)

        #row count
        self.table.setRowCount(10)  
        self.table.setColumnCount(5) 

        #sets the header text
        self.table.setHorizontalHeaderLabels(["Vehicle Type","Ticket ID", "Entry Time","Payment","Date"])

        #sets the scroll bar
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)


         #set size for the height for the row
        self.table.verticalHeader().setDefaultSectionSize(50)

        #set size for the width for row
        self.table.horizontalHeader().setFixedHeight(60)
        
        #sets the header size
        vh = self.table.verticalHeader()
        vh.setFixedWidth(50)
        
        #sets the header size
        self.table.verticalHeader().hide()

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(
        QHeaderView.ResizeMode.Stretch
        )

        #alternating row colors
        self.table.setAlternatingRowColors(True)

        #hides the line in the table
        self.table.setShowGrid(False)
         # Only one selection at a time
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        #Clicking selects an entire column
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)

        #unable editing to tbale
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)


        
        #sets the size of the table
        self.table.setGeometry(50, 100, 1180, 550)
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
#}
        