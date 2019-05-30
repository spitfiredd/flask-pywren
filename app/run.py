from flask import Flask, redirect, url_for

from app.apis.pywren.tasks import celery


def create_app():
    return create_app_or_celery(mode='app')


def create_celery():
    return create_app_or_celery(mode='celery')


# def create_app(config='app.settings'):
#     app = Flask(__name__, instance_relative_config=True)

#     app.config.from_object(config)
#     load_blueprints(app)

#     @app.route('/')
#     def homepage():
#         """Set /api/v1/ as home route"""
#         return redirect(url_for('api.doc'))

#     return app


def create_app_or_celery(config='app.settings', mode='app'):
    assert isinstance(mode, str), 'bad mode type "{}"'.format(type(mode))
    assert mode in ('app', 'celery'), 'bad mode "{}"'.format(mode)

    app = Flask(__name__)

    app.config.from_object(config)

    configure_celery(app, celery)

    # register blueprints
    load_blueprints(app)

    @app.route('/')
    def homepage():
        """Set /api/v1/ as home route"""
        return redirect(url_for('api.doc'))

    if mode == 'app':
        return app
    elif mode == 'celery':
        return celery


def load_blueprints(app):
    """Register blueprints."""
    from app.apis import api_v1_bp
    app.register_blueprint(api_v1_bp)
    return None


def configure_celery(app, celery):

    # set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    # subclass task base for app context
    # http://flask.pocoo.org/docs/0.12/patterns/celery/
    TaskBase = celery.Task

    class AppContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = AppContextTask

    # run finalize to process decorated tasks
    celery.finalize()
