from . import bode, db
from flask import request, redirect, flash, render_template
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import json
from .models import Class, User
import string
import random


def createFromJson(class_name, class_data):
    current_class = Class(name=class_name)
    db.session.add(current_class)
    db.session.commit()
    for c in class_data:
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        current_student = User(username=c.split('@')[0],
                               first_login=True,
                               class_id=current_class.id,
                               type='student',
                               email=c,
                               password=generate_password_hash(password))
        print(c, password)
        db.session.add(current_student)
    db.session.commit()


@bode.route('/create_class', methods=['POST'])
@login_required
def create_class():
    class_json = request.files.get('class_json', '')
    name = request.form.get('class_name')
    path = 'App/Class_Json/{0}.json'.format(name)
    ext = class_json.filename.split('.')[-1]
    if ext == 'txt':
        try:
            class_json.save(path)
            class_json.close()
            class_data = json.loads(open(path, newline='').read())['email']
            createFromJson(name, class_data)
        except:
            flash('Something went wrong in the upload')
    return redirect('/')


@bode.route('/Stats', methods=['GET', 'POST'])
@login_required
def class_stats():
    if current_user.type == 'admin':
        if request.method == 'GET':
            return render_template('UserProfiles/admin/class_stats.html')
    else:
        flash('Not Authorised')
        redirect('/user')


@bode.route('/Messaging', methods=['GET', 'POST'])
@login_required
def messaging():
    if current_user.type == 'admin':
        if request.method == 'GET':
            return render_template('UserProfiles/admin/messaging.html')
