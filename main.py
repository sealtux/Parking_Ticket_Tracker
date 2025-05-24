from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QVBoxLayout, QAbstractItemView, QLabel, QToolButton, QStyle
import os,sys
from PyQt6.QtGui import QPalette, QColor,QFont,QPixmap, QIcon
from PyQt6.QtCore import QTimer, Qt, QSize
from PyQt6.QtGui import QMovie
import mysql.connector
from Table import MyCustomFrame
from Frames.Information import savecustom
from Frames.Settings import Transactionsframe

conn = None

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(0, 0, 1521, 1000) 

        self._init_bars()
        self._init_sidebar()
       
        
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window,QColor('#FFFFFF')) 
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # Panel sizing corrected to fit within the main window
        panel_x_offset = 248
        panel_y_offset = 78
        actual_panel_width = self.width() - panel_x_offset
        actual_panel_height = self.height() - panel_y_offset

        self.panel = QFrame(self) 
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(panel_x_offset, panel_y_offset, actual_panel_width, actual_panel_height) 
        self.panel.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.panel.setStyleSheet("background-color: #F2F2E6;")

        
        self._init_home_elements() 
        
       
        self.frame1 = MyCustomFrame(self)
        self.frame1.setGeometry(panel_x_offset, panel_y_offset, actual_panel_width, actual_panel_height)
       
        self.saveframe = savecustom(self)
        self.saveframe.setGeometry(panel_x_offset, panel_y_offset, actual_panel_width, actual_panel_height)

        self.trasactframe = Transactionsframe(self)
        self.trasactframe.setGeometry(panel_x_offset, panel_y_offset, actual_panel_width, actual_panel_height)

       
        self.show_home() 

    def _init_home_elements(self):
        CONTENT_PADDING = 30 
        panel_content_width = self.panel.width() - (2 * CONTENT_PADDING)
        panel_content_height = self.panel.height() - (2 * CONTENT_PADDING)
        detail_view_x = CONTENT_PADDING 
        detail_view_y = CONTENT_PADDING

        self.home_overview_widget = QFrame(self.panel)
        self.home_overview_widget.setGeometry(detail_view_x, detail_view_y, panel_content_width, panel_content_height)
       
        rect_w = 280  
        rect_h = 450 
    
        spacing = (panel_content_width - (3 * rect_w)) / 4
        button_y_pos = 100 
        
        icon_size = QSize(120, 120)

        # Rectangle 1: Vehicle Information
        self.vehicles_rect_button = QToolButton(self.home_overview_widget)
        self.vehicles_rect_button.setText("Total Vehicle")
        
        vehicle_icon_path = "Icons/total vehicle.png"
        if os.path.exists(vehicle_icon_path):
            vehicle_icon = QIcon(vehicle_icon_path)
            self.vehicles_rect_button.setIcon(vehicle_icon)

        self.vehicles_rect_button.setIconSize(icon_size)
        self.vehicles_rect_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.vehicles_rect_button.setGeometry(int(spacing), button_y_pos, rect_w, rect_h)
        self.vehicles_rect_button.setStyleSheet("""
            QToolButton {
                background-color: #A7C7E7; border: 1px solid #5D8AA8; border-radius: 15px;
                font: bold 18pt "Arial"; color: #183152; padding: 20px;
            }
            QToolButton:hover { background-color: #9ABBD9; }
        """)
        self.vehicles_rect_button.clicked.connect(self.show_vehicles_detail)







        # Rectangle 2: Payment Records
        self.payments_rect_button = QToolButton(self.home_overview_widget)
        self.payments_rect_button.setText("Payment Records")
        
        payment_icon_path = "Icons/payment.png"
        if os.path.exists(payment_icon_path):
            payment_icon = QIcon(payment_icon_path)
            self.payments_rect_button.setIcon(payment_icon)
        
        self.payments_rect_button.setIconSize(icon_size)
        self.payments_rect_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.payments_rect_button.setGeometry(int(spacing * 2 + rect_w), button_y_pos, rect_w, rect_h)
        self.payments_rect_button.setStyleSheet("""
            QToolButton {
                background-color: #C1E1C1; border: 1px solid #7BA05B; border-radius: 15px;
                font: bold 18pt "Arial"; color: #295218; padding: 20px;
            }
            QToolButton:hover { background-color: #B1D1B1; }
        """)
        self.payments_rect_button.clicked.connect(self.show_payments_detail)






        # Rectangle 3: Parking Space Info
        self.parking_rect_button = QToolButton(self.home_overview_widget)
        self.parking_rect_button.setText("Entry Register")

        parking_icon_path = "Icons/parking space.png"
        if os.path.exists(parking_icon_path):
            parking_icon = QIcon(parking_icon_path)
            self.parking_rect_button.setIcon(parking_icon)

        self.parking_rect_button.setIcon(parking_icon)
        self.parking_rect_button.setIconSize(icon_size)
        self.parking_rect_button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        self.parking_rect_button.setGeometry(int(spacing * 3 + rect_w * 2), button_y_pos, rect_w, rect_h)
        self.parking_rect_button.setStyleSheet("""
            QToolButton {
                background-color: #FFB3BA; border: 1px solid #A5676F; border-radius: 15px;
                font: bold 18pt "Arial"; color: #521820; padding: 20px;
            }
            QToolButton:hover { background-color: #EEA3AA; }
        """)
        self.parking_rect_button.clicked.connect(self.show_parking_detail)

        # Detail View 1: Vehicles
        self.vehicles_detail_view = QFrame(self.panel)
        self.vehicles_detail_view.setGeometry(detail_view_x, detail_view_y, panel_content_width, panel_content_height)
        global vehicles_table
        self.vehicles_table = QTableWidget(self.vehicles_detail_view)
        self.vehicles_table.setGeometry(50, 70, panel_content_width - 100, panel_content_height - 140)
        self.vehicles_table.setColumnCount(2)
        self.vehicles_table.setHorizontalHeaderLabels(["License Plate", "Type Of Vehicle"])
        self._style_home_table(self.vehicles_table)
        
        back_button_vehicles = QPushButton("Back", self.vehicles_detail_view)
        back_button_vehicles.setGeometry(50, 15, 100, 40)
        back_button_vehicles.clicked.connect(self.return_to_home_overview)
        self._style_back_button(back_button_vehicles)

        # Detail View 2: Payments
        self.payments_detail_view = QFrame(self.panel)
        self.payments_detail_view.setGeometry(detail_view_x, detail_view_y, panel_content_width, panel_content_height)

        self.payments_table = QTableWidget(self.payments_detail_view)
        self.payments_table.setGeometry(50, 70, panel_content_width - 100, panel_content_height - 140)
        self.payments_table.setColumnCount(3)
        self.payments_table.setHorizontalHeaderLabels(["Ticket ID", "Issued Date", "License Plate"])
        self._style_home_table(self.payments_table)















        back_button_payments = QPushButton("Back", self.payments_detail_view)
        back_button_payments.setGeometry(50, 15, 100, 40)
        back_button_payments.clicked.connect(self.return_to_home_overview)
        self._style_back_button(back_button_payments)










        # Detail View 3: Parking
        self.parking_detail_view = QFrame(self.panel)
        self.parking_detail_view.setGeometry(detail_view_x, detail_view_y, panel_content_width, panel_content_height)

        self.parking_table = QTableWidget(self.parking_detail_view)
        self.parking_table.setGeometry(50, 70, panel_content_width - 100, panel_content_height - 140)
        self.parking_table.setColumnCount(4)
        self.parking_table.setHorizontalHeaderLabels(["TicketID", "EntryTime", "License_Plate","Presence Status"])
        self._style_home_table(self.parking_table)

        back_button_parking = QPushButton("Back", self.parking_detail_view)
        back_button_parking.setGeometry(50, 15, 100, 40)
        back_button_parking.clicked.connect(self.return_to_home_overview)
        self._style_back_button(back_button_parking)

    def _style_home_table(self, table: QTableWidget):
        table.verticalHeader().setDefaultSectionSize(45) 
        table.horizontalHeader().setFixedHeight(55) 
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setAlternatingRowColors(True)
        table.setShowGrid(False)
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        table.verticalHeader().hide()
        table.setStyleSheet("""
            QTableWidget {
                background-color: #FFFFFF; 
                alternate-background-color: #F7F7F7;
                color: Black;
                border: 1px solid #D3D3D3;
                border-radius: 10px;
                font-size: 10pt;
            }
            QHeaderView::section {
                background-color: #E0E0E0; 
                color: Black;
                padding: 8px; 
                border: none;
                border-bottom: 1px solid #C0C0C0;
                font-size: 11pt; 
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #607D8B; 
                color: white;
            }
            QTableWidget::item {
                border-bottom: 1px solid #EAEAEA; 
                padding-left: 8px; 
            }
            QTableWidget QScrollBar:vertical {
                border: none;
                background: #F0F0F0;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }
            QTableWidget QScrollBar::handle:vertical {
                background: #C0C0C0;
                min-height: 20px;
                border-radius: 6px;
            }
            QTableWidget QScrollBar::add-line:vertical, QTableWidget QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QTableWidget QScrollBar::add-page:vertical, QTableWidget QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def _style_back_button(self, button: QPushButton):
        button.setStyleSheet("""
            QPushButton {
                font: bold 12pt "Arial"; color: white;
                background-color: #708090; /* Slate Gray */
                border: none; border-radius: 8px;
                padding: 8px 15px;
            }
            QPushButton:hover { background-color: #5A6875; } /* Darker Slate Gray */
        """)
     
    def show_home(self):
      self.panel.show() 
      self.home_overview_widget.show() 
      self.vehicles_detail_view.hide()
      self.payments_detail_view.hide()
      self.parking_detail_view.hide()
      self.frame1.hide()
      self.saveframe.hide()
      self.trasactframe.hide()
      print("show_home: Displaying home overview.")

    def return_to_home_overview(self):
        self.home_overview_widget.show()
        self.vehicles_detail_view.hide()
        self.payments_detail_view.hide()
        self.parking_detail_view.hide()
        print("Returned to home overview.")

    def show_vehicles_detail(self):
        self.home_overview_widget.hide()
        self.vehicles_detail_view.show()
        print("Displaying vehicles detail table.")
        self.loadvehicles()

    def show_payments_detail(self):
        self.home_overview_widget.hide()
        self.payments_detail_view.show()
        print("Displaying payments detail table.")
        self.loadtickets()

    def show_parking_detail(self):
        self.home_overview_widget.hide()
        self.parking_detail_view.show()
        print("Displaying parking detail table.")
        self.EntryLoad()
 
    def show_table(self):
        self.panel.hide() 
        self.home_overview_widget.hide() 
        self.vehicles_detail_view.hide()
        self.payments_detail_view.hide()
        self.parking_detail_view.hide()
        self.frame1.show() 
        self.saveframe.hide()
        self.trasactframe.hide()
        print("button clicked1: Displaying Tables frame")
       
    def show_saves(self):
        self.panel.hide()
        self.home_overview_widget.hide()
        self.vehicles_detail_view.hide()
        self.payments_detail_view.hide()
        self.parking_detail_view.hide()
        self.frame1.hide()
        self.saveframe.show() 
        self.trasactframe.hide()
        print("button clicked2: Displaying Saves frame")

    def show_transaction(self):
        self.panel.hide()
        self.home_overview_widget.hide()
        self.vehicles_detail_view.hide()
        self.payments_detail_view.hide()
        self.parking_detail_view.hide()
        self.frame1.hide()
        self.saveframe.hide()
        self.trasactframe.show() 
        print("button clicked3: Displaying Transactions frame")
    
    def _init_bars(self):
        self.dashboard = QFrame(self)
        self.dashboard.setGeometry(0, 0, 2000, 80)
        self.dashboard.setStyleSheet("QFrame { background-color: #21293D; }")
        self.cornerboard = QFrame(self)
        self.cornerboard.setGeometry(0, 0, 250, 1000)
        self.cornerboard.setStyleSheet("QFrame { background-color: #21293D; }")

    def _init_sidebar(self):
        logotext = QLabel(self)
        logotext.setText("Ticket Pad")
        logotext.setGeometry(100,-2,200,100)
        logoicon = QLabel(self)
        logoicon.setGeometry(0,0,110,100)
       
        logomap_path = "Icons/Logo.png"
        if os.path.exists(logomap_path):
            logomap = QPixmap(logomap_path)
            logoicon.setPixmap(logomap)
        logoicon.setScaledContents(True)
        
        button = QPushButton("Home", self)
        button.setGeometry(0, 95, 250, 35)
        button.clicked.connect(self.show_home)
        Homeicon = QLabel(self)
        Homeicon.setGeometry(40,100,25,20)
        
        home_icon_path = "Icons/Home.png"
        if os.path.exists(home_icon_path):
            pixmap = QPixmap(home_icon_path)
            Homeicon.setPixmap(pixmap)
        Homeicon.setScaledContents(True)

        Tablebutton = QPushButton("Tables",self.cornerboard) #this adds a button to the table page
        Tablebutton.setGeometry(0,170,250,35)
        Tablebutton.clicked.connect(self.show_table)#this adds a function to a button when being clicked
        #> table icon
        Tableicon = QLabel(self)
        Tableicon.setGeometry(40,176,25,20)
        tableiconmap = QPixmap("Icons/table.png")
        Tableicon.setPixmap(tableiconmap)
        Tableicon.setScaledContents(True)
        
        Savebutton = QPushButton("Moderator",self.cornerboard)
        Savebutton.setGeometry(0,240,250,35)
        Savebutton.clicked.connect(self.show_saves)
        saveicon = QLabel(self)
        saveicon.setGeometry(40,245,25,20)
        saveiconmap = QPixmap("Icons/Information.png")
        saveicon.setPixmap(saveiconmap)
        saveicon.setScaledContents(True)

        Transaction = QPushButton("Settings",self.cornerboard)
        Transaction.setGeometry(0,310,250,35)
        Transaction.clicked.connect(self.show_transaction)
        transactionicon = QLabel(self)
        transactionicon.setGeometry(40,315,25,20)
        transactionmap = QPixmap("Icons/Settings.png")
        transactionicon.setPixmap(transactionmap)
        transactionicon.setScaledContents(True)


        button.setStyleSheet("""
        QPushButton {
            font-family: "Neuton"; font-size: 14pt; color: #6D6B6B;
            background: transparent; border: none; text-align: left; padding-left: 70px;
        }
        QPushButton:hover { color: #FFFFFF; }""")

        Transaction.setStyleSheet("""
        QPushButton {
            font-family: "Neuton"; font-size: 14pt; color: #6D6B6B;
            background: transparent; border: none; text-align: left; padding-left: 70px;
        }
        QPushButton:hover { color: #FFFFFF; }""")
        
        Tablebutton.setStyleSheet("""
        QPushButton {
            font-family: "Neuton"; font-size: 14pt; color: #6D6B6B;
            background: transparent; border: none; text-align: left; padding-left: 70px;
        }
        QPushButton:hover { color: #FFFFFF; }""")

        Savebutton.setStyleSheet("""
        QPushButton {
            font-family: "Neuton"; font-size: 14pt; color: #6D6B6B;
            background: transparent; border: none; text-align: left; padding-left: 70px;
        }
        QPushButton:hover { color: #FFFFFF; }""")

        logotext.setStyleSheet("""
        QLabel{
        font-family: "Kavoon"; font-size: 20pt; color: #FFFFFF;                     
        }""")
    

    def loadvehicles(self):
        
        print("clicked")
        
        try:
            # Step 1: Connect to MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="parkindgticketdb"
            )
            cursor = conn.cursor()

            # Step 2: Execute SELECT query
            cursor.execute("SELECT License_Plate, TypeOfVehicle FROM vehicle")
            results = cursor.fetchall()

            # Step 3: Configure the table
            self.vehicles_table.setColumnCount(2)
            self.vehicles_table.setHorizontalHeaderLabels(["License Plate", "Type Of Vehicle"])
            self.vehicles_table.setRowCount(len(results))

            # Step 4: Populate the table
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.vehicles_table.setItem(row_idx, col_idx, item)

            # Cleanup
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error loading data:", err)
       


    def loadtickets(self):
        try:
            # Step 1: Connect to MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="parkindgticketdb"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT TicketID, IssuedDate,License_Plate FROM ticket")
            results = cursor.fetchall()

            # Step 3: Configure the table
            self.payments_table.setColumnCount(3)
            self.payments_table.setHorizontalHeaderLabels(["Ticket ID", "Issued Date", "License Plate"])
            self.payments_table.setRowCount(len(results))

            # Step 4: Populate the table
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.payments_table.setItem(row_idx, col_idx, item)

            # Cleanup
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error loading data:", err)


    def EntryLoad(self):
        print("clicked")
        try:
            # Step 1: Connect to MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="parkindgticketdb"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT TicketID, EntryTime,License_Plate,PresenceStatus FROM acquires")
            results = cursor.fetchall()

            # Step 3: Configure the table
            self.parking_table.setColumnCount(4)
            self.parking_table.setHorizontalHeaderLabels(["Ticket ID", "EntryTime", "License_Plate","PresenceStatus"])
            self.parking_table.setRowCount(len(results))

            # Step 4: Populate the table
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    item = QTableWidgetItem(str(col_data))
                    self.parking_table.setItem(row_idx, col_idx, item)

            # Cleanup
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error loading data:", err)


if __name__ == "__main__":
    
        app = QApplication(sys.argv)
        if not os.path.exists("Icons"):
            os.makedirs("Icons")
            print("Created 'Icons' directory. Please place your icon files there.")
        window = MainWindow()
        window.show()
       
        sys.exit(app.exec())
   
