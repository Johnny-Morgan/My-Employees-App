import sys, os
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QFont
from PIL import Image

con = sqlite3.connect('employee.db')
cur = con.cursor()
default_image = 'person.png' # for when we don't have picture for employee
person_id = None


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
        self.get_employees()
        self.display_first_record()

    def main_design(self):
        self.setStyleSheet("font-size: 14pt; font-family: Arial Bold;")
        self.employee_list = QListWidget()
        self.employee_list.itemClicked.connect(self.single_click)
        self.btn_new = QPushButton("New")
        self.btn_new.clicked.connect(self.add_employee)
        self.btn_update = QPushButton("Update")
        self.btn_update.clicked.connect(self.update_employee)
        self.btn_delete = QPushButton("Delete")
        self.btn_delete.clicked.connect(self.delete_employee)

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

    # function to select employees from database and display in list
    def get_employees(self):
        query = "SELECT id, first_name, last_name FROM employee"
        employees = cur.execute(query).fetchall()
        for employee in employees:
            self.employee_list.addItem(str(employee[0]) + "-" + employee[1] + " " + employee[2])

    def display_first_record(self):
        query = "SELECT * FROM employee ORDER BY ROWID ASC LIMIT 1"
        employee = cur.execute(query).fetchone()
        image = QLabel()
        image.setPixmap(QPixmap("images/" + employee[5]))  # image at index 5
        first_name = QLabel(employee[1])
        last_name = QLabel(employee[2])
        phone = QLabel(employee[3])
        email = QLabel(employee[4])
        address = QLabel(employee[6])

        self.left_layout.setVerticalSpacing(20)
        self.left_layout.addRow("", image)
        self.left_layout.addRow("First Name: ", first_name)
        self.left_layout.addRow("Last Name: ", last_name)
        self.left_layout.addRow("Phone: ", phone)
        self.left_layout.addRow("Email: ", email)
        self.left_layout.addRow("Address: ", address)

    def single_click(self):
        ###################################################
        # delete employee details from left layout so
        # they can be replaced by employee clicked from list
        for i in reversed(range(self.left_layout.count())):
            widget = self.left_layout.takeAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        ###################################################

        employee = self.employee_list.currentItem().text()
        id = employee.split("-")[0]
        query = ("SELECT * FROM employee WHERE id = ?")
        person = cur.execute(query, (id, )).fetchone() # single item tuple = (1, )
        image = QLabel()
        image.setPixmap(QPixmap("images/" + person[5]))  # image at index 5
        first_name = QLabel(person[1])
        last_name = QLabel(person[2])
        phone = QLabel(person[3])
        email = QLabel(person[4])
        address = QLabel(person[6])

        self.left_layout.setVerticalSpacing(20)
        self.left_layout.addRow("", image)
        self.left_layout.addRow("First Name: ", first_name)
        self.left_layout.addRow("Last Name: ", last_name)
        self.left_layout.addRow("Phone: ", phone)
        self.left_layout.addRow("Email: ", email)
        self.left_layout.addRow("Address: ", address)

    def delete_employee(self):
        if self.employee_list.selectedItems():
            person = self.employee_list.currentItem().text()
            id = person.split("-")[0]
            mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this employee?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
            if mbox == QMessageBox.Yes:
                try:
                    query = "DELETE FROM employee WHERE id = ?"
                    cur.execute(query, (id, ))
                    con.commit()
                    QMessageBox.information(self, "Info", "Employee has been deleted")
                    self.close()
                    self.main = Main()
                except:
                    QMessageBox.information(self, "Warning", "Employee has not been deleted")
        else:
            QMessageBox.information(self, "Warning", "Please select an employee to delete")

    def update_employee(self):
        global person_id
        if self.employee_list.selectedItems():
            person = self.employee_list.currentItem().text()
            person_id = person.split("-")[0]
            self.update_window = UpdateEmployee()
            self.close()
        else:
            QMessageBox.information(self, "Warning", "Please select an employee to update")


class UpdateEmployee(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Employee")
        self.setGeometry(450, 150, 350, 600)
        self.UI()
        self.show()

    def UI(self):
        self.get_person()
        self.main_design()
        self.layouts()

    def closeEvent(self, QCloseEvent):
        self.main = Main()  # open main window after close event

    def get_person(self):
        global person_id
        query = "SELECT * FROM employee WHERE id = ?"
        employee = cur.execute(query, (person_id, )).fetchone()
        self.first_name = employee[1]
        self.last_name = employee[2]
        self.phone = employee[3]
        self.email = employee[4]
        self.image = employee[5]
        self.address = employee[6]

    def main_design(self):
        ##### Top layout widgets #####
        self.setStyleSheet("background-color: white; font-size: 14pt; font-family: Times")
        self.title = QLabel("Update Employee")
        self.title.setStyleSheet('font-size: 24pt; font-family: Arial Bold;')
        self.image_add = QLabel()
        self.image_add.setPixmap(QPixmap('images/{}'.format(self.image)))

        ##### Bottom layout widgets #####
        self.first_name_label = QLabel("First Name: ")
        self.first_name_entry = QLineEdit()
        self.first_name_entry.setText(self.first_name)
        self.last_name_label = QLabel("Last Name: ")
        self.last_name_entry = QLineEdit()
        self.last_name_entry.setText(self.last_name)
        self.phone_label = QLabel("Phone: ")
        self.phone_entry = QLineEdit()
        self.phone_entry.setText(self.phone)
        self.email_label = QLabel("Email: ")
        self.email_entry = QLineEdit()
        self.email_entry.setText(self.email)
        self.image_label = QLabel("Picture: ")
        self.image_button = QPushButton("Browse")
        self.image_button.setStyleSheet("background-color: orange; font-size: 10pt")
        self.image_button.clicked.connect(self.upload_image)
        self.address_label = QLabel("Address: ")
        self.address_editor = QTextEdit()
        self.address_editor.setText(self.address)
        self.update_button = QPushButton("Update")
        self.update_button.setStyleSheet("background-color: orange; font-size: 10pt")
        self.update_button.clicked.connect(self.update_employee)

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
        self.bottom_layout.addRow("", self.update_button)

        ##### Setting main window layout #####
        self.setLayout(self.main_layout)

    def upload_image(self):
        global default_image
        size = (128, 128)
        self.file_name, ok = QFileDialog.getOpenFileName(self, 'Upload Image', '', 'Image Files (*.jpg *.png)')

        if ok:
            default_image = os.path.basename(self.file_name) # gets just actual name of file from location
            image = Image.open(self.file_name)
            image = image.resize(size)
            image.save("images/{}".format(default_image))

    def update_employee(self):
        global default_image
        global person_id
        first_name = self.first_name_entry.text()
        last_name = self.last_name_entry.text()
        phone = self.phone_entry.text()
        email = self.email_entry.text()
        image = default_image
        address = self.address_editor.toPlainText()
        if(first_name and last_name and phone != ""):
            try:
                query = "UPDATE employee SET first_name = ?, last_name = ?, phone = ?, email = ?, image = ?, address = ? WHERE id = ?"
                cur.execute(query, (first_name, last_name, phone, email, image, address, person_id))
                con.commit()
                QMessageBox.information(self, "Success", "Employee has been updated")
                self.close() # close add employee window
                self.main = Main() # open main window
            except:
                QMessageBox.information(self, "Warning", "Employee not updated")
        else:
            QMessageBox.information(self, "Warning", "Fields can not be empty")


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

    def closeEvent(self, QCloseEvent):
        self.main = Main() # open main window after close event

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
        self.image_button.clicked.connect(self.upload_image)
        self.address_label = QLabel("Address: ")
        self.address_editor = QTextEdit()
        self.add_button = QPushButton("Add")
        self.add_button.setStyleSheet("background-color: orange; font-size: 10pt")
        self.add_button.clicked.connect(self.add_employee)

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
        self.bottom_layout.addRow("", self.add_button)

        ##### Setting main window layout #####
        self.setLayout(self.main_layout)

    def upload_image(self):
        global default_image
        size = (128, 128)
        self.file_name, ok = QFileDialog.getOpenFileName(self, 'Upload Image', '', 'Image Files (*.jpg *.png)')

        if ok:
            default_image = os.path.basename(self.file_name) # gets just actual name of file from location
            image = Image.open(self.file_name)
            image = image.resize(size)
            image.save("images/{}".format(default_image))

    def add_employee(self):
        global default_image
        first_name = self.first_name_entry.text()
        last_name = self.last_name_entry.text()
        phone = self.phone_entry.text()
        email = self.email_entry.text()
        image = default_image
        address = self.address_editor.toPlainText()
        if(first_name and last_name and phone != ""):
            try:
                query = "INSERT INTO employee (first_name, last_name, phone, email, image, address) VALUES(?, ?, ?, ?, ?, ?)"
                cur.execute(query, (first_name, last_name, phone, email, image, address))
                con.commit()
                QMessageBox.information(self, "Success", "Employee has been added")
                self.close() # close add employee window
                self.main = Main() # open main window
            except:
                QMessageBox.information(self, "Warning", "Employee not added")

        else:
            QMessageBox.information(self, "Warning", "Fields can not be empty")


def main():
    App = QApplication(sys.argv)
    window = Main()
    sys.exit(App.exec_())


if __name__ == '__main__':
    main()