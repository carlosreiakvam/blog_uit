import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    fornavn = StringField('Fornavn')
    etternavn = StringField('Etternavn')
    # epost = wtforms.fields.html5.EmailField('Epost')
    epost = StringField('Epost')
    brukernavn = StringField('Brukernavn')
    passord = PasswordField('Passord')
    submit = SubmitField('Submit')
