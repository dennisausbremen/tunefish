# coding=utf-8

from flask.ext.wtf import Form
from wtforms import PasswordField, validators, StringField, TextAreaField, FileField
from wtforms.validators import InputRequired, Email
from wtforms.fields.html5 import EmailField, TelField, IntegerField, URLField


class LoginForm(Form):
    login = StringField('Login', [InputRequired('Bitte Login eintragen')])
    password = PasswordField('Passwort', [InputRequired('Bitte Passwort eintragen')])


class RegistrationForm(Form):
    login = StringField('Login',
                        [InputRequired("Bitte Login eintragen"), validators.Length(min=4, max=25, message=u'Bitte überprüfe deinen Login (4-25 Zeichen)')])
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
    name = StringField('Name', [InputRequired("Bitte Bandnamen eintragen"), validators.Length(min=2, max=60, message="Der Bandname muss zwischen 2 und 60 Zeichen lang sein.")])
    descp = TextAreaField('Beschreibung', [InputRequired("Bitte Bandbeschreibungstext eintragen"), validators.Length(min=30, max=5000, message="Die Bandbeschreibung muss zwischen %(min)s und %(max)s Zeichen lang sein.")])
    amount_members = IntegerField('Mitglieder', [InputRequired("Bitte Mitgliederanzahl eintragen"), validators.NumberRange(min=1, max=30, message="Anzahl der Bandmitglieder muss zwischen %(min)s und %(max)s liegen.")])
    website = URLField('Website URL', [InputRequired("Bitte Webseite eintragen"), validators.Length(min=6, message="Die Webseite muss mindestens %(min)s Zeichen lang sein.")])
    youtube_id = StringField('YouTube Video ID')
    facebook_page = StringField('facebook')
    phone = TelField('Telefon', [InputRequired("Bitte Telefonnummer eintragen"), validators.Length(min=6, max=30, message="Die Telefonnummer muss zwischen %(min)s und %(max)s Zeichen lang sein.")])
    city = StringField('Stadt', [InputRequired("Bitte Stadt eintragen"), validators.Length(min=2, max=50, message="Der Name der Stadt muss zwischen %(min)s und %(max)s Zeichen lang sein.")])

    def set_from_model(self, band):
        self.name.raw_data = self.name.data = band.name
        self.descp.raw_data = self.descp.data = band.descp
        self.amount_members.data = band.amount_members
        self.amount_members.raw_data = str(band.amount_members)
        self.website.raw_data = self.website.data = band.website
        self.youtube_id.data = band.youtube_id
        self.facebook_page.data = band.facebook_page
        self.phone.raw_data = self.phone.data = band.phone
        self.city.raw_data = self.city.data = band.city

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