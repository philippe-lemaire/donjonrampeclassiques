from datetime import datetime
from random import randint, choice, sample
from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from flask_sqlalchemy.model import NameMetaMixin
from sqlalchemy import desc
from . import main
from app.models import User, Character
from .forms import (
    AlignmentForm,
    ProfileForm,
    CharacterCreationForm,
    CharacterEditForm,
    ClassSelectionForm,
    LuckyWeaponSelectionForm,
)
from werkzeug.utils import secure_filename
from os import path
from .. import db
from .birthsigns import birthsigns
from .occupations import occupations
from .utils import threedsix, ability_modifiers, hit_die
from .fumbles import fumbles
from .class_bonuses import (
    level_bonuses,
    mighty_deeds,
    halflin_skills,
    thieves_bonuses,
    thieves_skills,
    luck_die,
)
from .random_names import random_names
from .titles import titles
from .equipment import equipment
from .spells import wizard_spells, cleric_spells


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
        flash("Profile updated")
        db.session.commit()
        return redirect(url_for("main.index"))

    # fill in the form before rendering
    profileform.username.data = current_user.username
    profileform.email.data = current_user.email
    return render_template("my_profile.html", profileform=profileform)


@main.route("/créer_personnage", methods=["GET", "POST"])
@login_required
def create_character():
    characterform = CharacterCreationForm()
    character = Character()
    if characterform.validate_on_submit():
        # create the character and commit to db
        character.name = characterform.name.data or "Anonyme"
        character.user_id = current_user.id
        character.nickname = ""  # TODO add randomtables for nicknames
        character.level = 0
        character.class_ = "Paysan"
        character.xp = 0
        character.title = ""  # TODO add randomtables for titles
        occupation_roll = randint(1, 100)
        character.occupation = occupations[occupation_roll][0]
        character.proficient_weapons = occupations[occupation_roll][1]
        character.inventory = f"{occupations[occupation_roll][1]}, {occupations[occupation_roll][2]}, {equipment.get(randint(1,24))[0]}"

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

        character.current_hp = character.hp
        character.reflex = ability_modifiers[character.agility]
        character.fortitude = ability_modifiers[character.stamina]
        character.will = ability_modifiers[character.personality]
        character.ac = 10 + ability_modifiers[character.agility]

        character.speed = 9
        if "Nain" in character.occupation or "Halfelin" in character.occupation:
            character.speed = 6

        character.init = ability_modifiers[character.agility]
        character.birthsign, character.birthsign_effect = birthsigns[randint(1, 30)]
        character.languages = "Commun"

        character.last_updated = datetime.utcnow()
        character.patron = ""
        character.spells_known = str([])
        character.dead = False
        db.session.add(character)
        db.session.commit()
        flash(f"{character.name} a été créé.")
        return redirect(url_for("main.my_characters"))
    return render_template("create_character.html", characterform=characterform)


@main.route("/mes_personnages")
@login_required
def my_characters():
    characters = (
        Character.query.filter_by(user_id=current_user.id).filter_by(dead=False).all()
    )
    return render_template("my_characters.html", characters=characters)


@main.route("/mes_personnages/décédés")
@login_required
def my_dead_characters():
    characters = (
        Character.query.filter_by(user_id=current_user.id).filter_by(dead=True).all()
    )
    return render_template("my_characters.html", characters=characters)


@main.route("/mes_personnages/choisir_alignement/<int:id>", methods=["GET", "POST"])
@login_required
def choose_alignment(id):
    char = Character.query.get_or_404(id)
    if current_user.id != char.user_id:
        abort(403)
    form = AlignmentForm()
    if form.validate_on_submit():
        char.alignment = form.alignment.data
        db.session.commit()
        return redirect(url_for("main.level_up_character", id=char.id))
    return render_template("choose_alignment.html", form=form, char=char)


@main.route("/mes_personnages/<int:id>")
@login_required
def character_detail(id):
    character = Character.query.get_or_404(id)

    return render_template(
        "character_detail.html",
        character=character,
        mod=ability_modifiers,
        level_bonuses=level_bonuses,
        mighty_deeds=mighty_deeds,
        titles=titles,
        halflin_skills=halflin_skills,
        thieves_bonuses=thieves_bonuses,
        thieves_skills=thieves_skills,
        luck_die=luck_die,
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
        character.current_hp = form.hp.data
        character.languages = form.languages.data
        character.patron = form.patron.data
        character.inventory = form.inventory.data
        flash(f"{character.name} a été modifié…")
        db.session.commit()
        return redirect(url_for("main.character_detail", id=character.id))
    # Create and fill in the form
    form.name.data = character.name
    form.nickname.data = character.nickname
    form.level.data = character.level
    form.class_.data = character.class_
    form.xp.data = character.xp
    form.title.data = character.title
    form.occupation.data = character.occupation
    form.ac.data = character.ac
    form.hp.data = character.current_hp
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
    if char.dead:
        db.session.delete(char)
        db.session.commit()
        flash(f"{char.name} a été supprimé·e. Paix à son âme…")
    else:
        char.dead = True
        db.session.commit()
        flash(
            f"{char.name} est tombé·e en combat. Mais avec un peu de chance il ou elle peut ressusciter."
        )
    return redirect(url_for("main.my_characters"))


@main.route("/ressusciter/personnage/<int:id>")
@login_required
def resurect_character(id):
    char = Character.query.get_or_404(id)
    if current_user.id != char.user_id:
        abort(403)
    if char.dead:
        char.dead = False
        db.session.commit()
        flash(f"{char.name} a été ressuscité·e.")
    else:
        flash(f"{char.name} n’était même pas mort·e.")
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


@main.route("/monter_de_niveau/<int:id>", methods=["GET", "POST"])
@login_required
def level_up_character(id):
    char = Character.query.get_or_404(id)
    # check user owns the character
    if current_user.id != char.user_id:
        abort(403)
    # check if alignment is not set yet
    if not char.alignment:
        return redirect(url_for("main.choose_alignment", id=char.id))
    # check the character hasn't reached max level 10
    if char.level >= 10:
        flash("Ce personnage a atteint son niveau maximum, espèce de munchkin.")
        return redirect(url_for("main.character_detail", id=char.id))
    # check if its the first level up and char is human
    demihumans = ["Nain", "Elfe", "Halfelin"]

    if char.level == 0 and char.occupation.split(" ")[0] not in demihumans:
        form = ClassSelectionForm()
        if form.validate_on_submit():
            # we need to fork to the warrior / dwarf funnel
            # before leveling up, in case it is interrupted
            # first assign class
            char.class_ = form.class_.data
            db.session.commit()

            if char.class_ == "Guerrier":
                # revert to default class_ in case the weapon choice is interrupted
                char.class_ = "Paysan"
                db.session.commit()
                return redirect(url_for("main.select_lucky_weapon", id=char.id))
            if char.class_ == "Voleur":
                char.languages = f"{char.languages}, Argot des Voleurs"

            char.level += 1

            if char.class_ == "Mage":
                k = 4 + ability_modifiers[char.intelligence]
                if k < 1:
                    k = 1
                char.spells_known = ", ".join(
                    sample(population=wizard_spells.get(1)[:-1], k=k)
                )

            if char.class_ == "Clerc":
                k = 4
                char.spells_known = ", ".join(
                    sample(population=cleric_spells.get(1), k=k)
                )

            extra_hp = ability_modifiers[char.stamina] + randint(
                1, hit_die[char.class_]
            )
            if extra_hp < 1:
                extra_hp = 1
            char.hp += extra_hp
            char.current_hp += extra_hp
            if char.name == "Anonyme":
                char.name = choice(random_names.get(char.class_))
            char.title = titles.get(char.class_).get(char.alignment).get(1)
            db.session.commit()
            flash(
                f"{char.name} est monté d’un niveau et a gagné {extra_hp} points de vie."
            )

            return redirect(url_for("main.character_detail", id=char.id))
        return render_template(
            "class_selection.html", form=form, character=char, mod=ability_modifiers
        )
    # assign race as class for demihumans
    if char.level == 0 and char.occupation.split(" ")[0] in demihumans:
        char.class_ = char.occupation.split(" ")[0]
        db.session.commit()
    # special case for Dwarves
    if char.class_ == "Nain" and char.level == 0:
        # revert to default class_ in case the weapon choice is interrupted
        char.class_ = "Paysan"
        db.session.commit()
        return redirect(url_for("main.select_lucky_weapon", id=char.id))
    # general case level up
    if char.name == "Anonyme":
        char.name = choice(random_names.get(char.class_))
    char.level += 1
    if char.level == 1 and char.class_ == "Elfe":
        k = 3
        char.spells_known = ", ".join(
            sample(population=wizard_spells.get(1)[:-3], k=k)
            + wizard_spells.get(1)[-3:-1]
        )
    title_level = char.level
    if title_level > 5:
        title_level = 5
    char.title = titles.get(char.class_).get(char.alignment).get(title_level)
    extra_hp = ability_modifiers[char.stamina] + randint(1, hit_die[char.class_])
    if extra_hp < 1:
        extra_hp = 1
    char.current_hp += extra_hp
    char.hp += extra_hp
    db.session.commit()
    flash(f"{char.name} est monté d’un niveau et a gagné {extra_hp} points de vie.")

    return redirect(url_for("main.character_detail", id=char.id))


@main.route(
    "/monter_de_niveau/selectionner_arme_chanceuse/<int:id>", methods=["GET", "POST"]
)
@login_required
def select_lucky_weapon(id):
    char = Character.query.get_or_404(id)
    lucky_weapon_form = LuckyWeaponSelectionForm()
    if lucky_weapon_form.validate_on_submit():
        # the switch to level 1 happens here, to avoid leveling up
        # and interrupting the process during lucky weapon choice
        # only for warriors and dwarves
        char.level = 1
        # assign class_ here to be safer
        if char.occupation.split(" ")[0] == "Nain":
            char.class_ = "Nain"
        else:
            char.class_ = "Guerrier"
        extra_hp = ability_modifiers[char.stamina] + randint(1, hit_die[char.class_])
        if extra_hp < 1:
            extra_hp = 1
        char.hp += extra_hp
        char.current_hp += extra_hp
        if char.name == "Anonyme":
            char.name = choice(random_names.get(char.class_))
        char.title = titles.get(char.class_).get(char.alignment).get(1)
        char.lucky_weapon = lucky_weapon_form.lucky_weapon.data.capitalize()
        db.session.commit()
        flash(
            f"{char.name} est passé au niveau 1. {char.lucky_weapon} sera son arme chanceuse."
        )
        return redirect(url_for("main.character_detail", id=char.id))
    return render_template(
        "lucky_weapon_selection.html",
        char=char,
        lucky_weapon_form=lucky_weapon_form,
    )


@main.route("/équipement")
def view_equipment():
    return render_template("equipment.html", equipment=equipment)


@main.route("/équipement/hasard")
def equipment_roll():
    roll = randint(1, 24)
    flash(f"Tu as lancé un {roll}, et obtenu : {equipment.get(roll)[0]}.")
    return redirect(url_for("main.view_equipment"))


@main.route("/sorts")
def view_wizard_spells():
    return render_template("view_wizard_spells.html", spells=wizard_spells)


@main.route("/prières")
def view_cleric_spells():
    return render_template("view_cleric_spells.html", spells=cleric_spells)
