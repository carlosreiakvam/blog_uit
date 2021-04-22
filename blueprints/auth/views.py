from flask import Blueprint, render_template, abort, flash, url_for, redirect, request
from flask_login import login_user

from models.bruker import Bruker
from blueprints.auth.forms import LoginForm

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
            print('test')
            return render_template('login.html', form=form)

        login_user(bruker)

        flash('Logged in successfully.')

        next = request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        #if not is_safe_url(next):
        #    return flask.abort(400)

        return redirect(next or url_for('hello_world'))
    print('test2')
    return render_template('login.html', form=form)


'''
@router.route('/login', methods=["GET", "POST"])
def login() -> 'html':
    if request.method == "POST":

        username = request.form['username']
        password = request.form['password']
        with Bruker() as db:
            user = User(*db.get_bruker(username))
            if user.check_password(password):
                user.is_authenticated = True
                login_user(user)
                session['user'] = user.__dict__

        return redirect('/')
'''