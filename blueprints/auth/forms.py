from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    brukernavn = StringField(
        label=('Brukernavn'),
        validators=[DataRequired(),
                    Length(min=5,
                           max=24,
                           message='Brukernavnet må være mellom 5 og 24 tegn')])

    etternavn = StringField(
        label=('Etternavn'),
        validators=[DataRequired()])

    fornavn = StringField(
        label=('Fornavn'),
        validators=[DataRequired()])

    epost = StringField(
        label=('Epost'),
        validators=[
            DataRequired(),
            Email(message="Vennligst oppgi en gyldig epostadresse")])

    passord = PasswordField(
        label=('Passord'),
        validators=[DataRequired(),
                    Length(min=8,
                           message='Passordet må være minst 8 tegn langt')])

    confirm = PasswordField(
        label=('Gjenta passord'),
        validators=[DataRequired(message='*Required'),
                    EqualTo('passord',
                            message='Passordene må være like')])
    submit = SubmitField(label=('Registrer'))
