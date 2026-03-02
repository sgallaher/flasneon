from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import LoginLog

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("home.html")


@main.route("/protected")
@login_required
def protected():
    return render_template("protected.html", user=current_user)
@main.route("/admin")
@login_required
def admin_dashboard():
    logs = LoginLog.query.order_by(LoginLog.login_time.desc()).all()
    return render_template("admin.html", logs=logs)
