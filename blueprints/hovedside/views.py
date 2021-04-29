from flask import Blueprint, render_template, abort
from models.innlegg import Innlegg
from models.blog import Blog

router = Blueprint('hovedside', __name__)


@router.route("/")
def index():
    new10 = Innlegg.get_ten_newest()
    if new10:
        return render_template('index.html',
                               innlegg=new10, sidetittel="Le blöög")


@router.route("/tag/<tag_navn>")
def tag(tag_navn: str):
    postswithtag = Innlegg.get_with_tag(tag_navn)
    if postswithtag and len(postswithtag) > 0:
        return render_template('index.html',
                               innlegg=postswithtag)
    return abort(404)
