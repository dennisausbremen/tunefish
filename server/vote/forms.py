# coding=utf-8

from flask.ext.wtf import Form
from wtforms import PasswordField, validators, StringField, TextAreaField
from wtforms.fields.simple import HiddenField
from wtforms.validators import InputRequired


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

class CommentForm(Form):
    band_id = HiddenField('band')
    message = TextAreaField('Kommentar', [InputRequired("Bitte Kommentar eingeben"), validators.Length(min=2, max=1000, message="Die Bandbeschreibung muss zwischen %(min)s und %(max)s Zeichen lang sein.")])

