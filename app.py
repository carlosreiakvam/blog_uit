from flask import Flask

from blueprints.auth import router as auth_blueprint
from config import config
from extensions import db, login_manager


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    app.register_blueprint(auth_blueprint)

    return app


if __name__ == '__main__':
    flask_app = create_app(config_name="development")
    flask_app.run()
