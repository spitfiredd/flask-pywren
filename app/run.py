from flask import Flask, redirect, url_for


def create_app(config='app.settings'):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config)
    load_blueprints(app)

    @app.route('/')
    def homepage():
        """Set /api/v1/ as home route"""
        return redirect(url_for('api.doc'))

    return app


def load_blueprints(app):
    """Register blueprints."""
    from app.apis import api_v1_bp
    app.register_blueprint(api_v1_bp)
    return None
