from wtforms import Form, StringField, SubmitField, validators, PasswordField, SelectField
import phonenumbers
from api.models import UserType

class UserRegister(Form):
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

    # types = UserType.query.all()
    
    type = SelectField(
        'Select your profession',
        choices = [
            
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
    submit = SubmitField('Submit')

    def validate_phone(self, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise validators.ValidationError('Invalid phone number')
    
    def generate_auth_token(self):
        pass # todo???