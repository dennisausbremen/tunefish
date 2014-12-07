# coding=utf-8

from uuid import uuid4
from flask import request
from flask_mail import Message
from server.app import mailer
from server.models import db


REG_MAIL_BODY = u"""Hallo %s,


willkommnen bei der Sommerfest Auswahl. Um deine Bewerbung abschließen zu können, musst du zuerst deine E-Mail
bestätigen. Klick hierzu einfach auf folgenden Link: %sbands/confirm/%s


Viele Grüße
SoFe Orga '15
"""


def reset_mail(band):
    # todo check if uuid is unique?
    band.is_email_confirmed = False
    band.email_confirmation_token = str(uuid4())
    db.session.commit()


def send_registration_mail(band):
    msg = Message("Willkommen %s" % band.login,
                  sender="noreply@vorstrasse-bremen.de",
                  recipients=[band.email],
                  body=REG_MAIL_BODY % (band.login, request.url_root, band.email_confirmation_token))
    mailer.send(msg)