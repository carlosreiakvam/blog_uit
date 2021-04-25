
from flask import Blueprint
router = Blueprint('blog', __name__, url_prefix="/blog")


@router.route("/")
def example():
    return "hello from blog"


