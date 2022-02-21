from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired

class UploadForm(FlaskForm):
    title = StringField('title', render_kw={"placeholder": "title"})
    keywords = StringField('keywords', render_kw={"placeholder": "keywords"})
    photo = FileField(validators=[FileRequired()])
    submit = SubmitField('post')


class SearchForm(FlaskForm):
    search = StringField('search')
