from . import bode, login_manager, db
from flask import request, render_template, redirect, flash
from .models import User, Class
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, login_user, logout_user, current_user
import re


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
        if not current:
            flash('User does not exits')
        elif check_password_hash(current.password, password):
            login_user(current)
        return redirect('/user')


@bode.route('/set_password', methods=['POST'])
@login_required
def changePassword():
    old_password = request.form.get('old-password', '')
    new_password = request.form.get('new-password', '')
    confirm_password = request.form.get('confirm-password', '')

    # checking if new password checks all the minimum Conditions

    password = new_password
    Condition = ""
    lengthOfPassword = len(password)

    if (lengthOfPassword < 8):
        Condition += "\n minimum 8 characters required"

    if not re.search("[a-z]", password):
        Condition += "\n minimum 1 Lowercase character required"

    if not re.search("[A-Z]", password):
        Condition += "\n minimum 1 Uppercase character required"

    if not re.search("\d", password):
        Condition += "\n minimum 1 numerical digit required "

    if not re.search("[_@$]", password):
        Condition += "\n minimum 1 special character required"

    if re.search("\s", password):
        Condition += "\n no whitespace character"

    if password == old_password:
        Condition += '\n New Password same as old Password'

    if password != confirm_password:
        Condition += "\n Passwords don't Match"

    if Condition != "":
        flash("Not a Valid Password as \n" + Condition)
    else:
        # Valid Password
        flash('password changed!')
        current_user.password = generate_password_hash(new_password)
        current_user.first_login = False
        db.session.commit()
        return redirect('/user')


@bode.route('/user')
@login_required
def profile():
    if current_user.type == 'admin':
        all_classes = Class.query.order_by(Class.date).all()
        return render_template('UserProfiles/admin/home.html', classes=all_classes)
    else:
        return render_template('UserProfiles/student/home.html')


@bode.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
