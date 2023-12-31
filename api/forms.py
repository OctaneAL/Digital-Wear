from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, validators, PasswordField, SelectField, URLField, TextAreaField, FileField
from flask_wtf.file import FileAllowed, FileRequired
import phonenumbers
from api.models import UserType, Client, ProductType
from api import app
from flask import flash
from flask_login import current_user


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
            validators.Length(min = 3,max = 30, message = 'First name must be at least 3 characters long and no more than 30.'),
        ],
    )
    last_name = StringField(
        'Last Name',
        validators=[
            validators.DataRequired(),
            validators.Length(min = 3,max = 30, message = 'Last name must be at least 3 characters long and no more than 30.'),
        ],
    )
    phone = StringField(
        'Phone Number',
        validators=[
            validators.DataRequired(),
            validators.Length(min=6, max=10, message="Phone number must be at least 4 characters and no more than 10")
        ],
    )

    with app.app_context():
        types = [(user.id, user.name) for user in UserType.query.all()]
        
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
            validators.Length(min=4, max=80, message="Password must be at least 4 and no more than 80 characters"),
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
        exists = Client.query.filter_by(email=email.data).first() is not None
        if exists:
            flash("This email has been already registered", category="error")
            raise validators.ValidationError('Email is already taken')
        
    def validate_phone(self, phone):
        exists = Client.query.filter_by(phone=phone.data).first() is not None
        if exists:
            flash("This phone number has been registered", category="error")
            raise validators.ValidationError('Phone is already taken')
    # def validate_phone(self, phone):
    #     try:
    #         p = phonenumbers.parse(phone.data)
    #         if not phonenumbers.is_valid_number(p): 
    #             raise validators.ValidationError('Invalid phone number')
    #     except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
    #         raise validators.ValidationError('Invalid phone number')
    
    def generate_auth_token():
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

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
class CreatePost(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            validators.DataRequired(),
            validators.Length(min=1, max=50, message = 'Title must be at least 1 character long and no more than 30.'),
        ],
    )

    with app.app_context():
        types = [(type.id, type.name) for type in ProductType.query.all()]
        
    type = SelectField(
        'Select your profession',
        choices = types,
        validators=[
            validators.DataRequired(),
        ],
    )

    description = TextAreaField(
        'Description', 
        validators=[
            validators.DataRequired(),
            validators.Length(max=300, message="No more than 300 characters")
        ],
    )

    website = URLField(
        'Website'
    )

    photo = FileField(
        "Main Photo",
        validators=[
            FileRequired(),
            FileAllowed(['png', 'jpeg', 'jpg']),
        ],
    )

    submit = SubmitField('Create')

    def is_authenticated(self):
        return current_user.is_authenticated

class UpdatePost(FlaskForm):
    title = StringField(
        'Title',
        validators=[
            validators.DataRequired(),
            validators.Length(min=1, max=50, message = 'Title must be at least 1 character long and no more than 30.'),
        ],
    )

    with app.app_context():
        types = [(type.id, type.name) for type in ProductType.query.all()]
        
    type = SelectField(
        'Select your profession',
        choices = types,
        validators=[
            validators.DataRequired(),
        ],
    )

    description = TextAreaField(
        'Description', 
        validators=[
            validators.DataRequired(),
            validators.Length(max=300, message="No more than 300 characters")
        ],
    )

    website = URLField(
        'Website'
    )

    submit = SubmitField('Create')

    def is_authenticated(self):
        return current_user.is_authenticated


class UpdateUser(FlaskForm):
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
            validators.Length(min = 3,max = 30, message = 'First name must be at least 3 characters long and no more than 30.'),
        ],
    )
    
    last_name = StringField(
        'Last Name',
        validators=[
            validators.DataRequired(),
            validators.Length(min = 3,max = 30, message = 'Last name must be at least 3 characters long and no more than 30.'),
        ],
    )
    phone = StringField(
        'Phone Number',
        validators=[
            validators.DataRequired(),
            validators.Length(min=6, max=10, message="Phone number must be at least 4 characters and no more than 10")
        ],
    )

    description = TextAreaField(
        'Description', 
        validators=[
            validators.DataRequired(),
            validators.Length(max=300, message="No more than 300 characters")
        ],
    )

    with app.app_context():
        types = [(user.id, user.name) for user in UserType.query.all()]
        
    type = SelectField(
        'Select your profession',
        choices = types,
        validators=[
            validators.DataRequired(),
        ],
    )

    photo = FileField(
        " Photo",
        validators=[
            FileAllowed(['png', 'jpeg']),
        ],
    )


    website = StringField(
        'Website',
    )

    submit = SubmitField('Update')

    def validate_email(self, email):
        exists = Client.query.filter_by(email=email.data).first() is not None
        if exists:
            user =  Client.query.filter_by(email=email.data).first()
            if user.id != current_user.id:
                flash("This email has been already registered", category="error")
                raise validators.ValidationError('Email is already taken')
        
    def validate_phone(self, phone):
        exists = Client.query.filter_by(phone=phone.data).first() is not None
        if exists:
            user = Client.query.filter_by(phone=phone.data).first()
            if user.id != current_user.id:
                flash("This email has been already registered", category="error")
                raise validators.ValidationError('Email is already taken')
            
    def is_authenticated(self):
        return current_user.is_authenticated