import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QFrame, QLabel, 
    QStackedWidget, QGridLayout, 
    QTableWidget, QTableWidgetItem, QDialog,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor

def testing():
    # Create a new QTableWidget instance
    table = QTableWidget()
    
    # Set the column count
    table.setColumnCount(5)
    
    # Set the horizontal header labels
    table.setHorizontalHeaderLabels(["ID", "Dormitory Name", "Owner Name", "Phone", "Actions"])
    table.setColumnWidth(2, 240)
    # Styling
    table.setStyleSheet('''
    QTableWidget {
      background-color: #ffffff;
      border: 1px solid #E5E7EB;
      border-radius: 6px;
      gridline-color: #E5E7EB;
      color: #333333;
      font-size: 14px;
      margin: 0;
      padding: 0;
      width: 100%;
    }

    QTableWidget::item {
        padding: 8px;
        max-width: 0; /* Set max-width to 0 to allow the column to expand */
    }

    QHeaderView::section {
        background-color: #F3F4F6;
        color: #1F2937;
        border: none;
        font-weight: bold;
        padding: 6px;
        /* Set the minimum width to 0 to allow the column to expand */
        min-width: 0;
        /* Set the width to 0 to allow the column to expand */
        width: 0;
    }

    QTableWidget QTableCornerButton::section {
      background-color: #F3F4F6;
    }
    
    ''')
    # Return the table
    return table

if __name__ == "__main__":
    # Create the main application
    app = QApplication(sys.argv)

    # Create the main window
    window = QWidget()
    window.setWindowTitle("Dormitory Management")
    window.setStyleSheet('''
      QWidget {
          background-color: #fff;
      }
    ''')

    # Create the layout and add the table
    layout = QVBoxLayout()
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(20)
    window.setLayout(layout)

    table = testing()
    layout.addWidget(table)

    # Add some sample data to the table
    for row in range(3):
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        table.setItem(row, 1, QTableWidgetItem(f"Dormitory {row + 1}"))
        table.setItem(row, 2, QTableWidgetItem(f"Owner {row + 1}"))
        table.setItem(row, 3, QTableWidgetItem(f"123456{row + 1}"))

        # Add the Edit and Delete buttons
        edit_button = QPushButton("Edit")
        delete_button = QPushButton("Delete")

        action_layout = QHBoxLayout()
        action_layout.addWidget(edit_button)
        action_layout.addWidget(delete_button)

        action_widget = QWidget()
        action_widget.setLayout(action_layout)
        table.setCellWidget(row, 4, action_widget)

    # Show the main window
    window.show()
    app.exec()  