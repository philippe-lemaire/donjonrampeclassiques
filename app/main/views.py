from datetime import datetime
from random import randint
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import main
from app.models import User, Character
from .forms import ProfileForm, CharacterCreationForm
from werkzeug.utils import secure_filename
from os import path
from .. import db
from .. import config


def threedsix():
    """returns 3d6 for stat generation"""
    return randint(1, 6) + randint(1, 6) + randint(1, 6)


ability_modifiers = {
    k: v
    for k, v in zip(
        range(3, 19), [-3, -2, -2, -1, -1, -1, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3]
    )
}


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/mon_profil", methods=["GET", "POST"])
@login_required
def my_profile():
    profileform = ProfileForm()

    if profileform.validate_on_submit():
        # update the user and commit to db
        current_user.username = profileform.username.data
        current_user.email = profileform.email.data
        current_user.password = profileform.password.data
        # save the picture and update the user.picture database field
        filename = secure_filename(profileform.picture.data.filename)
        file_ext = path.splitext(filename)[1]
        img_path = f"app/static/img/uploads/{current_user.id}{file_ext}"
        profileform.picture.data.save(img_path)
        current_user.picture = f"{current_user.id}{file_ext}"
        flash("Profile updated")
        db.session.commit()
        return redirect(url_for("main.index"))

    # fill in the form before rendering
    profileform.username.data = current_user.username
    profileform.email.data = current_user.email
    return render_template("my_profile.html", profileform=profileform)


@main.route("/utilisateur/<int:id>")
def user_page(id):
    user = User.query.get_or_404(id)
    return render_template("user_page.html", user=user)


@main.route("/créer_personnage", methods=["GET", "POST"])
@login_required
def create_character():
    characterform = CharacterCreationForm()
    character = Character()
    if characterform.validate_on_submit():
        # create the character and commit to db
        character.name = characterform.name.data
        character.user_id = current_user.id
        character.nickname = ""  # TODO add randomtables for nicknames
        character.level = 0
        character.class_ = "Paysan"
        character.xp = 0
        character.title = ""  # TODO add randomtables for titles
        character.occupation = ""  # TODO add randomtables for occupation

        character.strength = threedsix()
        character.agility = threedsix()
        character.stamina = threedsix()
        character.personality = threedsix()
        character.intelligence = threedsix()
        character.luck = threedsix()
        # derived stats
        character.hp = randint(1, 4) + ability_modifiers[character.stamina]
        if character.hp < 1:
            character.hp = 1

        character.reflex = ability_modifiers[character.agility]
        character.fortitude = ability_modifiers[character.stamina]
        character.will = ability_modifiers[character.personality]
        character.ac = 10 + ability_modifiers[character.agility]

        character.speed = 9
        if "Nain" or "Halfelin" in character.occupation:
            character.speed = 6

        character.init = ability_modifiers[character.agility]
        character.alignment = characterform.alignment.data
        character.birthsign = "TODO"  # TODO add randomtables for birthsign
        character.languages = str(
            [
                "Commun",
            ]
        )
        character.last_updated = datetime.utcnow()
        character.patron = ""
        character.spells_known = str([])
        db.session.add(character)
        db.session.commit()
        flash(f"{character.name} a été créé.")
        return redirect(url_for("main.my_characters"))
    return render_template("create_character.html", characterform=characterform)


@main.route("/mes_personnages")
@login_required
def my_characters():
    characters = Character.query.filter_by(user_id=current_user.id).all()
    return render_template("my_characters.html", characters=characters)


@main.route("/modifier_personnage/<int:id>")
@login_required
def edit_character(id):
    character = Character.query.get_or_404(id)
    # Create and fill in the form
    return render_template("edit_character.html", character=character)


@main.route("/supprimer/personnage/<int:id>")
@login_required
def delete_character(id):
    char = Character.query.get_or_404(id)
    if current_user.id != char.user_id:
        abort(403)
    db.session.delete(char)
    db.session.commit()
    flash(f"{char.name} a été supprimé. Paix à son âme…")
    return redirect(url_for("main.my_characters"))
