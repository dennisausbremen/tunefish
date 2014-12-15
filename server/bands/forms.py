# coding=utf-8

from flask.ext.wtf import Form
from wtforms import PasswordField, validators, StringField, TextAreaField, FileField
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField


class TunefishForm(Form):
    errors = []

    def getErrors(self):
        return self.errors

    def addError(self, field):
        for error in field.errors:
            self.errors.append([error, field.name])

    
class LoginForm(Form):

    login = StringField('Login', [InputRequired('Bitte Login eintragen')])
    password = PasswordField('Passwort', [InputRequired('Bitte Passwort eintragen')])


class RegistrationForm(Form):
    login = StringField('Login',
                        [InputRequired("Bitte Login eintragen"), validators.Length(min=4, max=25, message=u'Bitte überprüfe deinen Login (4-26 Zeichen)')])
    email = EmailField("Email", [InputRequired("Bitte E-Mail Adresse eintragen"), Email("Bitte überprüfe deine E-Mail Adresse")])
    password = PasswordField('Passwort', [
        InputRequired('Bitte Passwort eintragen'),
        validators.Length(min=6, message=u'Bitte überprüfe dein Passwort (mind. 6 Zeichen)'),
    ])
    confirm = PasswordField('Passwort wiederholen', [
        InputRequired('Bitte Passwort wiederholen'),
        validators.EqualTo('password', message=u'Passwörter müssen identisch sein')
    ])


class BandForm(Form):
    name = StringField('BandName', [validators.Length(min=2, max=60)])
    descp = TextAreaField('Band-Beschreibung', [validators.Length(min=30)])
    amount_members = StringField('Anzahl Bandmitglieder', [validators.Length(min=1, max=10)])
    website = StringField('Webseite', [validators.Length(min=6)])
    youtube_id = StringField('Youtube VideoID', [validators.Length(min=6)])
    facebook_page = StringField('facebook Seite')
    phone = StringField('Telefon', [validators.Length(min=6)])
    city = StringField('Stadt', [validators.Length(min=3)])

    def set_from_model(self, band):
        self.name.data = band.name
        self.descp.data = band.descp
        self.amount_members.data = band.amount_members
        self.website.data = band.website
        self.youtube_id.data = band.youtube_id
        self.facebook_page.data = band.facebook_page
        self.phone.data = band.phone
        self.city.data = band.city

    def apply_to_model(self, band):
        band.name = self.name.data
        band.descp = self.descp.data
        band.amount_members = self.amount_members.data
        band.website = self.website.data
        band.youtube_id = self.youtube_id.data
        band.facebook_page = self.facebook_page.data
        band.phone = self.phone.data
        band.city = self.city.data


class TrackUploadForm(Form):
    audioFile = FileField('Audiodatei', [validators.DataRequired(message=u'Sie müssen eine Datei hochladen.')])


class ImageUploadForm(Form):
    image_file = FileField('Bild', [validators.DataRequired(message=u'Sie müssen eine Datei hochladen.')])

class TechriderUploadForm(Form):
    techriderFile = FileField('Techrider', [validators.DataRequired(message=u'Sie müssen eine Datei hochladen.')])