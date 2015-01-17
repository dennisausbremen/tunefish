from flask import Flask
from flask.ext.images import Images
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from celery import Celery

from settings import SETTINGS


def make_celery(app):
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context() as app_context:
                return TaskBase.__call__(self, app=app_context.app, *args, **kwargs)

    celery.Task = ContextTask
    return celery


app = Flask(__name__, static_folder='../client/app', template_folder='../client/views')
app.debug = True
app.secret_key = "this_should_be_way_more_secret_like_urandom.its_only_static_for_debug_reasons"
app.config.update(SETTINGS)
celery = make_celery(app)
images = Images(app)

trackPool = UploadSet('trackPool', ('mp3',))
imagePool = UploadSet('imagePool', IMAGES)
techriderPool = UploadSet('techriderPool', ('pdf',))
configure_uploads(app, (trackPool, imagePool, techriderPool,))