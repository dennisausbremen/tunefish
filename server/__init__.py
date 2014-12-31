# coding=utf-8

from flask import Blueprint
from server.landingpage import LandingPage

root_blueprint = Blueprint('root', __name__, template_folder='../../client/views')

root_blueprint.add_url_rule('/', view_func=LandingPage.as_view('landingpage'))