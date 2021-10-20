from logging import NullHandler
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import login_manager
from flask_login import UserMixin


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self):
        return "<Role %r>" % self.name


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    username = db.Column(db.String(64), index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    characters = db.relationship("Character", backref="user")

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User %r>" % self.username


class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(64))
    nickname = db.Column(db.String(64), nullable=True)
    level = db.Column(db.Integer)
    class_ = db.Column(db.String(64))
    xp = db.Column(db.Integer)
    title = db.Column(db.String(64), nullable=True)
    occupation = db.Column(db.String(128))
    ac = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    init = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    agility = db.Column(db.Integer)
    stamina = db.Column(db.Integer)
    personality = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    luck = db.Column(db.Integer)
    reflex = db.Column(db.Integer)
    fortitude = db.Column(db.Integer)
    will = db.Column(db.Integer)
    alignment = db.Column(db.String(64))
    birthsign = db.Column(db.String(64))
    birthsign_effect = db.Column(db.String(128))
    languages = db.Column(db.String(128), nullable=True)
    last_updated = db.Column(db.DateTime())
    patron = db.Column(db.String(128), nullable=True)
    spells_known = db.Column(db.String(128), nullable=True)
    inventory = db.Column(db.String(128), nullable=True)
    proficient_weapons = db.Column(db.String(128), nullable=True)
    lucky_weapon = db.Column(db.String(64), nullable=True)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
