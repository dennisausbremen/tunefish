# coding=utf-8

from email.header import Header
from email.mime.text import MIMEText
import smtplib
from flask.templating import render_template

from server.app import celery

SENDER = "noreply@vorstrasse-bremen.de"

@celery.task
def __sendmail(message, app):
    server = smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT'])
    server.starttls()
    server.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

    server.sendmail(SENDER, [message['To']], message.as_string())
    server.quit()


def __prepare_mail(recipient, subject, message_template, *args, **kwargs):
    msg = MIMEText(render_template(message_template, *args, **kwargs), _charset="UTF-8")
    msg['Subject'] = Header(subject, "utf-8")
    msg['From'] = SENDER
    msg['To'] = recipient
    return msg


def send_registration_mail(band):
    msg = __prepare_mail(band.email, "Willkommen %s" % band.name, "mails/registration.txt", band=band)
    __sendmail.delay(msg)


def send_reminder_mail(band):
    msg = __prepare_mail(band.email, "[tunefish] Reminder: Eure Bewerbung ist noch nicht abgeschlossen", "mails/reminder_state_new.txt", band=band)
    __sendmail.delay(msg)


def send_decline_mail(band):
    msg = __prepare_mail(band.email, "[tunefish] Leider hat es dieses Jahr nicht gereicht.", "mails/decline_voted_bands.txt", band=band)
    __sendmail.delay(msg)