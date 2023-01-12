# -*- coding: utf-8 -*-

import sys
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from presentation.notification_manager import *


class Gui(QtWidgets.QMainWindow):
    __instance: uic = None

    @staticmethod
    def get_instance():
        if Gui.__instance is None:
            Gui()
        return Gui.__instance

    def __init__(self):
        super().__init__()
        if Gui.__instance is not None:
            raise Exception("Multiple instances of the gui are not allowed!")
        else:
            try:
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
            except:
                print("Unexpected error:", sys.exc_info()[0])

    def add_item(self) -> None:
        if self.addText.text() == "":
            self.show_popup("Please enter a task!")
            return
        self.row_count += 1
        self.table.setRowCount(self.row_count)
        self.table.setCellWidget(
            self.row_count - 1, 0, QtWidgets.QCheckBox(self.addText.text()))
        self.addText.setText("")

    def strike_item(self) -> None:
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
        selected_row: int = self.table.currentRow()
        if selected_row == -1:
            self.show_popup("Please select a task!")
            return
        self.table.removeRow(selected_row)
        self.row_count -= 1

    def notify(self) -> None:
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
            send_email({"to": email, "summary": summary,
                       "year": year, "month": month, "day": day})
            self.show_popup("Notification sent!",
                            QtWidgets.QMessageBox.Information, "Success!")
            self.popup_window.close()

        # Create email line edit
        email_line_edit = QtWidgets.QLineEdit()
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
        self.popup_window.setWindowIcon(QtGui.QIcon("app/presentation/icon.png"))
        self.popup_window.setLayout(layout)
        self.popup_window.show()

    def show_popup(self, message: str, type: QtWidgets.QMessageBox = QtWidgets.QMessageBox.Warning, title: str = "Warning!") -> None:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()

    def update(self, args: list = []) -> None:
        pass
