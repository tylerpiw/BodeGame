from flask import Flask
from .bode_app import bode, models
from werkzeug.security import generate_password_hash

def bode_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'bodePlot'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///temp/Post2.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    from .bode_app import db, login_manager
    login_manager.init_app(app)
    login_manager.login_view = '/'
    db.init_app(app)
    with app.app_context():
        db.create_all()
        if models.User.query.filter_by(username='Test_Admin').first() == None:
            admin = models.User(username='Test_Admin',
                                class_id=-1,
                                type='admin',
                                email='Test_Admin@buffalo.edu',
                                password=generate_password_hash('Test'))
            models.db.session.add(admin)
            models.db.session.commit()
    app.register_blueprint(bode)
    return app