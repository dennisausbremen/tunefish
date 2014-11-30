# coding=utf-8

from wtforms import PasswordField, validators, StringField, TextAreaField, FileField
from flask_wtf import Form


class LoginForm(Form):
    login = StringField('Login', [validators.DataRequired()])
    password = PasswordField('Passwort', [validators.DataRequired()])


class RegistrationForm(Form):
    login = StringField('Login',
                        [validators.Length(min=4, max=25, message="Login muss zwischen 4 und 25 Zeichen lang sein")])
    email = StringField('E-Mail Adresse', [
        validators.Length(min=6, max=35, message=u'Die E-Mail Adresse muss zwischen 6 und 36 Zeichen lang sein.'),
        validators.Email(message=u'Die angegebene E-Mail Adresse ist ungültig.')])
    password = PasswordField('Passwort', [
        validators.Length(min=6, message=u'Das gewählte Passwort muss mindestens 6 Zeichen lang sein.'),
        validators.EqualTo('confirm', message=u'Passwörter müssen identisch sein')
    ])
    confirm = PasswordField('Passwort wiederholen', [validators.EqualTo('password', message='')])


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
    trackname = StringField('Trackname', [validators.Length(min=2, message=u'Bitte geben Sie dem Track einen Namen.')])
