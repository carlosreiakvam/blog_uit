from flask import Blueprint, render_template
from models.bruker import Bruker
from forms import LoginForm

router = Blueprint('auth', __name__, url_prefix="/auth")


@router.route("/")
def example():
    return "hello from auth"


@router.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        with Bruker() as db:
            user = Bruker(*db.get_bruker(username)) #kopiert disse linjene fra under her.
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


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