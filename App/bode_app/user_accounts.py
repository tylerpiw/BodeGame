from . import bode, login_manager
from flask import request, render_template, redirect
from .models import User
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@bode.route('/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/user')
    elif request.method == 'GET':
        return render_template('Login.html')
    elif request.method == 'POST':
        username = request.form.get("login-username", '')
        password = request.form.get("login-password", '')
        current = User.query.filter_by(username=username).first()
        if check_password_hash(current.password, password):
            login_user(current)
        return redirect('/user')

@bode.route('/user')
@login_required
def profile():
    return render_template('User_Profile.html', name=current_user.username)

@bode.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
