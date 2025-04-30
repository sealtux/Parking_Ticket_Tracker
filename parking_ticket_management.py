from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel,
    QPushButton, QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox
)
from PyQt6.QtCore import Qt
import sys


class ParkingTicketManagement(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parking Ticket Management")
        self.setGeometry(100, 100, 1100, 700)
        
        # Main container
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Parking Ticket Management")
        title_label.setStyleSheet("font-size: 24px; font-weight: 600; color: #333333;")
        add_ticket_btn = QPushButton("Add New Ticket")
        add_ticket_btn.setStyleSheet(
            "background-color: #4576f2; color: #ffffff; padding: 8px 16px; border-radius: 4px;"
        )
        header_layout.addWidget(title_label)
        header_layout.addWidget(add_ticket_btn)
        main_layout.addLayout(header_layout)

        # Search Section
        search_layout = QHBoxLayout()
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search by plate or location...")
        search_input.setStyleSheet(
            "border: 1px solid #e1e4e8; padding: 8px 16px; border-radius: 4px; color: #999999;"
        )
        status_filter = QComboBox()
        status_filter.addItems(["All Status", "Pending", "Paid", "Contested"])
        status_filter.setStyleSheet(
            "background-color: #d9d9d9; padding: 8px 16px; border-radius: 4px; color: #000000;"
        )
        search_layout.addWidget(search_input)
        search_layout.addWidget(status_filter)
        main_layout.addLayout(search_layout)

        # Tickets Table
        self.tickets_table = QTableWidget()
        self.tickets_table.setColumnCount(8)
        self.tickets_table.setHorizontalHeaderLabels([
            "Ticket ID", "License Plate", "Violation", "Location",
            "Amount", "Status", "Date", "Actions"
        ])
        self.tickets_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tickets_table.setStyleSheet("border: none;")
        main_layout.addWidget(self.tickets_table)

        # Populate table with sample data
        self.populate_table()

    def populate_table(self):
        sample_data = [
            ["#1", "ABC123", "Expired Meter", "Main St", "$50", "Pending", "2024-01-20"],
            ["#2", "XYZ789", "No Parking Zone", "Oak Ave", "$75", "Paid", "2024-01-19"],
            ["#3", "DEF456", "Handicap Space", "Pine Rd", "$200", "Contested", "2024-01-18"],
        ]

        self.tickets_table.setRowCount(len(sample_data))
        for row, ticket in enumerate(sample_data):
            for col, value in enumerate(ticket):
                item = QTableWidgetItem(value)
                if col == 5:  # Status column
                    if value == "Pending":
                        item.setForeground(Qt.GlobalColor.darkYellow)
                    elif value == "Paid":
                        item.setForeground(Qt.GlobalColor.darkGreen)
                    elif value == "Contested":
                        item.setForeground(Qt.GlobalColor.red)
                self.tickets_table.setItem(row, col, item)

            # Add actions column
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(5)

            status_dropdown = QComboBox()
            status_dropdown.addItems(["Pending", "Paid", "Contested"])
            status_dropdown.setCurrentText(ticket[5])
            status_dropdown.setStyleSheet(
                "background-color: #d9d9d9; padding: 4px 8px; border-radius: 4px; color: #000000;"
            )
            delete_btn = QPushButton("Delete")
            delete_btn.setStyleSheet(
                "color: #cf222e; border: 1px solid #e1e4e8; padding: 5px 9px; border-radius: 4px;"
            )
            actions_layout.addWidget(status_dropdown)
            actions_layout.addWidget(delete_btn)
            actions_widget.setLayout(actions_layout)
            self.tickets_table.setCellWidget(row, 7, actions_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ParkingTicketManagement()
    window.show()
    sys.exit(app.exec())