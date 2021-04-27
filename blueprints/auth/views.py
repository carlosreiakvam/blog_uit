from urllib.parse import urljoin, urlparse

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import login_user

from blueprints.auth.forms import LoginForm
from models.bruker import Bruker

router = Blueprint('auth', __name__, url_prefix="/auth")


@router.route("/")
def example():
    return "hello from auth"


@router.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        bruker = Bruker.get_user(form.username.data)
        if bruker is None or not bruker.check_password(form.password.data):
            flash('Feil brukernavn og/eller passord', 'error')
            return render_template('login.html', form=form)

        login_user(bruker)

        flash('Logged in successfully.')

        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)

        return redirect(next or url_for("hovedside.index"))
    return render_template('login.html', form=form)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc
