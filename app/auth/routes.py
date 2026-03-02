from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from ..models import User, LoginLog
from .. import db
from ..models import LoginLog
from .. import db

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed = generate_password_hash(password)

        user = User(username=username, password_hash=hashed)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            session.permanent = True

            log = LoginLog(
            user_id=user.id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get("User-Agent")
            )
            db.session.add(log)
            db.session.commit()

            session["log_id"] = log.id

            return redirect(url_for("main.protected"))

    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    log_id = session.get("log_id")

    if log_id:
        log = LoginLog.query.get(log_id)
        if log:
            log.logout_time = datetime.utcnow()
            db.session.commit()

        logout_user()
    return redirect(url_for("main.home"))


