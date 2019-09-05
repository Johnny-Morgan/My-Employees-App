import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont

con = sqlite3.connect('employee.db')
cur = con.cursor()


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Employees")
        self.setGeometry(450, 150, 750, 600)
        self.UI()
        self.show()

    def UI(self):
        self.main_design()
        self.layouts()

    def main_design(self):
        self.employee_list = QListWidget()
        self.btn_new = QPushButton("New")
        self.btn_new.clicked.connect(self.add_employee)
        self.btn_update = QPushButton("Update")
        self.btn_delete = QPushButton("Delete")

    def layouts(self):
        ##### Layouts #####
        self.main_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.right_layout = QVBoxLayout()
        self.right_top_layout = QHBoxLayout()
        self.right_bottom_layout = QHBoxLayout()

        ##### Adding child layouts to main layout #####
        self.right_layout.addLayout(self.right_top_layout)
        self.right_layout.addLayout(self.right_bottom_layout)
        self.main_layout.addLayout(self.left_layout, 40)
        self.main_layout.addLayout(self.right_layout, 60)

        ##### Adding widgets to layouts #####
        self.right_top_layout.addWidget(self.employee_list)
        self.right_bottom_layout.addWidget(self.btn_new)
        self.right_bottom_layout.addWidget(self.btn_update)
        self.right_bottom_layout.addWidget(self.btn_delete)

        ##### Setting main window layout #####
        self.setLayout(self.main_layout)

    def add_employee(self):
        self.new_employee = AddEmployee()
        self.close()


class AddEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Employees")
        self.setGeometry(450, 150, 350, 600)
        self.UI()
        self.show()

    def UI(self):
        self.main_design()
        self.layouts()

    def main_design(self):
        ##### Top layout widgets #####
        self.setStyleSheet("background-color: white; font-size: 14pt; font-family: Times")
        self.title = QLabel("Add Employee")
        self.title.setStyleSheet('font-size: 24pt; font-family: Arial Bold;')
        self.image_add = QLabel()
        self.image_add.setPixmap(QPixmap('icons/person.png'))

        ##### Bottom layout widgets #####
        self.first_name_label = QLabel("First Name: ")
        self.first_name_entry = QLineEdit()
        self.first_name_entry.setPlaceholderText("Enter Employee First Name")
        self.last_name_label = QLabel("Last Name: ")
        self.last_name_entry = QLineEdit()
        self.last_name_entry.setPlaceholderText("Enter Employee Last Name")
        self.phone_label = QLabel("Phone: ")
        self.phone_entry = QLineEdit()
        self.phone_entry.setPlaceholderText("Enter Employee Phone No.")
        self.email_label = QLabel("Email: ")
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Enter Employee Email")
        self.image_label = QLabel("Picture: ")
        self.image_button = QPushButton("Browse")
        self.image_button.setStyleSheet("background-color: orange; font-size: 10pt")
        self.address_label = QLabel("Address: ")
        self.address_editor = QTextEdit()
        self.address_button = QPushButton("Add")
        self.address_button.setStyleSheet("background-color: orange; font-size: 10pt")

    def layouts(self):
        ##### Main layouts #####
        self.main_layout = QVBoxLayout()
        self.top_layout = QVBoxLayout()
        self.bottom_layout = QFormLayout()

        ##### Adding child layouts to main layout #####
        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

        ##### Adding widgets to layouts #####
            #### Top Layout ####
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.title)
        self.top_layout.addWidget(self.image_add)
        self.top_layout.addStretch()
        self.title.setContentsMargins(70, 20, 10, 0)
        self.image_add.setContentsMargins(105, 0, 10, 30)
            #### Bottom Layout
        self.bottom_layout.addRow(self.first_name_label, self.first_name_entry)
        self.bottom_layout.addRow(self.last_name_label, self.last_name_entry)
        self.bottom_layout.addRow(self.phone_label, self.phone_entry)
        self.bottom_layout.addRow(self.email_label, self.email_entry)
        self.bottom_layout.addRow(self.image_label, self.image_button)
        self.bottom_layout.addRow(self.address_label, self.address_editor)
        self.bottom_layout.addRow("", self.address_button)

        ##### Setting main window layout #####
        self.setLayout(self.main_layout)

def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()