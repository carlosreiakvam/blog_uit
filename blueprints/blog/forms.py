from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import Field, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextArea, TextInput


class TagListField(Field):
    widget = TextInput()

    def __init__(self, label='', validators=None, remove_duplicates=True, **kwargs):
        super(TagListField, self).__init__(label, validators, **kwargs)
        self.remove_duplicates = remove_duplicates

    def process_formdata(self, valuelist):
        super(TagListField, self).process_formdata(valuelist)
        if self.remove_duplicates:
            self.data = list(self._remove_duplicates(self.data))

    def _value(self):
        if self.data:
            return u', '.join(self.data)
        else:
            return u''

    def process_formdata(self, value_list):
        if value_list:
            self.data = [x.strip() for x in value_list[1].split(',')]
        else:
            self.data = []

    @classmethod
    def _remove_duplicates(cls, seq):
        """Remove duplicates in a case insensitive, but case preserving manner"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


class BloggForm(FlaskForm):
    blog_navn = StringField("Bloggnavn", validators=[Length(min=2, max=45)])
    blog_prefix = StringField("Blogg-prefix", validators=[Length(min=2, max=45)])


class InnleggForm(FlaskForm):
    tittel = StringField("Tittel", validators=[Length(min=2, max=50)])
    innhold = CKEditorField("Innhold", validators=[DataRequired()])
    tagger = TagListField("Tagger", validators=[Length(max=8, message="You can only use up to 8 tags.")])


class KommentarForm(FlaskForm):
    innhold = StringField("Ny kommentar", widget=TextArea(), validators=[Length(max=255), DataRequired()])
    submit = SubmitField("Lagre")
