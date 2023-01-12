# -*- coding: utf-8 -*-

import smtplib
import ssl
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# Requires icalendar package: pip install icalendar
from icalendar import Calendar, Event

"""
Gmail profile:
    - Email: development.test.700@gmail.com
    - Password: nozx taub jlqc vhus
"""


def send_email(args: dict = None) -> None:
    # Setting up the email receiver and sender
    port = 465
    smtp_server = "smtp.gmail.com"
    sender_email = "development.test.700@gmail.com"
    receiver_email = args["to"]
    password = "nozx taub jlqc vhus"

    # Creating the email message
    msg = MIMEMultipart()

    html = """
    <html>
      <head>
        <style>
          h1 {
            color: slategray;
          }
          p {
            font-size: 20px;
            color: black;
          }
        </style>
      </head>
      <body>
          <h1> A new tasks has been created!</h1>
          <p>Here is the calendar appointment &#128526;</p>
      </body>
    </html>
    """
    msg.attach(MIMEText(html, 'html'))

    # Creating the calendar event
    cal = Calendar()
    event = Event()
    event.add('summary', args["summary"])
    year = int(args["year"])
    month = int(args["month"])
    day = int(args["day"])
    event.add('dtstart', datetime.datetime(year, month, day, 0, 0, 0))
    event.add('dtend', datetime.datetime(year, month, day, 23, 59, 59))
    event.add('dtstamp', datetime.datetime.now())
    cal.add_component(event)

    # Attaching the calendar event to the email message
    ics = MIMEText(cal.to_ical().decode(), "calendar;method=REQUEST")
    ics.add_header('Content-Disposition', 'attachment', filename='invite.ics')
    msg.attach(ics)

    # Sending the email
    msg['Subject'] = "New task!"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg, from_addr=sender_email,
                            to_addrs=receiver_email)
