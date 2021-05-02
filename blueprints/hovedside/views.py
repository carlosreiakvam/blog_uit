from flask import Blueprint, abort, render_template, request

from models.innlegg import Innlegg

router = Blueprint('hovedside', __name__)


@router.route("/")
def index():
    new10 = Innlegg.get_ten_newest()
    if new10:
        return render_template('index.html',
                               innlegg=new10,
                               no_result_message="Ingen innlegg så langt...")


@router.route("/tag/<tag_navn>")
def tag(tag_navn: str):
    postswithtag = Innlegg.get_with_tag(tag_navn)
    return render_template('index.html',
                           innlegg=postswithtag,
                           no_result_message="Denne taggen har ingen innlegg...")


@router.route("/search", methods=["GET", "POST"])
def search():
    search_string = request.form.get("search-string", "")
    search_result = Innlegg.search(search_string)
    return render_template("index.html", innlegg=search_result,
                           no_result_message="Søket ga desverre ingen resultater...")
