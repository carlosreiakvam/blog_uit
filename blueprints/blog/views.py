from flask import Blueprint, redirect, render_template, url_for, flash

from blueprints.blog.forms import InnleggForm
from models.innlegg import Innlegg

router = Blueprint('blog', __name__, url_prefix="/blog")


@router.route("/")
def example():
    return "hello from blog"


@router.route("/<blog_prefix>/new", methods=["GET", "POST"])
def nytt_innlegg(blog_prefix: str):
    form = InnleggForm()

    if form.validate_on_submit():
        innlegg = Innlegg(innlegg_tittel=form.tittel.data, innlegg_innhold=form.innhold.data, blog_prefix=blog_prefix)
        innlegg.insert()
        return redirect(url_for('hovedside.example'))
    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{fieldName}: {error_message}")
    return render_template("nytt_innlegg.html", form=form, blog_prefix=blog_prefix)
