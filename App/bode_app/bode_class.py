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


@bode.route('/stats', methods=['GET', 'POST'])
@login_required
def class_stats():
    if current_user.type == 'admin':
        if request.method == 'GET':
            all_classes = Class.query.order_by(Class.date).all()
            return render_template('UserProfiles/admin/class_stats.html', classes=all_classes)
        elif request.method == 'POST':
            id = request.json.get('class_id')
            users = User.query.filter_by(class_id=id).all()
            returnTag = ''
            for user in users:
                print(user)
                returnTag += '<div id={0}>{0}</div><hr/><br/>'.format(user.username)
            return returnTag
    else:
        flash('Not Authorised')
        redirect('/user')

