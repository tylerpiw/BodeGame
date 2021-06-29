from . import bode, login_manager, db
from flask import request, render_template, redirect, flash
from .models import User, Class
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@bode.route('/', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/user')
    elif request.method == 'GET':
        return render_template('Login/Login.html')
    elif request.method == 'POST':
        username = request.form.get("login-username", '')
        password = request.form.get("login-password", '')
        current = User.query.filter_by(username=username).first()
        print(current)
        if not current:
            flash('User does not exits')
        elif current.password == 'replace':
        elif check_password_hash(current.password, password):
            login_user(current)
        return redirect('/user')


@bode.route('/set_password', methods=['POST'])
@login_required
def changePassword():
    old_password = request.form.get('old-password', '')
    new_password = request.form.get('new-password', '')
    confirm_password = request.form.get('confirm-password', '')
    if new_password != confirm_password:
        flash('passwords don\'t match')
    elif old_password == current_user.temp_password:
        flash('password changed!')
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
    return redirect('/user')


@bode.route('/user')
@login_required
def profile():
    if current_user.type == 'admin':
        all_classes = Class.query.order_by(Class.date).all()
        return render_template('UserProfiles/admin_user_profile.html', classes=all_classes)
    else:
        return render_template('UserProfiles/student_user_profile.html',
                               firstLogin=(current_user.password == 'replace'))

@bode.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
