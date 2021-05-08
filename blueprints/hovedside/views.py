from flask import Blueprint, abort, render_template, request

from models.innlegg import Innlegg
from models.tagger import Tagger

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
    posts_with_tag = Innlegg.get_with_tag(tag_navn)
    return render_template('index.html',
                           innlegg=posts_with_tag,
                           no_result_message="Denne taggen har ingen innlegg...")


@router.route("/search", methods=["GET", "POST"])
def search():
    search_string = request.form.get("search-string", "")
    search_result = Innlegg.search(search_string)
    return render_template("index.html", innlegg=search_result,
                           no_result_message="Søket ga desverre ingen resultater...")

@router.route("/tag/list_all")
def list_all_tags():
    all_tags = Tagger.tag_usage()

    return render_template('taglist.html', alltags=all_tags)

@router.route("/most_views")
def most_hit_posts():
    most_hits = Innlegg.get_ten_most_hits()

    return render_template('index.html', innlegg=most_hits)

@router.route("/newest_posts")
def newest_posts():
    newest_posts = Innlegg.get_ten_newest()

    return render_template('index.html', innlegg=newest_posts)
