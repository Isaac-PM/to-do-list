# to-do-list

Simple "to do list" app, using Python, PyQT5, capable of adding, removing, and editing tasks, plus sending email reminders.

***

# About

## Objective
This code is a GUI (Graphical User Interface) implementation of a to-do list application using the `PyQt5` library, also it contains a script for sending emails via the Gmail SMTP server.

## Libraries Used
This code uses the following libraries:
- `PyQt5` for creating the GUI and handling user interactions
- `pickle` for saving and loading data
- `smtplib`, `ssl`, `datetime`, `email.mime.text`, and `email.mime.multipart` for sending emails
- `icalendar` package for creating calendar events that can be sent along with the email.

## User Manual
- To add a new task to the list, enter the task in the "Add Task" text field and click the "Add" button.
- To strike-through a task, select the task in the list and click the "Strike" button.
- To delete a task from the list, select the task in the list and click the "Delete" button.
- The to-do list data is automatically saved upon closing the application and loaded on start-up.
- If an error occurs, an error message will be displayed using a pop-up window.
- The app also includes a function that can be used to send an email with a calendar event attached. The function takes in a dictionary of arguments, including the email address of the recipient, the summary and date of the calendar event, and sends an email with the specified calendar event attached. The function returns a boolean value indicating whether the email was sent successfully.
- The email is sent using the Gmail account `development.test.700@gmail.com`.

> Note: The code uses the uic module to load the ui file and this module is part of PyQt5 package.

# Gallery

## Main window

<center><img   src="https://i.imgur.com/mDOa9OD.png"   width=""   height=""   /></center>

## Main window with tasks

<center><img   src="https://i.imgur.com/C7ar2a1.png"   width=""   height=""   /></center>

## Notification window

<center><img   src="https://i.imgur.com/lEpeL2S.png"   width=""   height=""   /></center>

## Email reminder

<center><img   src="https://i.imgur.com/yrNgufP.png"   width=""   height=""   /></center>

# App icon

By: **hqrloveq**. Retrieved from https://www.flaticon.com/free-icon/check_5610944?term=check&page=1&position=4&origin=tag&related_id=5610944
