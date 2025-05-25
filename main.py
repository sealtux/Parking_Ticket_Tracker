from PyQt6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QFrame, QVBoxLayout, QAbstractItemView, QLabel, QToolButton, QStyle,
    QMenu
)
import os,sys
from PyQt6.QtGui import QPalette, QColor,QFont,QPixmap, QIcon, QAction
from PyQt6.QtCore import QTimer, Qt, QSize, QPoint
from PyQt6.QtGui import QMovie
import mysql.connector
from Table import MyCustomFrame # MyCustomFrame is not directly used for styling here, but Table.py's stylesheet is.
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

        # Initialize sort information dictionaries for dropdown menu logic
        self.vehicles_sort_info = {'col': -1, 'order': Qt.SortOrder.AscendingOrder}
        self.payments_sort_info = {'col': -1, 'order': Qt.SortOrder.AscendingOrder}
        self.parking_sort_info  = {'col': -1, 'order': Qt.SortOrder.AscendingOrder}
       
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
            self.vehicles_rect_button.setIcon(QIcon(vehicle_icon_path))
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
            self.payments_rect_button.setIcon(QIcon(payment_icon_path))
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
            self.parking_rect_button.setIcon(QIcon(parking_icon_path))
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

        # --- Detail View 1: Vehicles ---
        self.vehicles_detail_view = QFrame(self.panel)
        self.vehicles_detail_view.setGeometry(detail_view_x, detail_view_y, panel_content_width, panel_content_height)
        back_button_vehicles = QPushButton("Back", self.vehicles_detail_view)
        back_button_vehicles.setGeometry(50, 15, 100, 40)
        back_button_vehicles.clicked.connect(self.return_to_home_overview)
        self._style_back_button(back_button_vehicles)
        self.vehicles_search_bar = QLineEdit(self.vehicles_detail_view)
        self.vehicles_search_bar.setPlaceholderText("Search Vehicles...")
        self.vehicles_search_bar.setGeometry(160, 15, panel_content_width - 320, 40) 
        self._style_search_bar(self.vehicles_search_bar)
        self.vehicles_search_bar.textChanged.connect(
            lambda: self._filter_table_content(self.vehicles_search_bar, self.vehicles_table)
        )
        self.vehicles_sort_button = QPushButton(self.vehicles_detail_view)
        self.vehicles_sort_button.setIcon(QIcon("Icons/sort.png")) 
        self.vehicles_sort_button.setIconSize(QSize(20, 20))
        self.vehicles_sort_button.setGeometry(panel_content_width - 100 - 50 , 15, 40, 40) 
        self._style_sort_button(self.vehicles_sort_button)
        self.vehicles_sort_button.clicked.connect(
            lambda: self._show_sort_menu(self.vehicles_sort_button, self.vehicles_table, self.vehicles_sort_info)
        )
        self.vehicles_table = QTableWidget(self.vehicles_detail_view)
        self.vehicles_table.setGeometry(50, 70, panel_content_width - 100, panel_content_height - 140)
        self.vehicles_table.setColumnCount(2)
        self.vehicles_table.setHorizontalHeaderLabels(["License Plate", "Type Of Vehicle"])
        self._style_home_table(self.vehicles_table)
        self.vehicles_table.setSortingEnabled(True)

        # --- Detail View 2: Payments ---
        self.payments_detail_view = QFrame(self.panel)
        self.payments_detail_view.setGeometry(detail_view_x, detail_view_y, panel_content_width, panel_content_height)
        back_button_payments = QPushButton("Back", self.payments_detail_view)
        back_button_payments.setGeometry(50, 15, 100, 40)
        back_button_payments.clicked.connect(self.return_to_home_overview)
        self._style_back_button(back_button_payments)
        self.payments_search_bar = QLineEdit(self.payments_detail_view)
        self.payments_search_bar.setPlaceholderText("Search Payments...")
        self.payments_search_bar.setGeometry(160, 15, panel_content_width - 320, 40)
        self._style_search_bar(self.payments_search_bar)
        self.payments_search_bar.textChanged.connect(
            lambda: self._filter_table_content(self.payments_search_bar, self.payments_table)
        )
        self.payments_sort_button = QPushButton(self.payments_detail_view)
        self.payments_sort_button.setIcon(QIcon("Icons/sort.png"))
        self.payments_sort_button.setIconSize(QSize(20, 20))
        self.payments_sort_button.setGeometry(panel_content_width - 100 - 50, 15, 40, 40)
        self._style_sort_button(self.payments_sort_button)
        self.payments_sort_button.clicked.connect(
            lambda: self._show_sort_menu(self.payments_sort_button, self.payments_table, self.payments_sort_info)
        )
        self.payments_table = QTableWidget(self.payments_detail_view)
        self.payments_table.setGeometry(50, 70, panel_content_width - 100, panel_content_height - 140)
        self.payments_table.setColumnCount(3)
        self.payments_table.setHorizontalHeaderLabels(["Ticket ID", "Issued Date", "License Plate"])
        self._style_home_table(self.payments_table)
        self.payments_table.setSortingEnabled(True)

        # --- Detail View 3: Parking (Entry Register) ---
        self.parking_detail_view = QFrame(self.panel)
        self.parking_detail_view.setGeometry(detail_view_x, detail_view_y, panel_content_width, panel_content_height)
        back_button_parking = QPushButton("Back", self.parking_detail_view)
        back_button_parking.setGeometry(50, 15, 100, 40)
        back_button_parking.clicked.connect(self.return_to_home_overview)
        self._style_back_button(back_button_parking)
        self.parking_search_bar = QLineEdit(self.parking_detail_view)
        self.parking_search_bar.setPlaceholderText("Search Entries...")
        self.parking_search_bar.setGeometry(160, 15, panel_content_width - 320, 40)
        self._style_search_bar(self.parking_search_bar)
        self.parking_search_bar.textChanged.connect(
            lambda: self._filter_table_content(self.parking_search_bar, self.parking_table)
        )
        self.parking_sort_button = QPushButton(self.parking_detail_view)
        self.parking_sort_button.setIcon(QIcon("Icons/sort.png"))
        self.parking_sort_button.setIconSize(QSize(20, 20))
        self.parking_sort_button.setGeometry(panel_content_width - 100 - 50, 15, 40, 40)
        self._style_sort_button(self.parking_sort_button)
        self.parking_sort_button.clicked.connect(
            lambda: self._show_sort_menu(self.parking_sort_button, self.parking_table, self.parking_sort_info)
        )
        self.parking_table = QTableWidget(self.parking_detail_view)
        self.parking_table.setGeometry(50, 70, panel_content_width - 100, panel_content_height - 140)
        self.parking_table.setColumnCount(4)
        self.parking_table.setHorizontalHeaderLabels(["TicketID", "EntryTime", "License_Plate","Presence Status"])
        self._style_home_table(self.parking_table)
        self.parking_table.setSortingEnabled(True)

    def _style_search_bar(self, search_bar: QLineEdit):
        search_bar.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                font-size: 11pt;
                color: black;
                border: 1px solid #B0B0B0;
                border-radius: 8px;
                background-color: white;
            }
        """)

    def _style_sort_button(self, button: QPushButton):
        button.setToolTip("Sort by column")
        button.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0; 
                border: 1px solid #C0C0C0; 
                border-radius: 8px;
                padding: 5px;
            }
            QPushButton:hover { background-color: #D0D0D0; }
            QPushButton:pressed { background-color: #C0C0C0; }
        """)

    def _filter_table_content(self, search_bar: QLineEdit, table_widget: QTableWidget):
        search_text = search_bar.text().lower().strip()
        for i in range(table_widget.rowCount()):
            if not search_text: 
                table_widget.setRowHidden(i, False)
                continue
            match_found = False
            for j in range(table_widget.columnCount()):
                item = table_widget.item(i, j)
                if item and search_text in item.text().lower():
                    match_found = True
                    break
            table_widget.setRowHidden(i, not match_found)

    def _show_sort_menu(self, button: QPushButton, table_widget: QTableWidget, sort_info_dict: dict):
        menu = QMenu(self)
        header = table_widget.horizontalHeader()
        for col_idx in range(header.count()):
            header_text = table_widget.horizontalHeaderItem(col_idx).text()
            action = QAction(header_text, self)
            action.setData(col_idx) # Store column index in action's data
            action.triggered.connect(
                lambda checked=False, tbl=table_widget, s_info=sort_info_dict, act=action: 
                self._handle_menu_sort_selection(tbl, act.data(), s_info)
            )
            menu.addAction(action)
        
        # Position the menu below the button
        menu.exec(button.mapToGlobal(QPoint(0, button.height())))

    def _handle_menu_sort_selection(self, table_widget: QTableWidget, column_index: int, sort_info_dict: dict):
        current_sort_col = sort_info_dict.get('col', -1)
        current_sort_order = sort_info_dict.get('order', Qt.SortOrder.AscendingOrder)

        if column_index == current_sort_col:
            # Toggle order if same column is selected again
            new_order = Qt.SortOrder.DescendingOrder if current_sort_order == Qt.SortOrder.AscendingOrder else Qt.SortOrder.AscendingOrder
        else:
            # Default to ascending for a new column
            new_order = Qt.SortOrder.AscendingOrder
        
        table_widget.sortByColumn(column_index, new_order)
        
        # Update sort_info_dict for next time
        sort_info_dict['col'] = column_index
        sort_info_dict['order'] = new_order
        
        # Update visual indicator on the header
        table_widget.horizontalHeader().setSortIndicator(column_index, new_order)
        if not table_widget.isSortingEnabled(): # Ensure it's enabled for visual cue
            table_widget.setSortingEnabled(True)


    def _style_home_table(self, table: QTableWidget):
        # Styles copied from Table.py
        table.setAlternatingRowColors(True)
        table.setShowGrid(False) # Hides the lines in the table
        table.verticalHeader().hide() # Hides the incrementer on the left

        table.verticalHeader().setDefaultSectionSize(50) # Row height
        table.horizontalHeader().setFixedHeight(60)      # Header height
        
        # Fill the whole frame with columns
        header = table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Selection behavior
        table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        table.setStyleSheet("""
            QTableWidget {
                background-color: #E8E7DD;            /* Even rows */
                alternate-background-color: #F4F4ED;  /* Odd rows */
                color: Black;
                border: none;
                border-radius: 15px;
            }
            QHeaderView::section {
                background-color: #F4F4ED;
                color: Black;
                border: none; /* No border for header sections specifically */
                padding: 8px; /* Copied from previous _style_home_table */
                font-size: 11pt; /* Copied from previous _style_home_table */
                font-weight: bold; /* Copied from previous _style_home_table */
            }
            QTableWidget::item:selected {
                background-color: #464646;  /* Highlight background from Table.py */
                color: white;              /* Highlight text color (changed from black for visibility) */
            }
            QTableWidget::item:focus {
                background-color: transparent;
                outline: none;              /* remove dotted outline */
                border: none;               /* drop any cell border on focus */
            }
            /* QTableWidget::item specific border from Table.py wasn't present; previous had border-bottom */
            /* For consistency with Table.py, let's remove individual item borders unless desired */
            QTableWidget::item {
                outline: none;
                border: none; /* This makes table look more like Table.py's setShowGrid(False) */
                padding-left: 8px; /* Copied from previous _style_home_table */
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
                background-color: #708090; 
                border: none; border-radius: 8px;
                padding: 8px 15px;
            }
            QPushButton:hover { background-color: #5A6875; } 
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
        if hasattr(self, 'vehicles_search_bar'): self.vehicles_search_bar.clear()
        if hasattr(self, 'payments_search_bar'): self.payments_search_bar.clear()
        if hasattr(self, 'parking_search_bar'): self.parking_search_bar.clear()

        self.home_overview_widget.show()
        self.vehicles_detail_view.hide()
        self.payments_detail_view.hide()
        self.parking_detail_view.hide()
        print("Returned to home overview.")

    def _prepare_detail_view(self, search_bar: QLineEdit, table_widget: QTableWidget, load_data_method: callable):
        self.home_overview_widget.hide()
        self.vehicles_detail_view.hide()
        self.payments_detail_view.hide()
        self.parking_detail_view.hide()
        
        load_data_method()
        if search_bar.text(): 
            self._filter_table_content(search_bar, table_widget)
        else: 
            for i in range(table_widget.rowCount()):
                table_widget.setRowHidden(i, False)

    def show_vehicles_detail(self):
        self._prepare_detail_view(self.vehicles_search_bar, self.vehicles_table, self.loadvehicles)
        self.vehicles_detail_view.show()
        print("Displaying vehicles detail table.")

    def show_payments_detail(self):
        self._prepare_detail_view(self.payments_search_bar, self.payments_table, self.loadtickets)
        self.payments_detail_view.show()
        print("Displaying payments detail table.")

    def show_parking_detail(self):
        self._prepare_detail_view(self.parking_search_bar, self.parking_table, self.EntryLoad)
        self.parking_detail_view.show()
        print("Displaying parking detail table.")
 
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
            logoicon.setPixmap(QPixmap(logomap_path))
        logoicon.setScaledContents(True)
        
        button = QPushButton("Home", self)
        button.setGeometry(0, 95, 250, 35)
        button.clicked.connect(self.show_home)
        Homeicon = QLabel(self)
        Homeicon.setGeometry(40,100,25,20)
        home_icon_path = "Icons/Home.png"
        if os.path.exists(home_icon_path):
            Homeicon.setPixmap(QPixmap(home_icon_path))
        Homeicon.setScaledContents(True)

        Tablebutton = QPushButton("Tables",self.cornerboard)
        Tablebutton.setGeometry(0,170,250,35)
        Tablebutton.clicked.connect(self.show_table)
        Tableicon = QLabel(self)
        Tableicon.setGeometry(40,176,25,20)
        if os.path.exists("Icons/table.png"):
            Tableicon.setPixmap(QPixmap("Icons/table.png"))
        Tableicon.setScaledContents(True)
        
        Savebutton = QPushButton("Moderator",self.cornerboard)
        Savebutton.setGeometry(0,240,250,35)
        Savebutton.clicked.connect(self.show_saves)
        saveicon = QLabel(self)
        saveicon.setGeometry(40,245,25,20)
        if os.path.exists("Icons/Information.png"):
            saveicon.setPixmap(QPixmap("Icons/Information.png"))
        saveicon.setScaledContents(True)

        Transaction = QPushButton("Settings",self.cornerboard)
        Transaction.setGeometry(0,310,250,35)
        Transaction.clicked.connect(self.show_transaction)
        transactionicon = QLabel(self)
        transactionicon.setGeometry(40,315,25,20)
        if os.path.exists("Icons/Settings.png"):
            transactionicon.setPixmap(QPixmap("Icons/Settings.png"))
        transactionicon.setScaledContents(True)

        common_button_style = """
        QPushButton {
            font-family: "Neuton"; font-size: 14pt; color: #6D6B6B;
            background: transparent; border: none; text-align: left; padding-left: 70px;
        }
        QPushButton:hover { color: #FFFFFF; }"""
        button.setStyleSheet(common_button_style)
        Transaction.setStyleSheet(common_button_style)
        Tablebutton.setStyleSheet(common_button_style)
        Savebutton.setStyleSheet(common_button_style)
        logotext.setStyleSheet("QLabel{font-family: \"Kavoon\"; font-size: 20pt; color: #FFFFFF;}")
    

    def loadvehicles(self):
        print("Loading vehicles data...")
        self.vehicles_table.setSortingEnabled(False) 
        self.vehicles_table.clearContents()
        self.vehicles_table.setRowCount(0)
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="password", database="parkindgticketdb"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT License_Plate, TypeOfVehicle FROM vehicle")
            results = cursor.fetchall()
            self.vehicles_table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.vehicles_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("Error loading vehicle data:", err)
        finally:
            self.vehicles_table.setSortingEnabled(True)
            if self.vehicles_sort_info['col'] != -1: # Reapply last sort from menu
                 self.vehicles_table.horizontalHeader().setSortIndicator(
                     self.vehicles_sort_info['col'], self.vehicles_sort_info['order']
                 )
       

    def loadtickets(self):
        print("Loading tickets data...")
        self.payments_table.setSortingEnabled(False)
        self.payments_table.clearContents()
        self.payments_table.setRowCount(0)
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="password", database="parkindgticketdb"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT TicketID, IssuedDate,License_Plate FROM ticket")
            results = cursor.fetchall()
            self.payments_table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.payments_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("Error loading ticket data:", err)
        finally:
            self.payments_table.setSortingEnabled(True)
            if self.payments_sort_info['col'] != -1:
                 self.payments_table.horizontalHeader().setSortIndicator(
                     self.payments_sort_info['col'], self.payments_sort_info['order']
                 )

    def EntryLoad(self):
        print("Loading entry data...")
        self.parking_table.setSortingEnabled(False)
        self.parking_table.clearContents()
        self.parking_table.setRowCount(0)
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="password", database="parkindgticketdb"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT TicketID, EntryTime,License_Plate,PresenceStatus FROM acquires")
            results = cursor.fetchall()
            self.parking_table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    if col_idx == 3: 
                         item_text = "Yes" if col_data else "No"
                    else:
                        item_text = str(col_data)
                    self.parking_table.setItem(row_idx, col_idx, QTableWidgetItem(item_text))
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            print("Error loading entry data:", err)
        finally:
            self.parking_table.setSortingEnabled(True)
            if self.parking_sort_info['col'] != -1:
                 self.parking_table.horizontalHeader().setSortIndicator(
                     self.parking_sort_info['col'], self.parking_sort_info['order']
                 )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    if not os.path.exists("Icons"):
        os.makedirs("Icons")
        print("Created 'Icons' directory. Please place your icon files there (e.g., sort.png).")

    window = MainWindow()
    window.show()
    sys.exit(app.exec())