
from flask import render_template, Flask, Blueprint
router = Blueprint('error', __name__, url_prefix="/error")

@router.route("/")
def page_not_found(e):
  return render_template('error.html'), 404

def create_app(config_filename):
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    return app