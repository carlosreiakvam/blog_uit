from flask import Flask, render_template

from blueprints.auth import router as auth_blueprint
from blueprints.hovedside import router as hovedside_blueprint
from blueprints.blog import router as blog_blueprint
from blueprints.vedlegg import router as vedlegg_blueprint
from config import config
from extensions import db, login_manager, ck, csrf
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

    return app


if __name__ == '__main__':
    flask_app = create_app(config_name="development")
    flask_app.run()
