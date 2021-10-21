from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 128), Email()])
    password = PasswordField("Mot de passe", validators=[DataRequired()])
    remember_me = BooleanField("Me laisser identifié·e")
    submit = SubmitField("M’identifier")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Length(1, 128), Email()])
    username = StringField(
        "Nom d’utilisateur·trice",
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(
                "^[A-Za-z][A-Za-z0-9_.]*$",
                0,
                "Usernames must only have letters, numbers, dots or underscores",
            ),
        ],
    )
    password = PasswordField(
        "Mot de passe",
        validators=[
            DataRequired(),
            EqualTo("password2", message="Passwords must match."),
        ],
    )
    password2 = PasswordField(
        "Répéter le mot de passe, juste pour être sûr·e", validators=[DataRequired()]
    )
    submit = SubmitField("Je crée mon compte")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Il y a déjà un compte avec cet email.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Il y a déjà un compte avec ce petit nom.")
