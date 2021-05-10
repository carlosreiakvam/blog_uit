from flask import Flask

from blueprints.auth import router as auth_blueprint
from blueprints.blog import router as blog_blueprint
from blueprints.hovedside import router as hovedside_blueprint
from blueprints.vedlegg import router as vedlegg_blueprint
from config import config
from errors import page_not_found, unauthorized, internal_server_error
from extensions import ck, csrf, db, login_manager
from models.bruker import Bruker


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    ck.init_app(app)
    csrf.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Bruker.get_user(user_id)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(hovedside_blueprint)
    app.register_blueprint(blog_blueprint)
    app.register_blueprint(vedlegg_blueprint)

    app.register_error_handler(404, page_not_found)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(500, internal_server_error)

    return app


if __name__ == '__main__':
    flask_app = create_app(config_name="development")
    flask_app.run()
