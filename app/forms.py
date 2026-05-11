from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User
from wtforms import TextAreaField
from wtforms.validators import Length
from flask_babel import lazy_gettext as _l

class LoginForm(FlaskForm):
    username = StringField(str(_l('Username')), validators=[DataRequired()])
    password = PasswordField(str(_l('Password')), validators=[DataRequired()])
    remember_me = BooleanField(str(_l('Remember Me')))
    submit = SubmitField(str(_l('Sign In')))

class RegistrationForm(FlaskForm):
    username = StringField(str(_l('Username')), validators=[DataRequired()])
    email = StringField(str(_l('Email')), validators=[DataRequired(), Email()])
    password = PasswordField(str(_l('Password')), validators=[DataRequired()])
    password2 = PasswordField(
        str(_l('Repeat Password')), validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(str(_l('Register')))

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data
        ))
        if user is not None:
            raise ValidationError(str(_l('Please use a different username.')))
        
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data
        ))
        if user is not None:
            raise ValidationError(str(_l('Please use a different email address.')))
        
class EditProfileForm(FlaskForm):
    username = StringField(str(_l('Username')), validators=[DataRequired()])
    about_me = TextAreaField(str(_l('About me')), validators=[Length(min=0, max=140)])
    submit = SubmitField(str(_l('Submit')))

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data
            ))

            if user is not None:
                raise ValidationError(str(_l('Please use a different username.')))

class EmtpyForm(FlaskForm):
    submit = SubmitField(str(_l('Submit')))


class PostForm(FlaskForm):
    post = TextAreaField(str(_l('Say something')), validators=[
        DataRequired(), Length(min=1, max=140)
    ])
    submit = SubmitField(str(_l('Submit')))

class ResetPasswordRequestForm(FlaskForm):
    email = StringField(str(_l('Email')), validators=[DataRequired(), Email()])
    submit = SubmitField(str(_l('Request Password Reset')))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(str(_l('Password')), validators=[DataRequired()])
    password2 = PasswordField(
        str(_l('Repeat Password')), validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField(str(_l('Request Password Reset')))