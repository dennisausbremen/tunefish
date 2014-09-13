from flask import Blueprint

from server.models import Band


bands = Blueprint('bands', __name__, template_folder='templates')


@bands.route('/', defaults={'id': 1})
@bands.route('/<id>')
def show(id):
    return Band.query.filter(Band.id == id).first().name