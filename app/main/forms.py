from typing import BinaryIO, Text
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import (
    StringField,
    RadioField,
    TextAreaField,
    BooleanField,
    SubmitField,
    PasswordField,
    ValidationError,
    FileField,
)
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, Optional
from app.models import User






class ProfileForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 128), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField(
        "Update password",
        validators=[
            EqualTo("password2", message="Passwords must match."),
        ],
    )
    password2 = PasswordField("Confirm new password")
    submit = SubmitField("Update profile")
