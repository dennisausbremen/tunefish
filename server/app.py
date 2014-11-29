from flask import Flask
from flask_mail import Mail
from settings import SETTINGS

app = Flask(__name__, static_folder='../client/app', template_folder='../client/views')
app.debug = True
app.secret_key = "this_should_be_way_more_secret_like_urandom.its_only_static_for_debug_reasons"
app.config.update(SETTINGS)

mailer = Mail(app)
