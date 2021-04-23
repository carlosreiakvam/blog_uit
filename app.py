from flask import Flask

from blueprints.auth import router as auth_blueprint
from blueprints.hovedside import router as hovedside_blueprint
from config import config
from extensions import db, login_manager
from models.bruker import Bruker


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Bruker.get_user(user_id)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(hovedside_blueprint)

    return app


if __name__ == '__main__':
    flask_app = create_app(config_name="development")
    flask_app.run()
