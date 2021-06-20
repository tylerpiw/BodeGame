from flask import Flask, blueprints
from .bode_app import bode

def bode_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'qwertyuiop0192837465'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    from .bode_app import db, login
    db.init_app(app)
    # db.create_all()
    # login.init_app(app)
    app.register_blueprint(bode)
    return app