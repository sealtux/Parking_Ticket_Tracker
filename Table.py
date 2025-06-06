from PyQt6.QtWidgets import (
    QApplication, QWidget, QFrame,QMessageBox,QComboBox,
    QTableWidget, QTableWidgetItem,QLabel,QHeaderView,QGraphicsDropShadowEffect,QScrollArea,QPushButton, QLineEdit,QAbstractItemView,QMessageBox,QInputDialog
)
from PyQt6.QtCore import Qt, QRect, QSize,QDate,QTime,QSortFilterProxyModel
from PyQt6.QtGui import QColor,QPixmap,QIcon

from Frames.Information import savecustom
import mysql.connector
from mysql.connector import Error
from datetime import datetime,date
import random
import string
import sys
import random
import string
import re
addbutton = None
date_combo = None
vehicle_type_combo = None
ticketinput = None
table = None
time_combo = None
vehicle_inputID = None



class MyCustomFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        #initialization{
        self.panel = QLabel(self)
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(0, 0, 1300, 850) #change the position
        self.panel.setStyleSheet("background-color: #F2F2E6;")  # apply color
        
        
        #add button
        global addbutton
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
        self.search_bar.textChanged.connect(self.filter_table)
        

        self.deletebutton = QPushButton(" Delete", self.panel)
        self.deletebutton.setGeometry(200,30,100,45)
        self.deletebutton.clicked.connect(self.remove_val)
        #sets the remove icon
        removeicon = QIcon("Icons/Remove.png")
        self.deletebutton.setIcon(removeicon)
        self.deletebutton.setIconSize(QSize(14, 14))
        
        self.sortcombo = QComboBox(self.panel)
        self.sortcombo.setGeometry(320, 30, 200, 45)
        self.sortcombo.addItems([
    "Sort by:",
    "Sort by: License Plate",
    "Sort by: Vehicle Type",
    "Sort by: Ticket ID",
    "Sort by: Date",
    "Sort by: Entry Time",
    "Sort by: Payment"
])
        self.sortcombo.setCurrentIndex(0)
        self.column_map = {
    "Sort by: License Plate": 0,
    "Sort by: Vehicle Type": 1,
    "Sort by: Ticket ID": 2,
    "Sort by: Date": 3,
    "Sort by: Entry Time": 4,
    "Sort by: Payment": 5
}
        self.sortcombo.setStyleSheet("""
    QComboBox {
        font-size: 12pt;
        border-radius: 5px;
        padding: 5px;
        background-color: #FFFFFF;
        color: black;
    }
    QComboBox::drop-down {
        background-color: #8E8383;
        width: 15px;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
    }
        QComboBox QAbstractItemView {
        background-color: #40455D;
        border-radius: 5px;
    }
                                              
""")
        self.sortcombo.currentTextChanged.connect(self.sort_table_by_combo)

        self.modifybutton = QPushButton(" Modify", self.panel)
        self.modifybutton.setGeometry(50,30,100,45)
        self.modifybutton.clicked.connect(self.modify_val)
        #sets the remove icon
        modifyicon = QIcon("Icons/Modify.png")
        self.modifybutton.setIcon(modifyicon)
        self.modifybutton.setIconSize(QSize(14, 14))
        

        # Apply a white background
        global table
        self.table = QTableWidget(self)
       
        self.table.setSortingEnabled(True)
       
        #Paid button
        self.Paid = QPushButton("  Paid",self.panel)
        self.Paid.setGeometry(1150, 30, 100, 45)
        self.Paid.clicked.connect(self.paid_func)
        money = QIcon("Icons/import.png")
        self.Paid.setIcon(money)
        self.Paid.setIconSize(QSize(14, 14))
        #}


        
       

        self.table.setColumnCount(6) 
        #sets the header text
        self.table.setHorizontalHeaderLabels(["License Plate","Vehicle Type","Ticket ID", "Date","Entry Time","Payment"])
        

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
        self.modifybutton.setStyleSheet("""
  QPushButton {
            font-family: "Neuton";
            font-size: 14pt;
            border-radius: 5px;
            background-color: #FFFFFF;
            border: none;
            color:Black
        }
        QPushButton:hover {
            background-color: #C5C3C3;
            
        }

                            
""")
        
        self.Paid.setStyleSheet("""
  QPushButton {
            font-family: "Neuton";
            font-size: 14pt;
            border-radius: 5px;
            background-color: #7EAD61;
            border: none;
            color:white
        }
        QPushButton:hover {
            background-color: #5C8046;
            
        }
                                        




""")
        
        

        self.Moderator = QPushButton("Moderator Mode", self)
        self.Moderator.setGeometry(1150, 652, 120, 50)
        self.Moderator.setStyleSheet(
        "background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px;"
        
    )
        self.Moderator.clicked.connect(self.on_moderator_mode)



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
        self.load_table_data()
        



###############################################################################
    def add_new(self):
    
        #sets global variables
        global addbutton 
        global date_combo 
        global vehicle_type_combo 
        global ticketinput
        global time_combo
        global table
        global vehicle_inputID
         
        self.addbutton.setEnabled(False)
        self.deletebutton.setEnabled(False)
        self.modifybutton.setEnabled(False)
        self.Paid.setEnabled(False)
        self.Moderator.setEnabled(False)

        
        self.table.clearSelection()

    # Frame at (700,100), size 400×300
        self.addframe = QFrame(self)
        self.addframe.setGeometry(700, 100, 400, 200)
        self.addframe.setStyleSheet("background-color: #E9E8E8; border-radius: 15px;")

        shadow = QGraphicsDropShadowEffect(self)
        shadow1 = QGraphicsDropShadowEffect(self)
        shadow2 = QGraphicsDropShadowEffect(self)
        
        #shadows
        shadow.setBlurRadius(10)
        shadow.setXOffset(2)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

        shadow1.setBlurRadius(10)
        shadow1.setXOffset(2)
        shadow1.setYOffset(2)
        shadow1.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

        shadow2.setBlurRadius(10)
        shadow2.setXOffset(2)
        shadow2.setYOffset(2)
        shadow2.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

        self.addframe.setGraphicsEffect(shadow1)
        


        
        
        
        
#adds a ticket inputer 
        self.Licenseplate = QLabel("License Plate:", self.addframe)
        self.Licenseplate.setGeometry(100, 20, 120, 30)

        self.Licenseplate_input = QLineEdit(self.addframe)
        self.Licenseplate_input.setGeometry(230, 20, 130, 30)
        self.Licenseplate_input.setPlaceholderText("ex.ABC1234")

        
        self.Licenseplate_input.setStyleSheet("""
    QLineEdit {
        font-size: 14pt;
        border-radius: 5px;
        padding: 5px;
        background-color: #D9D9D9;
        color: black;
    }
""")
        self.Licenseplate.setStyleSheet("""
    QLabel {
        font-size: 14pt;
        color: black;
                                        
    }
""")

        self.vehicle_label = QLabel("Ticket:", self.addframe)
        self.vehicle_label.setGeometry(30, 70, 120, 30)
        

# Vehicle Type Text Field
        self.ticketinput = QLineEdit(self.addframe)
        self.ticketinput.setGeometry(100, 70, 130, 30)
        self.ticketinput.setPlaceholderText("ex.1234-9283")

        self.ticketinput.setStyleSheet("""
    QLineEdit {
        font-size: 14pt;
        border-radius: 5px;
        padding: 5px;
        background-color: #D9D9D9;
        color: black;
    }
""")
        self.vehicle_label.setStyleSheet("""
    QLabel {
        font-size: 14pt;
        color: black;
    }
""")
      
        


        #this adds combobox for the vehicle type
        self.vehicle_type_combo = QComboBox(self.addframe)
        self.vehicle_type_combo.setGeometry(250, 70, 120, 30)
        self.vehicle_type_combo.setStyleSheet("""
    QComboBox {
        font-size: 12pt;
        border-radius: 5px;
        padding: 5px;
        background-color: #FFFFFF;
        color: black;
    }
    QComboBox::drop-down {
        background-color: #8E8383;
        width: 15px;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
    }
        QComboBox QAbstractItemView {
        background-color: #40455D;
        border-radius: 5px;
    }
                                              
""")
        self.vehicle_type_combo.addItems(["Vehicle:","Car", "Motorcycle"])

    # Submit button

        self.submit = QPushButton("Submit", self.addframe)
        self.submit.setGeometry(240, 120, 120, 40)  
        self.submit.setStyleSheet(
        "background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px;"
        
    )
        self.submit.setGraphicsEffect(shadow)
        self.submit.clicked.connect(self.submit_data)
        
        



    # Cancel button, also child of addframe, positioned to the left of Submit
        self.cancel = QPushButton("Cancel", self.addframe)
        self.cancel.setGeometry(45, 120, 120, 40)
        self.cancel.setStyleSheet(
            "background-color: #B25959; color: white; font-weight: bold; border-radius: 5px;"
    )
        self.cancel.setGraphicsEffect(shadow2)
        self.cancel.clicked.connect(self.on_cancel)
        
        self.addframe.show()
        self.submit.show()
        self.cancel.show()
        
        

        

        

        
        
        
        
        

    

    def remove_val(self):
        
        # Which row?
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Row Selected",
                                "Please select a row before clicking Delete.")
            return

        #  Read VehicleID (col 0) and TicketID (col 2)
        veh_item = self.table.item(row, 0)
        tkt_item = self.table.item(row, 2)
        if not veh_item or not tkt_item:
            QMessageBox.critical(self, "Error",
                                "Could not read License_Plate or TicketID from the selected row.")
            return
        vehicle_id = veh_item.text().strip()
        ticket_id  = tkt_item.text().strip()

        #  Confirm with user
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Delete Vehicle {vehicle_id} and Ticket {ticket_id} (and all related records)?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # 4) Delete in correct order
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="password", database="parkindgticketk"
            )
            cursor = conn.cursor()

            # Child tables first
            cursor.execute("DELETE FROM pays_for     WHERE TicketID = %s", (ticket_id,))
            cursor.execute("DELETE FROM acquires     WHERE TicketID = %s", (ticket_id,))
            cursor.execute("DELETE FROM parkingspace WHERE TicketID = %s", (ticket_id,))

            # Now the ticket
            cursor.execute("DELETE FROM ticket       WHERE TicketID = %s", (ticket_id,))

            # Finally the vehicle
            cursor.execute("DELETE FROM vehicle      WHERE License_Plate = %s", (vehicle_id,))

            conn.commit()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error",
                                f"Could not delete from database:\n{err}")
            return
        finally:
            cursor.close()
            conn.close()
            self.table.clearSelection()
        #  Update UI
        self.table.removeRow(row)
        QMessageBox.information(self, "Deleted",
                                f"Vehicle {vehicle_id} and Ticket {ticket_id} were deleted.")
        self.load_table_data()

        


    



    
    def paid_func(self):
        # 1) Which row?
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Row Selected", "Please select a row before clicking Paid.")
            return

        # 2) Read fields from the table
        vehicle_type = self.table.item(row, 1).text().strip()
        ticket_id    = self.table.item(row, 2).text().strip()
        date_str     = self.table.item(row, 3).text().strip()
        time_str     = self.table.item(row, 4).text().strip()

        # 3) Parse into datetime
        try:
            entry_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            QMessageBox.critical(self, "Parse Error", f"Could not parse entry date/time:\n{date_str} {time_str}")
            return

        now = datetime.now()
        delta = now - entry_dt
        hours = delta.total_seconds() / 3600.0

        # 4) Determine rate
        rate_per_hour = 5.0 if vehicle_type.lower() == "motorcycle" else 10.0
        amount_paid = round(hours * rate_per_hour, 2)

        # 5) Confirm with user
        confirm = QMessageBox.question(
            self,
            "Confirm Payment",
            f"Confirm payment for:\n\n"
            f"Ticket ID: {ticket_id}\n"
            f"Vehicle Type: {vehicle_type}\n"
            f"Duration: {hours:.2f} hours\n"
            f"Rate: ₱{rate_per_hour:.2f}/hr\n"
            f"Amount to Pay: ₱{amount_paid:.2f}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Cancelled", "Payment cancelled.")
            return

        # 6) Write to MySQL with UPSERT to avoid duplicates
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="password", database="parkindgticketk"
            )
            cur = conn.cursor()
            paysfor_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            sql = """
            INSERT INTO pays_for
                (Paysfor_ID, License_Plate, TicketID, AmountPaid, PaymentDate)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                AmountPaid = VALUES(AmountPaid),
                PaymentDate = VALUES(PaymentDate)
            """
            vehicle_id = self.table.item(row, 0).text().strip()
            cur.execute(sql, (paysfor_id, vehicle_id, ticket_id, amount_paid, now))
            conn.commit()
            cur.close()
            conn.close()
            self.table.clearSelection()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Could not record payment:\n{e}")
            return

        # 7) Update the table
        self.table.setItem(row, 5, QTableWidgetItem(f"₱{amount_paid:.2f}"))

        # 8) Show confirmation
        QMessageBox.information(
            self, "Payment Recorded",
            f"Ticket {ticket_id}\n"
            f"Vehicle Type: {vehicle_type}\n"
            f"Duration: {hours:.2f} hrs @ ₱{rate_per_hour:.2f}/hr\n"
            f"Amount: ₱{amount_paid:.2f}\n"
            f"Recorded at {now.strftime('%Y-%m-%d %H:%M:%S')}"
        )
    # ... your existing code above remains unchanged ...

    # 6) Write to MySQL with manual check to avoid duplicates
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="password", database="parkindgticketk"
            )
            cur = conn.cursor()

            vehicle_id = self.table.item(row, 0).text().strip()

            # Check if payment already exists for this TicketID
            cur.execute("SELECT COUNT(*) FROM pays_for WHERE TicketID = %s", (ticket_id,))
            exists = cur.fetchone()[0] > 0

            if exists:
                # Update existing payment record
                sql_update = """
                    UPDATE pays_for
                    SET AmountPaid = %s, PaymentDate = %s, License_Plate = %s
                    WHERE TicketID = %s
                """
                cur.execute(sql_update, (amount_paid, now, vehicle_id, ticket_id))
            else:
                # Insert new payment record
                paysfor_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
                sql_insert = """
                    INSERT INTO pays_for
                        (Paysfor_ID, License_Plate, TicketID, AmountPaid, PaymentDate)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cur.execute(sql_insert, (paysfor_id, vehicle_id, ticket_id, amount_paid, now))

            conn.commit()
            cur.close()
            conn.close()
            self.table.clearSelection()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Database Error", f"Could not record payment:\n{e}")
            return

    # ... rest of your existing code unchanged ...









    def submit_data(self):
        # Generate SpaceID like "A1-Y10"
        self.addbutton.setEnabled(True)
        
        part1 = random.choice(string.ascii_uppercase)
        part2 = random.choice(string.digits)
        part3 = random.choice(string.ascii_uppercase)
        part4 = ''.join(random.choices(string.digits, k=2))
        SpaceID = f"{part1}{part2}-{part3}{part4}"  # e.g., "A1-Y10"

        paysforID = ''.join(random.choices(string.ascii_uppercase, k=6))
        acquiresID = ''.join(random.choices(string.ascii_uppercase, k=6))

        # Get values from form
        vehicle_type = self.vehicle_type_combo.currentText().strip()
        Ticket_type = self.ticketinput.text().strip()
        VehicleID = self.Licenseplate_input.text().strip()

        # Input validation
        if vehicle_type == "Vehicle:" or not Ticket_type or not VehicleID:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields correctly.")
            return
         # Validate ticket ID format
        ticket_pattern = re.compile(r"^(\d{4})-(\d{4})$")
        match = ticket_pattern.match(Ticket_type)

        if not match:
            QMessageBox.warning(self, "Invalid Format", "Ticket ID must be in the format DDDD-DDDD (e.g., 1234-5678).")
            return

        left, right = int(match.group(1)), int(match.group(2))
        if left == 0 or right == 0:
            QMessageBox.warning(self, "Invalid Ticket ID", "Both parts of the Ticket ID must be greater than zero.")
            return
        license_pattern = re.compile(r"^[A-Z]{3}\d{4}$")
        match = license_pattern.match(VehicleID)

        if not match:
            QMessageBox.warning(self, "Invalid License Plate",
                                "License plate must be in the format LLLnNNN (e.g., ABC1234).")
            return
        
        try:
            # Connect to MySQL
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",  # change as needed
                database="parkindgticketk"
            )
            cursor = conn.cursor()
            conn.start_transaction()  # Start explicit transaction

            # Check for duplicate License Plate
            cursor.execute("SELECT 1 FROM vehicle WHERE License_Plate = %s", (VehicleID,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Duplicate Error", f"License Plate '{VehicleID}' already exists.")
                cursor.close()
                conn.close()
                return

            # Check for duplicate Ticket ID
            cursor.execute("SELECT 1 FROM ticket WHERE TicketID = %s", (Ticket_type,))
            if cursor.fetchone():
                QMessageBox.warning(self, "Duplicate Error", f"Ticket ID '{Ticket_type}' already exists.")
                cursor.close()
                conn.close()
                return

            # Confirm before proceeding
            confirm = QMessageBox.question(
                self,
                "Confirm Entry",
                f"Are you sure you want to add this new entry?\n\n"
                f"License Plate: {VehicleID}\n"
                f"Ticket ID: {Ticket_type}\n"
                f"Vehicle Type: {vehicle_type}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm != QMessageBox.StandardButton.Yes:
                QMessageBox.information(self, "Cancelled", "Operation cancelled by user.")
                cursor.close()
                conn.close()
                return

            # Insert into vehicle table
            sql_vehicle = "INSERT INTO vehicle (License_Plate, TypeofVehicle) VALUES (%s, %s)"
            cursor.execute(sql_vehicle, (VehicleID, vehicle_type))

            # Insert into ticket table
            sql_ticket = "INSERT INTO ticket (TicketID, IssuedDate, License_Plate, SpaceID) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_ticket, (Ticket_type, date.today(), VehicleID, SpaceID))

            # Insert into parkingspace table
            sql_parking = "INSERT INTO parkingspace (SpaceID, TicketID, VehicleType,License_Plate) VALUES (%s, %s, %s,%s)"
            cursor.execute(sql_parking, (SpaceID, Ticket_type, vehicle_type, VehicleID))

            # Insert into pays_for table
            sql_pays_for = """
                INSERT INTO pays_for(Paysfor_ID, License_Plate, TicketID, AmountPaid, PaymentDate)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_pays_for, (paysforID, VehicleID, Ticket_type, 0.00, datetime.now()))

            # Insert into acquires table
            sql_acquires = """
                INSERT INTO acquires(Acquires_ID, License_Plate, TicketID, EntryTime, PresenceStatus)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_acquires, (acquiresID, VehicleID, Ticket_type, datetime.now().time(), True))

            # Commit all changes
            conn.commit()

            cursor.close()
            conn.close()

            # Success message
            QMessageBox.information(self, "Success", "Entry added successfully!")
            self.load_table_data()

            # Reset form
            self.modifybutton.setEnabled(True)
            self.deletebutton.setEnabled(True)
            self.Paid.setEnabled(True)
            self.Moderator.setEnabled(True)

            self.ticketinput.clear()
            self.vehicle_type_combo.setCurrentIndex(0)
            self.addbutton.setEnabled(True)
            self.addframe.hide()

        except mysql.connector.Error as err:
            conn.rollback()  # rollback on error
            cursor.close()
            conn.close()
            QMessageBox.critical(self, "Database Error", f"Error: {err}")
            





        

    def on_cancel(self):
    # hide the add‑frame
        self.addbutton.setEnabled(True)
        self.modifybutton.setEnabled(True)
        self.deletebutton.setEnabled(True)
        self.Paid.setEnabled(True)
        self.Moderator.setEnabled(True)
        self.addframe.hide()
    # re‑enable the Add button
        
        


    

    def load_table_data(self):
       

          # Clear existing rows
        self.table.setRowCount(0)

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",   # your password
                database="parkindgticketk"  # your DB
            )
            cursor = conn.cursor()

            # Select each ticket only once, with latest payment if any
            cursor.execute("""
                SELECT
                v.License_Plate,
                v.TypeOfVehicle,
                t.TicketID,
                t.IssuedDate   AS `Date`,
                a.EntryTime    AS `Entry Time`,
                (
                    SELECT pf.AmountPaid
                    FROM pays_for pf
                    WHERE pf.TicketID = t.TicketID
                    ORDER BY pf.PaymentDate DESC
                    LIMIT 1
                ) AS `Payment`
                FROM vehicle  AS v
                JOIN ticket   AS t  ON v.License_Plate = t.License_Plate
                JOIN acquires AS a  ON t.TicketID  = a.TicketID
                ORDER BY a.EntryTime DESC
            """)
            self.table_data = cursor.fetchall()
            
            for row_data in self.table_data:  
                row_idx = self.table.rowCount()
                self.table.insertRow(row_idx)
                for col_idx, value in enumerate(row_data):
                    item = QTableWidgetItem("" if value is None else str(value))
                    self.table.setItem(row_idx, col_idx, item)

            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print("Error loading data:", err)




    def modify_val(self):
        self.modifybutton.setEnabled(False)
        self.addbutton.setEnabled(False)
        self.deletebutton.setEnabled(False)
        self.Paid.setEnabled(False)
        self.Moderator.setEnabled(False)

        print("clicked")
        self.table.clearSelection()
        self.addframe = QFrame(self)
        self.addframe.setGeometry(100, 100, 400, 200)
        self.addframe.setStyleSheet("background-color: #E9E8E8; border-radius: 15px;")
        
        
        
        row = self.table.currentRow()
        if row < 0:
            self.modifybutton.setEnabled(True )
            QMessageBox.warning(self, "No Row Selected",
                                    "Please select a row before clicking Modify.")
            
            self.modifybutton.setEnabled(True)
            self.addbutton.setEnabled(True)
            self.deletebutton.setEnabled(True)
            self.Paid.setEnabled(True)
            self.Moderator.setEnabled(True)
                    
            return
    
        old_ticket_id    = self.table.item(row, 2).text().strip()
        License_Plate = self.table.item(row, 0).text().strip()
        self._old_ticket_id = old_ticket_id
       
        print(old_ticket_id)
        
        shadow = QGraphicsDropShadowEffect(self)
        shadow1 = QGraphicsDropShadowEffect(self)
        shadow2 = QGraphicsDropShadowEffect(self)
        
        
        
        #shadows
        shadow.setBlurRadius(10)
        shadow.setXOffset(2)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

        shadow1.setBlurRadius(10)
        shadow1.setXOffset(2)
        shadow1.setYOffset(2)
        shadow1.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

        shadow2.setBlurRadius(10)
        shadow2.setXOffset(2)
        shadow2.setYOffset(2)
        shadow2.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

        self.addframe.setGraphicsEffect(shadow1)

        


#adds a ticket inputer 
        self.Licenseplate = QLabel("License Plate:", self.addframe)
        self.Licenseplate.setGeometry(100, 20, 120, 30)

        self.Licenseplate_input = QLineEdit(self.addframe)
        self.Licenseplate_input.setGeometry(230, 20, 130, 30)
        self.Licenseplate_input.setPlaceholderText("ex.ABC1234")

        self.Licenseplate_input.setText(License_Plate)
        self.Licenseplate_input.setStyleSheet("""
    QLineEdit {
        font-size: 14pt;
        border-radius: 5px;
        padding: 5px;
        background-color: #D9D9D9;
        color: black;
    }
""")
        self.Licenseplate.setStyleSheet("""
    QLabel {
        font-size: 14pt;
        color: black;
    }
""")
        self.vehicle_label = QLabel("Ticket:", self.addframe)
        self.vehicle_label.setGeometry(30, 70, 120, 30)
        

# Vehicle Type Text Field
        self.ticketinput = QLineEdit(self.addframe)
        self.ticketinput.setGeometry(100, 70, 130, 30)
        self.ticketinput.setText(old_ticket_id)

        self.ticketinput.setStyleSheet("""
    QLineEdit {
        font-size: 14pt;
        border-radius: 5px;
        padding: 5px;
        background-color: #D9D9D9;
        color: black;
    }
""")
        self.vehicle_label.setStyleSheet("""
    QLabel {
        font-size: 14pt;
        color: black;
    }
""")
      
        

        
        #this adds combobox for the vehicle type
        self.vehicle_type_combo = QComboBox(self.addframe)
        self.vehicle_type_combo.setGeometry(250, 70, 120, 30)
        #  Read old value from the table
        

        self.vehicle_type_combo.setStyleSheet("""
    QComboBox {
        font-size: 12pt;
        border-radius: 5px;
        padding: 5px;
        background-color: #FFFFFF;
        color: black;
    }
    QComboBox::drop-down {
        background-color: #8E8383;
        width: 15px;
        border-top-right-radius: 5px;
        border-bottom-right-radius: 5px;
    }
        QComboBox QAbstractItemView {
        background-color: #40455D;
        border-radius: 5px;
    }
                                              
""")
        self.vehicle_type_combo.addItems(["Vehicle:","Car", "Motorcycle"])

    # Submit button
        

        old_vehicle_type = self.table.item(row, 1).text().strip()
        

#  Use stripped, exact match against combo box
        index = self.vehicle_type_combo.findText(old_vehicle_type, Qt.MatchFlag.MatchExactly)

        # If found, select it
        if index >= 0:
            self.vehicle_type_combo.setCurrentIndex(index)
        else:
            self.vehicle_type_combo.setCurrentIndex(0)  # fallback
        

        self.submit = QPushButton("Submit", self.addframe)
        self.submit.setGeometry(240, 120, 120, 40)  
        self.submit.setStyleSheet(
        "background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px;"
        
    )
        self.submit.setGraphicsEffect(shadow)
        self.submit.clicked.connect(self.modify_submit)
        
        



    # Cancel button, also child of addframe, positioned to the left of Submit
        self.cancel = QPushButton("Cancel", self.addframe)
        self.cancel.setGeometry(45, 120, 120, 40)
        self.cancel.setStyleSheet(
            "background-color: #B25959; color: white; font-weight: bold; border-radius: 5px;"
    )
        self.cancel.setGraphicsEffect(shadow2)
        self.cancel.clicked.connect(self.on_cancel)
        
        self.addframe.show()
        self.submit.show()
        self.cancel.show()
        

        
   
  


    
    def modify_submit(self):
        self.modifybutton.setEnabled(True)
        new_ticket = self.ticketinput.text().strip()
        new_type = self.vehicle_type_combo.currentText().strip()
        new_license = self.Licenseplate_input.text().strip().upper()

        old_ticket = getattr(self, "_old_ticket_id", None)

        if (not new_ticket) or (new_type == "Vehicle:") or (not old_ticket):
            QMessageBox.warning(self, "Input Error",
                                "Please enter a new TicketID and select a vehicle type.")
            return

        # Validate Ticket ID
        ticket_pattern = re.compile(r"^(\d{4})-(\d{4})$")
        match = ticket_pattern.match(new_ticket)
        if not match or int(match.group(1)) == 0 or int(match.group(2)) == 0:
            QMessageBox.warning(self, "Invalid Ticket ID", "Ticket ID must be in format DDDD-DDDD and not contain 0000.")
            return

        # Validate License Plate
        license_pattern = re.compile(r"^[A-Z]{3}\d{4}$")
        match = license_pattern.match(new_license)
        if not match:
            QMessageBox.warning(self, "Invalid License Plate",
                                "License plate must be in the format LLLnNNN (e.g., ABC1234).")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Modification",
            f"Are you sure you want to update the following?\n\n"
            f"Old Ticket ID: {old_ticket}\n"
            f"New Ticket ID: {new_ticket}\n"
            f"New Vehicle Type: {new_type}\n"
            f"New License Plate: {new_license}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm != QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Cancelled", "Modification cancelled.")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="password", database="parkindgticketk"
            )
            cur = conn.cursor()

            # Get old license plate
            cur.execute("SELECT License_Plate FROM ticket WHERE TicketID = %s", (old_ticket,))
            result = cur.fetchone()
            if not result:
                QMessageBox.warning(self, "Not Found", "Ticket not found in the database.")
                return

            old_license = result[0]

            # Prevent duplicate license plate assignment
            cur.execute("""
                SELECT t.TicketID 
                FROM vehicle v 
                JOIN ticket t ON v.License_Plate = t.License_Plate 
                WHERE v.License_Plate = %s
            """, (new_license,))
            row = cur.fetchone()
            if row and row[0] != old_ticket:
                QMessageBox.warning(self, "Duplicate License Plate",
                                    f"License plate {new_license} is already assigned to another ticket.")
                return

            # Prevent duplicate ticket ID if changing it
            if new_ticket != old_ticket:
                cur.execute("SELECT TicketID FROM ticket WHERE TicketID = %s", (new_ticket,))
                existing_ticket = cur.fetchone()
                if existing_ticket:
                    QMessageBox.warning(self, "Duplicate Ticket ID",
                                        f"Ticket ID {new_ticket} already exists. Please choose a different one.")
                    return

            cur.execute("SET FOREIGN_KEY_CHECKS = 0;")

            # Only update License_Plate if changed
            if new_license != old_license:
                cur.execute("UPDATE acquires SET License_Plate = %s WHERE License_Plate = %s", (new_license, old_license))
                cur.execute("UPDATE ticket SET License_Plate = %s WHERE TicketID = %s", (new_license, old_ticket))
                cur.execute("UPDATE vehicle SET License_Plate = %s WHERE License_Plate = %s", (new_license, old_license))

            # Only update TicketID if changed
            if new_ticket != old_ticket:
                cur.execute("UPDATE acquires SET TicketID = %s WHERE TicketID = %s", (new_ticket, old_ticket))
                cur.execute("UPDATE pays_for SET TicketID = %s WHERE TicketID = %s", (new_ticket, old_ticket))
                cur.execute("UPDATE parkingspace SET TicketID = %s WHERE TicketID = %s", (new_ticket, old_ticket))
                cur.execute("UPDATE ticket SET TicketID = %s WHERE TicketID = %s", (new_ticket, old_ticket))

            # Always update vehicle type
            cur.execute("""
                UPDATE vehicle v
                JOIN ticket t ON v.License_Plate = t.License_Plate
                SET v.TypeOfVehicle = %s
                WHERE t.TicketID = %s
            """, (new_type, new_ticket if new_ticket != old_ticket else old_ticket))

            cur.execute("SET FOREIGN_KEY_CHECKS = 1;")
            conn.commit()
            self.deletebutton.setEnabled(True)
            self.addbutton.setEnabled(True)
            self.modifybutton.setEnabled(True)
            self.Paid.setEnabled(True)
            self.Moderator.setEnabled(True)

        except mysql.connector.Error as e:
            conn.rollback()
            QMessageBox.critical(self, "Database Error", f"Could not update records:\n{e}")
            return

        finally:
            cur.close()
            conn.close()

        self.load_table_data()
        QMessageBox.information(self, "Success",
                                f"Ticket {old_ticket} → {new_ticket}\n"
                                f"Vehicle type: {new_type}\n"
                                f"License plate updated to: {new_license}")
        self.submit.setText("Submit")
        self.submit.clicked.disconnect()
        self.submit.clicked.connect(self.submit_data)
        self.addframe.hide()






        

    def filter_table(self,search_text):
        print("clicked")
           
        search_text = search_text.lower().strip()

        for row in range(self.table.rowCount()):
                match = False
                for col in range(self.table.columnCount()):
                    item = self.table.item(row, col)
                    if item and search_text in item.text().lower():
                        match = True
                        break
                self.table.setRowHidden(row, not match)


    def sort_table_by_combo(self, selected_text):
        if selected_text == "Sort by:":
            self.table.setSortingEnabled(False)
            self.load_table_data()  # Optional: Reset to original order
            return

        column = self.column_map.get(selected_text)
        if column is not None:
            self.table.setSortingEnabled(True)
            self.table.sortItems(column, Qt.SortOrder.AscendingOrder)
            self.table.setSortingEnabled(False)  # Lock sorting to prevent user clicks




    def on_moderator_mode(self):
            self.deletebutton.setEnabled(False)
            self.addbutton.setEnabled(False)
            self.modifybutton.setEnabled(False)
            self.Paid.setEnabled(False)
            self.Moderator.setEnabled(False)

            password, ok = QInputDialog.getText(
            self,
            "Moderator Access",
            "Enter moderator password:",
            QLineEdit.EchoMode.Password
        )

            if not ok or password != "password":  # Change  to your desired password
                QMessageBox.warning(self, "Access Denied", "Incorrect password. Access denied.")
                self.deletebutton.setEnabled(True)
                self.addbutton.setEnabled(True)
                self.modifybutton.setEnabled(True)
                self.Paid.setEnabled(True)
                self.Moderator.setEnabled(True)
                return
    
            self.table.clearSelection()
            self.addframe = QFrame(self)
            self.addframe.setGeometry(500, 450, 650, 200)
            self.addframe.setStyleSheet("background-color: #E9E8E8; border-radius: 15px;")
            
            
            row = self.table.currentRow()
            if row < 0:
                QMessageBox.warning(self, "No Row Selected",
                                        "Please select a row before clicking Modify.")
                self.deletebutton.setEnabled(True)
                self.addbutton.setEnabled(True)
                self.modifybutton.setEnabled(True)
                self.Paid.setEnabled(True)
                self.Moderator.setEnabled(True)
                return
        
            old_ticket_id    = self.table.item(row, 2).text().strip()
            License_Plate = self.table.item(row, 0).text().strip()
            self._old_ticket_id = old_ticket_id
        
            
            old_Date = self.table.item(row, 3).text().strip()
            old_Time = self.table.item(row, 4).text().strip()
            print(old_Date)
            print(old_Time)

            shadow = QGraphicsDropShadowEffect(self)
            shadow1 = QGraphicsDropShadowEffect(self)
            shadow2 = QGraphicsDropShadowEffect(self)
            
            
            
            #shadows
            shadow.setBlurRadius(10)
            shadow.setXOffset(2)
            shadow.setYOffset(2)
            shadow.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

            shadow1.setBlurRadius(10)
            shadow1.setXOffset(2)
            shadow1.setYOffset(2)
            shadow1.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

            shadow2.setBlurRadius(10)
            shadow2.setXOffset(2)
            shadow2.setYOffset(2)
            shadow2.setColor(QColor(0, 0, 0, 160))  # semi-transparent black

            self.addframe.setGraphicsEffect(shadow1)

            self.Datetext = QLabel("Date:", self.addframe)
            self.Datetext.setGeometry(400, 20, 120, 30)

            self.Datetextinput = QLineEdit(self.addframe)
            self.Datetextinput.setGeometry(450, 20, 150, 30)
            self.Datetextinput.setPlaceholderText("ex.2025-05-26")
            self.Datetextinput.setText(old_Date)
            
            self.Timetext = QLabel("Time:", self.addframe)
            self.Timetext.setGeometry(400, 70, 120, 30)

            self.Timetexinp = QLineEdit(self.addframe)
            self.Timetexinp.setGeometry(450, 70, 150, 30)
            self.Timetexinp.setPlaceholderText("02:17:05")
            self.Timetexinp.setText(old_Time)
            self.Timetexinp.setStyleSheet("""
        QLineEdit {
            font-size: 14pt;
            border-radius: 5px;
            padding: 5px;
            background-color: #D9D9D9;
            color: black;
        }
    """)
            self.Datetextinput.setStyleSheet("""
        QLineEdit {
            font-size: 14pt;
            border-radius: 5px;
            padding: 5px;
            background-color: #D9D9D9;
            color: black;
        }
    """)
            self.Datetext.setStyleSheet("""
        QLabel {
            font-size: 14pt;
            color: black;
        }
    """)
            self.Timetext.setStyleSheet("""
        QLabel {
            font-size: 14pt;
            color: black;
        }
    """)

    #adds a ticket inputer 
            self.Licenseplate = QLabel("License Plate:", self.addframe)
            self.Licenseplate.setGeometry(100, 20, 120, 30)

            self.Licenseplate_input = QLineEdit(self.addframe)
            self.Licenseplate_input.setGeometry(230, 20, 130, 30)
            self.Licenseplate_input.setPlaceholderText("ex.ABC1234")

            self.Licenseplate_input.setText(License_Plate)
            self.Licenseplate_input.setStyleSheet("""
        QLineEdit {
            font-size: 14pt;
            border-radius: 5px;
            padding: 5px;
            background-color: #D9D9D9;
            color: black;
        }
    """)
            self.Licenseplate.setStyleSheet("""
        QLabel {
            font-size: 14pt;
            color: black;
        }
    """)
            self.vehicle_label = QLabel("Ticket:", self.addframe)
            self.vehicle_label.setGeometry(30, 70, 120, 30)
            

    # Vehicle Type Text Field
            self.ticketinput = QLineEdit(self.addframe)
            self.ticketinput.setGeometry(100, 70, 130, 30)
            self.ticketinput.setText(old_ticket_id)

            self.ticketinput.setStyleSheet("""
        QLineEdit {
            font-size: 14pt;
            border-radius: 5px;
            padding: 5px;
            background-color: #D9D9D9;
            color: black;
        }
    """)
            self.vehicle_label.setStyleSheet("""
        QLabel {
            font-size: 14pt;
            color: black;
        }
    """)
        
            

            
            #this adds combobox for the vehicle type
            self.vehicle_type_combo = QComboBox(self.addframe)
            self.vehicle_type_combo.setGeometry(250, 70, 120, 30)
            #  Read old value from the table
            

            self.vehicle_type_combo.setStyleSheet("""
        QComboBox {
            font-size: 12pt;
            border-radius: 5px;
            padding: 5px;
            background-color: #FFFFFF;
            color: black;
        }
        QComboBox::drop-down {
            background-color: #8E8383;
            width: 15px;
            border-top-right-radius: 5px;
            border-bottom-right-radius: 5px;
        }
            QComboBox QAbstractItemView {
            background-color: #40455D;
            border-radius: 5px;
        }
                                                
    """)
            self.vehicle_type_combo.addItems(["Vehicle:","Car", "Motorcycle"])

        # Submit button
            

            old_vehicle_type = self.table.item(row, 1).text().strip()
            

    #  Use stripped, exact match against combo box
            index = self.vehicle_type_combo.findText(old_vehicle_type, Qt.MatchFlag.MatchExactly)

            # If found, select it
            if index >= 0:
                self.vehicle_type_combo.setCurrentIndex(index)
            else:
                self.vehicle_type_combo.setCurrentIndex(0)  # fallback
            

            self.submit = QPushButton("Submit", self.addframe)
            self.submit.setGeometry(500, 120, 120, 40)  
            self.submit.setStyleSheet(
            "background-color: #4CAF50; color: white; font-weight: bold; border-radius: 5px;"
            
        )
            self.submit.setGraphicsEffect(shadow)
            self.submit.clicked.connect(self.submit_moderator_edit)
            
            



        # Cancel button, also child of addframe, positioned to the left of Submit
            self.cancel = QPushButton("Cancel", self.addframe)
            self.cancel.setGeometry(45, 120, 120, 40)
            self.cancel.setStyleSheet(
                "background-color: #B25959; color: white; font-weight: bold; border-radius: 5px;"
        )
            self.cancel.setGraphicsEffect(shadow2)
            self.cancel.clicked.connect(self.on_cancel)
            
            self.addframe.show()
            self.submit.show()
            self.cancel.show()





    def submit_moderator_edit(self):
        
        try:
            new_ticket = self.ticketinput.text().strip()
            new_license = self.Licenseplate_input.text().strip()
            new_date = self.Datetextinput.text().strip()
            new_time = self.Timetexinp.text().strip()
            new_type = self.vehicle_type_combo.currentText().strip()
            old_ticket = getattr(self, "_old_ticket_id", None)

            if not all([new_ticket, new_license, new_date, new_time, new_type]) or new_type == "Vehicle:":
                QMessageBox.warning(self, "Input Error", "Please fill in all fields and select a valid vehicle type.")
                return

            # Validate TicketID format
            ticket_pattern = re.compile(r"^(\d{4})-(\d{4})$")
            if not ticket_pattern.match(new_ticket):
                QMessageBox.warning(self, "Invalid Ticket ID", "Ticket ID must be in the format 1234-5678.")
                return

            # Validate License Plate format
            license_pattern = re.compile(r"^[A-Z]{3}?\d{4}$")
            if not license_pattern.match(new_license):
                QMessageBox.warning(self, "Invalid License Plate", "License plate must be in the format ABC1234.")
                return

            # ✅ Validate combined date & time are in the past
            try:
                combined_datetime = datetime.strptime(f"{new_date} {new_time}", "%Y-%m-%d %H:%M:%S")
                if combined_datetime > datetime.now():
                    QMessageBox.warning(self, "Invalid Date/Time", "The date and time cannot be in the future.")
                    return
            except ValueError:
                QMessageBox.warning(self, "Invalid Format", "Ensure date is YYYY-MM-DD and time is HH:MM:SS (24-hour).")
                return

            confirm = QMessageBox.question(
                self,
                "Confirm Update",
                f"Are you sure you want to apply the following changes?\n\n"
                f"Old Ticket ID: {old_ticket}\nNew Ticket ID: {new_ticket}\n"
                f"License Plate: {new_license}\nDate: {new_date}\nTime: {new_time}\nType: {new_type}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )

            if confirm != QMessageBox.StandardButton.Yes:
                QMessageBox.information(self, "Cancelled", "Changes were not applied.")
                return

            # --- Perform the database operations ---
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="parkindgticketk"
            )
            cur = conn.cursor()
            conn.start_transaction()

            cur.execute("SELECT License_Plate FROM ticket WHERE TicketID = %s", (old_ticket,))
            result = cur.fetchone()
            if not result:
                QMessageBox.warning(self, "Not Found", "Ticket not found.")
                return

            old_license = result[0]

            cur.execute("SET FOREIGN_KEY_CHECKS = 0")

            cur.execute("UPDATE ticket SET TicketID = %s, License_Plate = %s, IssuedDate = %s WHERE TicketID = %s",
                        (new_ticket, new_license, new_date, old_ticket))

            cur.execute("UPDATE acquires SET License_Plate = %s, TicketID = %s, EntryTime = %s WHERE TicketID = %s",
                        (new_license, new_ticket, new_time, old_ticket))

            cur.execute("UPDATE pays_for SET TicketID = %s WHERE TicketID = %s", (new_ticket, old_ticket))
            cur.execute("UPDATE parkingspace SET TicketID = %s WHERE TicketID = %s", (new_ticket, old_ticket))
            cur.execute("UPDATE vehicle SET License_Plate = %s WHERE License_Plate = %s", (new_license, old_license))

            cur.execute("""
                UPDATE vehicle v 
                JOIN ticket t ON v.License_Plate = t.License_Plate
                SET v.TypeOfVehicle = %s 
                WHERE t.TicketID = %s
            """, (new_type, new_ticket))

            cur.execute("SET FOREIGN_KEY_CHECKS = 1")
            conn.commit()

            QMessageBox.information(self, "Success", "Record updated successfully.")
            self.addframe.hide()
            self.load_table_data()
            self.deletebutton.setEnabled(True)
            self.addbutton.setEnabled(True)
            self.modifybutton.setEnabled(True)
            self.Paid.setEnabled(True)
            self.Moderator.setEnabled(True)
        except mysql.connector.Error as e:
            if conn:
                conn.rollback()
            QMessageBox.critical(self, "Database Error", str(e))

        finally:
            if 'cur' in locals():
                cur.close()
            if 'conn' in locals():
                conn.close()
            
        

    