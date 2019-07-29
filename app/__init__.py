from celery import Celery
from flask import Flask

from app.extensions import mail


def create_app_min():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'top-secret!'

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    # app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    # app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', 'fdnhxxpistqiuxdy')

    app.config['MAIL_USERNAME'] = 'todayiate.co@gmail.com'
    app.config['MAIL_PASSWORD'] = 'fdnhxxpistqiuxdy'
    app.config['MAIL_DEFAULT_SENDER'] = 'todayiate.co@gmail.com'

    # Celery configuration
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    # Initialize extensions
    mail.init_app(app)

    return app


def create_app():
    from app.main import main

    app = create_app_min()
    app.register_blueprint(main)

    return app


def create_celery():
    app = create_app_min()
    # Initialize Celery
    celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery
