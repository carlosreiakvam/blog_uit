from flask import Blueprint, redirect, render_template, url_for, flash

from blueprints.blog.forms import InnleggForm
from models.blog import Blog
from models.innlegg import Innlegg
from models.tagger import Tagger
from flask_login import current_user, login_required

router = Blueprint('blog', __name__, url_prefix="/blog")


@router.route("/")
def example():
    return "hello from blog"


@router.route("/<blog_prefix>/new", methods=["GET", "POST"])
@login_required
def nytt_innlegg(blog_prefix: str):
    form = InnleggForm()
    blog = Blog.get_one(blog_prefix)
    if blog.blog_bruker_navn != current_user.brukernavn:
        flash("Du må være eieren av en blog for å legge inn ett nytt innlegg!")
        return redirect(url_for("hovedside.example"))

    available_tags = Tagger.get_all_available_tags()

    if form.validate_on_submit():
        innlegg = Innlegg(innlegg_tittel=form.tittel.data, innlegg_innhold=form.innhold.data, blog_prefix=blog_prefix)
        innlegg = innlegg.insert()
        print(form.tagger.data)
        for tag in form.tagger.data:
            print(tag)
            tag = Tagger(tagnavn=tag, innleggid=innlegg.innlegg_id)
            tag.add_tag()
        return redirect(url_for('hovedside.example'))
    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{fieldName}: {error_message}")
    return render_template("nytt_innlegg.html", form=form, blog_prefix=blog_prefix, available_tags=available_tags)
