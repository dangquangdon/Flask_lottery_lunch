from flask_wtf import FlaskForm
from wtforms import (BooleanField,
                     PasswordField,
                     StringField,
                     SubmitField)
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                ValidationError)
from main.subscribers.models import Subscriber
from main import bcrypt

class AdminLoginForm(FlaskForm):
    email = StringField("Email",
                        validators=[ DataRequired(),
                                    Email()
                                    ])
    password = PasswordField("Password",
                             validators=[ DataRequired()])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

    def validate_email(self, email):
        subscriber = Subscriber.query.filter_by(email = email.data).first()
        if not subscriber:
            raise ValidationError('This email address is not valid')

    def validate_password(self, password):
        subscriber = Subscriber.query.filter_by(email = self.email.data).first()
        if subscriber:
            check_password = bcrypt.check_password_hash(subscriber.password,
                                                        password.data)
            if not check_password:
                raise ValidationError('Wrong password')

class CreateAdminForm(FlaskForm):
    first_name = StringField("First name",
                             validators = [ DataRequired(),
                                            Length(min=2, max=20,
                                                message="2 to 20 characters")
                             ])
    last_name = StringField("Last name",
                             validators = [ DataRequired(),
                                            Length(min=2, max=20,
                                                message="2 to 20 characters")
                             ])
    email = StringField("Email",
                        validators=[ DataRequired(),
                                    Email()
                                    ])
    password = PasswordField("Password",
                             validators=[ DataRequired()])
    confirm_password = PasswordField("Confirm Password",
                             validators=[ DataRequired(),
                                        EqualTo('password')
                             ])
    submit = SubmitField("Register User")

    def validate_email(self, email):
        subscriber = Subscriber.query.filter_by(email = email.data).first()
        if subscriber:
            raise ValidationError('This email address has already been registered')

