from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from blueprints.blog.forms import InnleggForm, KommentarForm, BloggForm
from models.blog import Blog
from models.innlegg import Innlegg
from models.kommentar import Kommentar
from models.tag import Tagger

router = Blueprint('blog', __name__, url_prefix="/blog")


@router.route("/list_all")
def list_all_blogs():
    all_blogs = Blog.get_all()

    return render_template('bloglist.html', allblogs=all_blogs)


@router.route("/<blog_prefix>")
def show_blog(blog_prefix: str):
    posts_with_tag = Innlegg.get_with_blog_prefix(blog_prefix)
    blog = Blog.get_one(blog_prefix)
    if not blog:
        abort(404)
    if posts_with_tag and len(posts_with_tag) > 0:
        return render_template('blog.html', blog=blog,
                               innlegg=posts_with_tag)
    if len(posts_with_tag) == 0:
        return render_template('blog.html', blog=blog, innlegg=None)

    abort(404)


@router.route("/new_blog", methods=["GET", "POST"])
@login_required
def new_blog():
    form = BloggForm()
    if form.validate_on_submit():
        blog = Blog.get_one(form.blog_prefix.data)
        if blog:
            flash("Dette prefikset er allerede tatt", 'danger')
            return render_template('new_blog.html', form=form)
        blog = Blog(blog_navn=form.blog_navn.data, blog_prefix=form.blog_prefix.data,
                    bruker_navn=current_user.brukernavn)
        blog.insert_blog()
        return redirect(url_for("hovedside.index"))

    return render_template('new_blog.html', form=form)


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
        return redirect(url_for('blog.vis_innlegg', blog_prefix=blog_prefix, innlegg_id=innlegg.innlegg_id))
    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{fieldName}: {error_message}", "danger")
    return render_template("nytt_innlegg.html", form=form, blog_prefix=blog_prefix, available_tags=available_tags)


@router.route("/<blog_prefix>/<int:innlegg_id>/rediger", methods=["GET", "POST"])
@login_required
def rediger_innlegg(blog_prefix: str, innlegg_id: int):
    form = InnleggForm()
    blog = Blog.get_one(blog_prefix)
    if blog.blog_bruker_navn != current_user.brukernavn:
        abort(401)

    if form.validate_on_submit():
        innlegg = Innlegg.get_one(innlegg_id)
        innlegg.innlegg_tittel = form.tittel.data
        innlegg.innlegg_innhold = form.innhold.data
        innlegg = innlegg.update()
        tagger = [tag.tagnavn for tag in innlegg.tagger]
        for tag in form.tagger.data:
            if tag not in tagger:
                tag = Tagger(tagnavn=tag, innleggid=innlegg.innlegg_id)
                tag.add_tag()
        for tag in innlegg.tagger:
            if tag.tagnavn not in form.tagger.data:
                tag.delete_tag()
        return redirect(url_for('blog.vis_innlegg', blog_prefix=blog_prefix, innlegg_id=innlegg_id))

    for fieldName, error_messages in form.errors.items():
        for error_message in error_messages:
            flash(f"{fieldName}: {error_message}", "danger")

    innlegg = Innlegg.get_one(innlegg_id)
    form.tagger.data = [tag.tagnavn for tag in innlegg.tagger]
    form.tittel.data = innlegg.innlegg_tittel
    form.innhold.data = innlegg.innlegg_innhold

    available_tags = Tagger.get_all_available_tags_not_used_in_post(innlegg_id)

    return render_template("nytt_innlegg.html", form=form, blog_prefix=blog_prefix, available_tags=available_tags,
                           innlegg_id=innlegg_id)


@router.route("/<blog_prefix>/<int:innlegg_id>", methods=["GET", "POST"])
def vis_innlegg(blog_prefix: str, innlegg_id: int):
    innlegg = Innlegg.get_one(innlegg_id)

    if innlegg.blog_prefix != blog_prefix:
        abort(404)

    Innlegg.update_hit(innlegg_id)

    form = KommentarForm()
    if form.validate_on_submit():
        innlegg.add_kommentar(form.innhold.data, current_user.brukernavn)

    return render_template("innlegg.html", innlegg=innlegg, form=form)


@router.route("/<blog_prefix>/<int:innlegg_id>/slett")
def slett_innlegg(blog_prefix: str, innlegg_id: int):
    innlegg = Innlegg.get_one(innlegg_id)

    if innlegg.blog_prefix != blog_prefix:
        abort(404)

    innlegg.delete()
    flash("Innlegget er slettet!", 'success')

    return redirect(url_for("blog.show_blog", blog_prefix=blog_prefix))


@router.route("/slett_kommentar/<int:kommentar_id>")
def slett_kommentar(kommentar_id: int):
    kommentar = Kommentar.get_kommentar(kommentar_id)
    innlegg = Innlegg.get_one(kommentar.innlegg_id)
    if (kommentar.brukernavn == current_user.brukernavn) or (innlegg.bruker.brukernavn == current_user.brukernavn):
        kommentar.delete_kommentar()
        flash("Kommentar slettet!", "success")
        return redirect(innlegg.url)
    else:
        abort(401)
