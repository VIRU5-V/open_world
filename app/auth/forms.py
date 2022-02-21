from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from ..models import User



class LoginForm(FlaskForm):
    username = StringField("name", validators=[DataRequired()], render_kw={"placeholder": "username"})
    password = PasswordField( "password", validators=[DataRequired()], render_kw={"placeholder": "password"})
    remember_me = BooleanField("remember_me")
    submit = SubmitField('login')


class SignupForm(FlaskForm):
    username = StringField("name", render_kw={"placeholder": "username"})
    password = PasswordField( "password", render_kw={"placeholder": "password"})
    submit = SubmitField('signup')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('User already exist!')


