# coding=utf-8
from email.header import Header
from email.mime.text import MIMEText
import smtplib

from server.app import celery
from server.models import Band

SENDER = "noreply@vorstrasse-bremen.de"
BASE_URL = "http://0.0.0.0:5000"
REG_MAIL_BODY = u"""Hallo %s,


willkommnen bei der Sommerfest Auswahl. Um deine Bewerbung abschließen zu können, musst du zuerst deine E-Mail
bestätigen. Klick hierzu einfach auf folgenden Link: %s/bands/confirm/%s


Viele Grüße
SoFe Orga '15
"""


def sendmail(config, recepient, subject, message):
    server = smtplib.SMTP(config['MAIL_SERVER'], config['MAIL_PORT'])
    server.starttls()
    server.login(config['MAIL_USERNAME'], config['MAIL_PASSWORD'])

    msg = MIMEText(message, _charset="UTF-8")
    msg['Subject'] = Header(subject, "utf-8")
    msg['From'] = SENDER
    msg['To'] = recepient

    server.sendmail(SENDER, [recepient], msg.as_string())
    server.quit()



@celery.task
def send_registration_mail(band_id, app):
    band = Band.query.get(band_id)
    if band:
        sendmail(app.config, band.email, "Willkommen %s" % band.login, REG_MAIL_BODY % (band.login, BASE_URL, band.email_confirmation_token))

