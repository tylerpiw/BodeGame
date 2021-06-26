from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

bode = Blueprint('application', __name__, template_folder='templates', static_folder='static')
db = SQLAlchemy()
login_manager = LoginManager()

from . import models, user_accounts

