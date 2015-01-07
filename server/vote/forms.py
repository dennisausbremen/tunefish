# coding=utf-8

from flask.ext.wtf import Form
from wtforms import PasswordField, validators, StringField, TextAreaField, FileField
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField, TelField, IntegerField, URLField

class UserRegistrationForm(Form):
    login = StringField('Login',
                        [InputRequired("Bitte Login eintragen"), validators.Length(min=4, max=25, message=u'Bitte überprüfe deinen Login (4-25 Zeichen)')])
    password = PasswordField('Passwort', [
        InputRequired('Bitte Passwort eintragen'),
        validators.Length(min=6, message=u'Bitte überprüfe dein Passwort (mind. 6 Zeichen)'),
    ])
    confirm = PasswordField('Passwort wiederholen', [
        InputRequired('Bitte Passwort wiederholen'),
        validators.EqualTo('password', message=u'Passwörter müssen identisch sein')
    ])
