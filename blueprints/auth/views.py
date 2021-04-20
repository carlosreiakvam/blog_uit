from flask import Blueprint, render_template
from models.bruker import Bruker

router = Blueprint('auth', __name__, url_prefix="/auth")


@router.route("/")
def example():
    return "hello from auth"

@router.route('/loginpage')
# @login_required
def login_page() -> 'html':
    return render_template('login.html')


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