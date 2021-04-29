from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from blueprints.blog.forms import InnleggForm, KommentarForm
from models.blog import Blog
from models.innlegg import Innlegg
from models.tagger import Tagger

router = Blueprint('blog', __name__, url_prefix="/blog")


@router.route("/<blog_prefix>")
def blog(blog_prefix: str):
    postswithtag = Innlegg.get_with_blog_prefix(blog_prefix)
    blog = Blog.get_one(blog_prefix)
    if postswithtag and len(postswithtag) > 0:
        return render_template('blog.html', blog=blog,
                               innlegg=postswithtag)
    return abort(404)


@router.route("/<blog_prefix>/new", methods=["GET", "POST"])
@login_required
def nytt_innlegg(blog_prefix: str):
    form = InnleggForm()
    blog = Blog.get_one(blog_prefix)
    if blog.blog_bruker_navn != current_user.brukernavn:
        flash("Du må være eieren av en blog for å legge inn ett nytt innlegg!")
        return redirect(url_for("hovedside.index"))

    available_tags = Tagger.get_all_available_tags()

    if form.validate_on_submit():
        innlegg = Innlegg(innlegg_tittel=form.tittel.data, innlegg_innhold=form.innhold.data, blog_prefix=blog_prefix)
        innlegg = innlegg.insert()
        for tag in form.tagger.data:
            tag = Tagger(tagnavn=tag, innleggid=innlegg.innlegg_id)
            tag.add_tag()
        return redirect(url_for('hovedside.index'))
    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{fieldName}: {error_message}", "danger")
    return render_template("nytt_innlegg.html", form=form, blog_prefix=blog_prefix, available_tags=available_tags)


@router.route("/<blog_prefix>/<int:innlegg_id>", methods=["GET", "POST"])
def vis_innlegg(blog_prefix: str, innlegg_id: int):
    innlegg = Innlegg.get_one(innlegg_id)

    if innlegg.blog_prefix != blog_prefix:
        abort(404)

    form = KommentarForm()
    if form.validate_on_submit():
        innlegg.add_kommentar(form.innhold.data, current_user.brukernavn)

    return render_template("innlegg.html", innlegg=innlegg, form=form)
