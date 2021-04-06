from flask import Flask

from config import config
from extensions import db


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    @app.route('/')
    def hello_world():
        return 'Hello World!'

    return app


if __name__ == '__main__':
    flask_app = create_app(config_name="development")
    flask_app.run()
