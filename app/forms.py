from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, InputRequired
from app.models import User
from flask_wtf.file import FileAllowed, FileField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', 
        validators=[
            DataRequired(), 
            EqualTo('password')
            ]
        )
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use another username')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use another email adress')

class CommentForm(FlaskForm):
    comment = TextAreaField('write something...', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Comment')

class UploadForm(FlaskForm):
    photo = FileField("Photo",validators=[InputRequired()])
    submit = SubmitField('Upload photo')