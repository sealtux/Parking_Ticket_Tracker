from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem
import sys

class student_table(QTableWidget):
    def __init__(self, parent=None, headers=None):
        super().__init__(parent)
        if headers:
            self.setColumnCount(len(headers))
            self.setHorizontalHeaderLabels(headers)
        self.setRowCount(0)

    def add_row(self, data: list[str]):
        row = self.rowCount()
        self.insertRow(row)
        for col, value in enumerate(data):
            self.setItem(row, col, QTableWidgetItem(value))