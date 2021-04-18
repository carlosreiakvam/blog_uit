from flask import Blueprint

router = Blueprint('auth', __name__)


@router.route("/")
def example():
    return "hello from auth"
