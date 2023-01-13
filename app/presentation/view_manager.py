# -*- coding: utf-8 -*-

import sys
import pickle
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from presentation.notification_manager import *
from presentation.task import Task


class Gui(QtWidgets.QMainWindow):
    __instance: uic = None

    @staticmethod
    def get_instance():
        if Gui.__instance is None:
            Gui()
        return Gui.__instance

    def __init__(self) -> None:
        super().__init__()
        if Gui.__instance is not None:
            raise Exception("Multiple instances of the gui are not allowed!")
        else:
            try:
                # Data
                self.saved_email: str = ""
                self.tasks: list[Task] = []

                # Read UI file
                Gui.__instance = uic.loadUi("app/presentation/view.ui", self)

                # Widget listeners
                self.addPushButton.clicked.connect(self.add_item)
                self.strikePushButton.clicked.connect(self.strike_item)
                self.deletePushButton.clicked.connect(self.delete_item)
                self.notifyPushButton.clicked.connect(self.notify)

                # Table configuration
                self.column_count: int = 1
                self.row_count: int = 0
                self.table.setColumnCount(self.column_count)
                self.table.setRowCount(self.row_count)
                header = self.table.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                self.table.setHorizontalHeaderLabels(['Tasks'])

                # Notification popup window
                self.popup_window = None

                # Loading data
                self.load_data()
            except:
                print("Unexpected error:", sys.exc_info()[0])

    def add_item(self) -> None:
        """This method adds a new task to the to-do list.
        """
        if self.addText.text() == "":
            self.show_popup("Please enter a task!")
            return
        self.row_count += 1
        self.table.setRowCount(self.row_count)
        self.table.setCellWidget(
            self.row_count - 1, 0, QtWidgets.QCheckBox(self.addText.text()))
        self.addText.setText("")

    def strike_item(self) -> None:
        """This method strikethroughs a task in the to-do list.
        """
        selected_row: int = self.table.currentRow()
        if selected_row == -1:
            self.show_popup("Please select a task!")
            return
        font = self.table.cellWidget(selected_row, 0).font()
        if font.strikeOut():
            font.setStrikeOut(False)
        else:
            font.setStrikeOut(True)
        self.table.cellWidget(selected_row, 0).setFont(font)

    def delete_item(self) -> None:
        """This method deletes a task from the to-do list.
        """
        selected_row: int = self.table.currentRow()
        if selected_row == -1:
            self.show_popup("Please select a task!")
            return
        self.table.removeRow(selected_row)
        self.row_count -= 1

    def save_data(self):
        """This method saves the data of the to-do list.
        """
        try:
            with open("app/presentation/email.pickle", "wb") as file:
                pickle.dump(self.saved_email, file)
        except:
            print("Unexpected error:", sys.exc_info()[0])
        try:
            with open("app/presentation/tasks.pickle", "wb") as file:
                self.tasks = []
                for row in range(self.row_count):
                    font = self.table.cellWidget(row, 0).font()
                    striken = font.strikeOut()
                    is_done = self.table.cellWidget(row, 0).isChecked()
                    description = self.table.cellWidget(row, 0).text()
                    self.tasks.append(Task(description, striken, is_done))
                pickle.dump(self.tasks, file)
        except:
            print("Unexpected error:", sys.exc_info()[0])

    def load_data(self):
        """This method loads the data of the to-do list.
        """
        try:
            with open("app/presentation/email.pickle", "rb") as file:
                self.saved_email = pickle.load(file)
                print(self.saved_email)
        except:
            self.saved_email = ""
        try:
            with open("app/presentation/tasks.pickle", "rb") as file:
                self.tasks = pickle.load(file)
                print(self.tasks)
                for task in self.tasks:
                    self.row_count += 1
                    self.table.setRowCount(self.row_count)
                    self.table.setCellWidget(
                        self.row_count - 1, 0, QtWidgets.QCheckBox(task.description))
                    font = self.table.cellWidget(self.row_count - 1, 0).font()
                    font.setStrikeOut(task.stricken)
                    self.table.cellWidget(self.row_count - 1, 0).setFont(font)
                    self.table.cellWidget(
                        self.row_count - 1, 0).setChecked(task.is_done)
        except:
            self.tasks = []

    def notify(self) -> None:
        """This method creates a popup window to set the notification settings.
        """
        selected_row: int = self.table.currentRow()
        if selected_row == -1:
            self.show_popup("Please select a task!")
            return

        summary: str = self.table.cellWidget(selected_row, 0).text()

        # Create popup window
        self.popup_window = QtWidgets.QDialog()
        self.popup_window.setWindowTitle("Notification settings")
        self.popup_window.setFixedSize(300, 200)
        self.popup_window.setModal(True)

        # Popup window controller
        def on_ok_clicked():
            email: str = email_line_edit.text()
            date: str = calendar_widget.selectedDate()
            year: str = str(date.year())
            month: str = str(date.month())
            day: str = str(date.day())
            if email == "":
                self.show_popup("Please enter an email!")
                return
            reponse: bool = send_email(
                {"to": email, "summary": summary, "year": year, "month": month, "day": day})
            if not reponse:
                self.show_popup("Something went wrong!",
                                QtWidgets.QMessageBox.Critical, "Error!")
            else:
                self.show_popup("Notification sent!",
                                QtWidgets.QMessageBox.Information, "Success!")
            self.saved_email = email
            self.popup_window.close()

        # Create email line edit
        email_line_edit = QtWidgets.QLineEdit()
        if self.saved_email != "":
            email_line_edit.setText(self.saved_email)
        else:
            email_line_edit.setPlaceholderText("Email")

        # Create calendar widget
        calendar_widget = QtWidgets.QCalendarWidget()

        # Create OK button
        ok_button = QtWidgets.QPushButton("OK")
        ok_button.clicked.connect(on_ok_clicked)

        # Create layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(email_line_edit)
        layout.addWidget(calendar_widget)
        layout.addWidget(ok_button, alignment=Qt.AlignRight)
        self.popup_window.setWindowIcon(
            QtGui.QIcon("app/presentation/icon.png"))
        self.popup_window.setLayout(layout)
        self.popup_window.show()

    def show_popup(self, message: str, type: QtWidgets.QMessageBox = QtWidgets.QMessageBox.Warning, title: str = "Warning!") -> None:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def closeEvent(self, event):
        self.save_data()
