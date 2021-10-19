from datetime import datetime
from random import randint
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import main
from app.models import User, Character
from .forms import ProfileForm, CharacterCreationForm, CharacterEditForm
from werkzeug.utils import secure_filename
from os import path
from .. import db
from .. import config
from .birthsigns import birthsigns
from .occupations import occupations
from .utils import threedsix, ability_modifiers
from .fumbles import fumbles


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
        occupation_roll = randint(1, 100)
        character.occupation = occupations[occupation_roll][0]
        character.proficient_weapons = occupations[occupation_roll][1]
        character.inventory = (
            f"{occupations[occupation_roll][1]}, {occupations[occupation_roll][2]}"
        )

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
        character.birthsign, character.birthsign_effect = birthsigns[randint(1, 30)]
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


@main.route("/mes_personnages/<int:id>")
@login_required
def character_detail(id):
    character = Character.query.get_or_404(id)
    return render_template(
        "character_detail.html", character=character, mod=ability_modifiers
    )


@main.route("/modifier_personnage/<int:id>", methods=["GET", "POST"])
@login_required
def edit_character(id):
    character = Character.query.get_or_404(id)
    if current_user.id != character.user_id:
        abort(403)
    form = CharacterEditForm()
    if form.validate_on_submit():
        character.name = form.name.data
        character.nickname = form.nickname.data

        character.xp = form.xp.data
        character.title = form.title.data
        character.occupation = form.occupation.data
        character.strength = form.strength.data
        character.agility = form.agility.data
        character.stamina = form.stamina.data
        character.personality = form.personality.data
        character.intelligence = form.intelligence.data
        character.luck = form.luck.data
        character.alignment = form.alignment.data

        character.languages = form.languages.data
        character.patron = form.patron.data
        flash(f"{character.name} a été modifié…")
        db.session.commit()
        return redirect(url_for("main.my_characters"))
    # Create and fill in the form
    form.name.data = character.name
    form.nickname.data = character.nickname
    form.level.data = character.level
    form.class_.data = character.class_
    form.xp.data = character.xp
    form.title.data = character.title
    form.occupation.data = character.occupation
    form.ac.data = character.ac
    form.hp.data = character.hp
    form.speed.data = character.speed
    form.init.data = character.init
    form.strength.data = character.strength
    form.agility.data = character.agility
    form.stamina.data = character.stamina
    form.personality.data = character.personality
    form.intelligence.data = character.intelligence
    form.luck.data = character.luck
    form.reflex.data = character.reflex
    form.fortitude.data = character.fortitude
    form.will.data = character.will
    form.alignment.data = character.alignment
    form.birthsign.data = character.birthsign
    form.birthsign_effect.data = character.birthsign_effect
    form.languages.data = character.languages
    form.patron.data = character.patron
    form.spells_known.data = character.spells_known
    form.inventory.data = character.inventory
    form.proficient_weapons.data = character.proficient_weapons

    return render_template("edit_character.html", character=character, form=form)


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


@main.route("/maladresses")
def fumbles_list():
    return render_template("fumbles.html", fumbles=fumbles.items())


@main.route("/maladresses/<int:die>")
def fumble_roll(die):
    roll = randint(1, die)
    if roll < 0:
        roll = 0
    if roll > 16:
        roll = 16

    flash(
        f"Tu as lancé un {roll}. Pense à ajuster en soustrayant to modificateur de chance."
    )
    return redirect(url_for("main.fumbles_list"))
