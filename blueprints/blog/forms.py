from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class InnleggForm(FlaskForm):
    tittel = StringField("Tittel", validators=[Length(min=2, max=50)])
    innhold = CKEditorField("Innhold", validators=[DataRequired()])
