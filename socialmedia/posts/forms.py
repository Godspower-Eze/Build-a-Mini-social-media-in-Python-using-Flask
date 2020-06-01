from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import SubmitField, StringField, TextAreaField
from flask_wtf.file import FileField, FileAllowed


class PostCreationForm(FlaskForm):
    post_title = StringField('Title', validators=[
        DataRequired(),
    ])
    post_content = TextAreaField('Content', validators=[
        DataRequired()
    ])
    post_image = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])
    ])

    submit = SubmitField('Post')

