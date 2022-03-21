from cProfile import label
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo,Email, DataRequired, ValidationError
from market.models import User


class Register(FlaskForm):
    def validate_username(self, check_username):
        user= User.query.filter_by(username=check_username.data).first()
        if user:
            raise ValidationError("User already exists!")
    
    def validate_emailaddress(self, email_check):
        emailaddress= User.query.filter_by(emailadd=email_check.data).first()
        if emailaddress:
            raise ValidationError("This email is already in use")


    username = StringField(label='User Name', validators= [Length(min=2,max=50), DataRequired()])
    emailaddress = StringField(label= 'E-mail',validators=[Email(),DataRequired()])
    password1 = PasswordField(label='Password',validators = [Length(min =5),DataRequired()])
    password2 = PasswordField(label= 'Renter Password',validators= [EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Create Account')


class Login(FlaskForm):
    username = StringField(label='User Name', validators=[DataRequired()])
    password = PasswordField(label='Password',validators= [DataRequired()])
    submit = SubmitField(label='Sign in')


class Buy(FlaskForm):
    submit = SubmitField(label='Yes')

class Sell(FlaskForm):
    submit = SubmitField(label='Yes')