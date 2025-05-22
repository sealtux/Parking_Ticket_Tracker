from PyQt6.QtWidgets import (
    QApplication, QWidget, QFrame,QMessageBox,QComboBox,
    QTableWidget, QTableWidgetItem,QLabel,QHeaderView,QGraphicsDropShadowEffect,QScrollArea,QPushButton, QLineEdit,QAbstractItemView,QMessageBox
)
from PyQt6.QtCore import Qt, QRect, QSize,QDate,QTime
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

addbutton = None
date_combo = None
vehicle_type_combo = None
vehicle_input = None
table = None
time_combo = None
vehicle_inputID = None


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='parkindgticketdb',
            user='root',
            password='password'
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

class MyCustomFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        #initialization{
        self.panel = QLabel(self)
        self.panel.setFrameShape(QFrame.Shape.StyledPanel)
        self.panel.setGeometry(0, 0, 1300, 850) #change the position
        self.panel.setStyleSheet("background-color: #F2F2E6;")  # apply color
        create_connection()
        
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
        

        self.deletebutton = QPushButton(" Delete", self.panel)
        self.deletebutton.setGeometry(200,30,100,45)
        self.deletebutton.clicked.connect(self.remove_val)
        #sets the remove icon
        removeicon = QIcon("Icons/Remove.png")
        self.deletebutton.setIcon(removeicon)
        self.deletebutton.setIconSize(QSize(14, 14))
        
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
        self.table.setHorizontalHeaderLabels(["Vehicle ID","Vehicle Type","Ticket ID", "Date","Entry Time","Payment"])
       

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
        global vehicle_input
        global time_combo
        global table
        global vehicle_inputID
         
        self.addbutton.setEnabled(False)

        
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

        self.vehicle_label = QLabel("Ticket:", self.addframe)
        self.vehicle_label.setGeometry(30, 50, 120, 30)
        

# Vehicle Type Text Field
        self.vehicle_input = QLineEdit(self.addframe)
        self.vehicle_input.setGeometry(100, 50, 130, 30)
        self.vehicle_input.setPlaceholderText("ex.1234-9283")

        self.vehicle_input.setStyleSheet("""
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
        self.vehicle_type_combo.setGeometry(250, 50, 100, 30)
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
        self.vehicle_type_combo.addItems(["Vehicle:","     Car", "Motorcycle"])

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

        # 1) Which row?
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Row Selected",
                                "Please select a row before clicking Delete.")
            return

        # 2) Read VehicleID (col 0) and TicketID (col 2)
        veh_item = self.table.item(row, 0)
        tkt_item = self.table.item(row, 2)
        if not veh_item or not tkt_item:
            QMessageBox.critical(self, "Error",
                                "Could not read VehicleID or TicketID from the selected row.")
            return
        vehicle_id = veh_item.text().strip()
        ticket_id  = tkt_item.text().strip()

        # 3) Confirm with user
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
                password="password", database="parkindgticketdb"
            )
            cursor = conn.cursor()

            # Child tables first
            cursor.execute("DELETE FROM pays_for     WHERE TicketID = %s", (ticket_id,))
            cursor.execute("DELETE FROM acquires     WHERE TicketID = %s", (ticket_id,))
            cursor.execute("DELETE FROM parkingspace WHERE TicketID = %s", (ticket_id,))

            # Now the ticket
            cursor.execute("DELETE FROM ticket       WHERE TicketID = %s", (ticket_id,))

            # Finally the vehicle
            cursor.execute("DELETE FROM vehicle      WHERE VehicleID = %s", (vehicle_id,))

            conn.commit()

        except mysql.connector.Error as err:
            QMessageBox.critical(self, "Database Error",
                                f"Could not delete from database:\n{err}")
            return
        finally:
            cursor.close()
            conn.close()
            self.table.clearSelection()
        # 5) Update UI
        self.table.removeRow(row)
        QMessageBox.information(self, "Deleted",
                                f"Vehicle {vehicle_id} and Ticket {ticket_id} were deleted.")
        self.load_table_data()

        


    



    
    def paid_func(self):
            # 1) Which row?
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "No Row Selected",
                                "Please select a row before clicking Paid.")
            return

        # 2) Read fields from the table
        vehicle_type = self.table.item(row, 1).text().strip()  # column 1 = Vehicle Type
        ticket_id    = self.table.item(row, 2).text().strip()
        date_str     = self.table.item(row, 3).text().strip()  # "YYYY-MM-DD"
        time_str     = self.table.item(row, 4).text().strip()  # "HH:MM:SS"

        # 3) Parse into datetime
        try:
            entry_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
        except ValueError:
            QMessageBox.critical(self, "Parse Error",
                                f"Could not parse entry date/time:\n{date_str} {time_str}")
            return

        now = datetime.now()
        delta = now - entry_dt
        hours = delta.total_seconds() / 3600.0

        # 4) Determine rate
        rate_per_hour = 5.0 if vehicle_type.lower() == "motorcycle" else 10.0
        amount_paid = round(hours * rate_per_hour, 2)

        # 5) Write to MySQL
        try:
            conn = mysql.connector.connect(
                host="localhost", user="root",
                password="password", database="parkindgticketdb"
            )
            cur = conn.cursor()
            paysfor_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            sql = """
            INSERT INTO pays_for
                (Paysfor_ID, VehicleID, TicketID, AmountPaid, PaymentDate)
            VALUES (%s, %s, %s, %s, %s)
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

        # 6) Update the table cell
        self.table.setItem(row, 5, QTableWidgetItem(f"₱{amount_paid:.2f}"))

        QMessageBox.information(
            self, "Paid",
            f"Ticket {ticket_id}\n"
            f"Vehicle Type: {vehicle_type}\n"
            f"Duration: {hours:.2f} hrs @ ₱{rate_per_hour:.2f}/hr\n"
            f"Amount: ₱{amount_paid:.2f}\n"
            f"Recorded at {now.strftime('%Y-%m-%d %H:%M:%S')}"
    )   






    def submit_data(self):
    
    # Generate VehicleID like "123ABC"
            numbers = ''.join(random.choices(string.digits, k=3))
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            VehicleID = numbers + letters  # e.g., "123ABC"

            # Generate SpaceID like "A1-Y10"
            part1 = random.choice(string.ascii_uppercase)
            part2 = random.choice(string.digits)
            part3 = random.choice(string.ascii_uppercase)
            part4 = ''.join(random.choices(string.digits, k=2))
            SpaceID = f"{part1}{part2}-{part3}{part4}"  # e.g., "A1-Y10"

            paysforID = ''.join(random.choices(string.ascii_uppercase, k=6))

            acquiresID = ''.join(random.choices(string.ascii_uppercase, k=6))

            # Get values from form
            vehicle_type = self.vehicle_type_combo.currentText().strip()
            Ticket_type = self.vehicle_input.text().strip()

            # Input validation
            if vehicle_type == "Vehicle:" or not Ticket_type:
                QMessageBox.warning(self, "Input Error", "Please fill in all fields correctly.")
                return

            try:
                # Connect to MySQL
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="password",  # change this
                    database="parkindgticketdb"
                )
                cursor = conn.cursor()

                # Insert into vehicle table
                sql_vehicle = "INSERT INTO vehicle (VehicleID, TypeofVehicle) VALUES (%s, %s)"
                cursor.execute(sql_vehicle, (VehicleID, vehicle_type))

                # Insert into ticket table
                sql_ticket = "INSERT INTO ticket (TicketID, IssuedDate, VehicleID) VALUES (%s, %s, %s)"
                cursor.execute(sql_ticket, (Ticket_type, date.today(), VehicleID))

                # Insert into parkingspace table
                sql_parking = "INSERT INTO parkingspace (SpaceID, TicketID, VehicleType) VALUES (%s, %s, %s)"
                cursor.execute(sql_parking, (SpaceID, Ticket_type, vehicle_type))

                sql_pays_for = "INSERT INTO pays_for(Paysfor_ID, VehicleID,TicketID,AmountPaid,PaymentDate) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql_pays_for, (paysforID, VehicleID,Ticket_type,0.00,datetime.now()))

                sqlacquires = "INSERT INTO acquires(Acquires_ID, VehicleID,TicketID,EntryTime,PresenceStatus) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sqlacquires, (acquiresID, VehicleID,Ticket_type,datetime.now().time(),True))

                # Commit changes
                conn.commit()
                cursor.close()
                conn.close()

                # Success message
                QMessageBox.information(self, "Success", "Entry added successfully!")
                self.load_table_data()
                # Reset form
                self.vehicle_input.clear()
                self.vehicle_type_combo.setCurrentIndex(0)
                self.addbutton.setEnabled(True)
                self.addframe.hide()

            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Database Error", f"Error: {err}")




        

    def on_cancel(self):
    # hide the add‑frame
        self.addframe.hide()
    # re‑enable the Add button
        self.addbutton.setEnabled(True)


    

    def load_table_data(self):
       

          # Clear existing rows
        self.table.setRowCount(0)

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",   # your password
                database="parkindgticketdb"  # your DB
            )
            cursor = conn.cursor()

            # Select each ticket only once, with latest payment if any
            cursor.execute("""
                SELECT
                v.VehicleID,
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
                JOIN ticket   AS t  ON v.VehicleID = t.VehicleID
                JOIN acquires AS a  ON t.TicketID  = a.TicketID
                ORDER BY a.EntryTime DESC
            """)

            for row_data in cursor.fetchall():
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
        print("clicked")
        self.table.clearSelection()
        self.addframe = QFrame(self)
        self.addframe.setGeometry(100, 100, 400, 200)
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

        self.vehicle_label = QLabel("Ticket:", self.addframe)
        self.vehicle_label.setGeometry(30, 50, 120, 30)
        

# Vehicle Type Text Field
        self.vehicle_input = QLineEdit(self.addframe)
        self.vehicle_input.setGeometry(100, 50, 130, 30)
        

        self.vehicle_input.setStyleSheet("""
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
        self.vehicle_type_combo.setGeometry(250, 50, 100, 30)
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
        self.vehicle_type_combo.addItems(["Vehicle:","     Car", "Motorcycle"])

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
        