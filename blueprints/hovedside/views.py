from flask import Blueprint

router = Blueprint('hovedside', __name__)


@router.route("/")
def example():
    return "hello from hovedside"

