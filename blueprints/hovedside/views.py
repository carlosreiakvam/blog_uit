
from flask import Blueprint, render_template

router = Blueprint('hovedside', __name__)


@router.route("/")
def example():
    return render_template('base.html')

