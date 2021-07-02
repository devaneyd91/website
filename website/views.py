from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

    