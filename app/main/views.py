from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from sqlalchemy import desc
from . import main
from app.models import User
from .forms import ProfileForm
from werkzeug.utils import secure_filename
from os import path
from .. import db
from .. import config


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/my_profile", methods=["GET", "POST"])
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


@main.route("/user/<int:id>")
def user_page(id):
    user = User.query.get_or_404(id)
    return render_template("user_page.html", user=user)
