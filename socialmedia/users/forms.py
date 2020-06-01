from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import (DataRequired,
                                ValidationError,
                                EqualTo,
                                Length)
from wtforms import (StringField,
                     SubmitField,
                     PasswordField,
                     BooleanField,
                     SelectField,
                     TextAreaField)

from socialmedia.models import User


choices = (
    ('male', 'Male'),
    ('female', 'Female')
)


class UserCreationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('User already exists. Please select another')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('User already exists. Please select another')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class AccountInfo(FlaskForm):
    first_name = StringField('First name')
    last_name = StringField('Last Name')
    gender = SelectField('Gender', choices=choices)
    bio = TextAreaField('Bio')
    submit = SubmitField('Submit')
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired()
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    profile_image = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'png'])
    ])


class RequestChangePassword(FlaskForm):
    email = StringField('Email Address', validators=[
        DataRequired()
    ])
    submit = SubmitField('Send reset link')

    def validate_email(self, email):
        user = User.query.filter_by(email=email).first()
        if user is None:
            return ValidationError('Email does not exist')
        return user


class ChangePasswordFormFromToken(FlaskForm):
    new_password = PasswordField('New Password', validators=[
        DataRequired()
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('new_password')
    ])
    submit = SubmitField('Reset Password')
