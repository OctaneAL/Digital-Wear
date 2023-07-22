from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, SelectField
import phonenumbers
from api.models import UserType, Client
from api import app

class UserRegister(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            validators.DataRequired(),
            validators.Email(),
        ],
    )
    first_name = StringField(
        'First Name',
        validators=[
            validators.DataRequired(),
            validators.Length(min = 3, message = 'First Name must be at least 3 characters long.'),
        ],
    )
    last_name = StringField(
        'Last Name',
        validators=[
            validators.DataRequired(),
            validators.Length(min = 2, message = 'Last Name must be at least 2 characters long.'),
        ],
    )
    phone = StringField(
        'Phone Number',
        validators=[
            validators.DataRequired(),
        ],
    )

    with app.app_context():
        types = [user.name for user in UserType.query.all()]
        types.append("Красавчик")
        types.append("Лошара")

        
    type = SelectField(
        'Select your profession',
        choices = types,
        validators=[
            validators.DataRequired(),
        ],
    )
    password = PasswordField(
        "Enter password",
        validators=[
            validators.DataRequired(),
            validators.Length(min=4, max=80),
            validators.EqualTo('password2', message = 'Passwords must match')
        ],
    )
    password2 = PasswordField(
        "Repeat password",
        validators=[
            validators.DataRequired(),
            validators.Length(min=4, max=80),
        ],
    )
    submit = SubmitField('Register')

    def validate_email(self, email):
        exists = Client.query.filter_by(email=email).first() is not None
        if exists:
            raise validators.ValidationError('Email is already taken')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p): 
                raise validators.ValidationError('Invalid phone number')
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise validators.ValidationError('Invalid phone number')
    
    def generate_auth_token(self):
        pass # todo???

class UserLogin(FlaskForm):
    email = StringField(
        'Email',
        validators=[
            validators.DataRequired(),
            validators.Email(),
        ],
    )
    password = PasswordField(
        "Enter password",
        validators=[
            validators.DataRequired(),
            validators.Length(min=4, max=80),
        ],
    )
    submit = SubmitField('Login')