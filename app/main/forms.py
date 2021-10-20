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


class CharacterCreationForm(FlaskForm):
    name = StringField(
        "Nom du personnage, laisser vide pour un nom aléatoire, qui sera attribué au niveau 1."
    )
    alignment = RadioField(
        label="Choisissez votre alignement", choices=["Chaotique", "Neutre", "Loyal"]
    )
    submit = SubmitField("Montjoie !")


class CharacterEditForm(FlaskForm):
    name = StringField(label="Nom")

    nickname = StringField(label="Sobriquet")
    level = IntegerField(label="Niveau")
    class_ = StringField(label="Classe", render_kw={"readonly": True})
    xp = IntegerField(label="XP")
    title = StringField(label="Titre")
    occupation = StringField(label="Occupation", render_kw={"readonly": True})
    ac = IntegerField(label="CA", render_kw={"readonly": True})
    hp = IntegerField(label="PV")
    speed = IntegerField(label="Vitesse", render_kw={"readonly": True})
    init = IntegerField(label="Init", render_kw={"readonly": True})
    strength = IntegerField(label="Force")
    agility = IntegerField(label="Agilité")
    stamina = IntegerField(label="Endurance")
    personality = IntegerField(label="Présence")
    intelligence = IntegerField(label="Intelligence")
    luck = IntegerField(label="Chance")
    reflex = IntegerField(label="Réf.")
    fortitude = IntegerField(label="Vig.")
    will = IntegerField(label="Vol.")
    alignment = StringField(label="Alignement", render_kw={"readonly": True})
    birthsign = StringField(label="Naissance", render_kw={"readonly": True})
    birthsign_effect = StringField(label="Jet chanceux", render_kw={"readonly": True})
    languages = StringField(label="Langues")
    patron = StringField(label="Patron")
    spells_known = StringField(label="Sorts Connus")
    inventory = StringField(label="Inventaire")
    proficient_weapons = StringField(label="Armes maîtrisées")

    submit = SubmitField("Montjoie !")


class ClassSelectionForm(FlaskForm):
    class_ = RadioField(
        label="Selectionner une classe",
        choices=["Guerrier", "Voleur", "Clerc", "Mage"],
        validators=[DataRequired()],
    )
    submit = SubmitField("Montjoie !")


class LuckyWeaponSelectionForm(FlaskForm):
    lucky_weapon = StringField(
        label="Choisissez un type d’armes avec lesquelles vous appliquerez votre modificateur de chance",
        validators=[DataRequired()],
    )
    submit = SubmitField("Montjoie !")
