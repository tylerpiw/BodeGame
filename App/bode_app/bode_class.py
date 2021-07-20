from . import bode, db
from flask import request, redirect, flash, render_template
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import json
from .models import Class, User, GameLevels, GameData
import string
import random


def createFromJson(class_name, class_data):
    current_class = Class(name=class_name, type='active')
    db.session.add(current_class)
    for c in class_data:
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        current_student = User(username=c.split('@')[0],
                               class_id=current_class.id,
                               type='student',
                               email=c,
                               password=generate_password_hash(password))
        print(c, password)
        db.session.add(current_student)
        student_data = GameData(student_id=current_student.id, level=0, score=0)
        db.session.add(student_data)
        current_student.game_data.append(student_data)
        current_class.students.append(current_student)
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


def class_stats_get():
    all_classes = Class.query.order_by(Class.date).all()
    return render_template('UserProfiles/admin/class_stats.html', classes=all_classes)


def class_stats_post():
    class_id = request.json.get('class_id')
    users = User.query.filter_by(class_id=class_id).all()
    returnTag = '<tr><th>Rank</th><th>Username</th><th>Level</th><th>Score</th></tr>'
    for user in users:
        returnTag += '<tr id={0}>' \
                        '<td>1</td>' \
                        '<td>{0}</td>' \
                        '<td>{1}</td>' \
                        '<td>{2}</td>' \
                     '</tr>'.format(user.username, user.game_data[0].level, user.game_data[0].score)

    print(returnTag)
    return returnTag


def class_archive():
    class_id = request.json.get('class_id')
    class_ = Class.query.filter_by(id=class_id).first()
    class_.type = 'archived'
    db.session.commit()
    return 'class archived'


def class_delete():
    class_id = request.json.get('class_id')
    class_ = Class.query.filter_by(id=class_id).first()
    db.session.delete(class_)
    db.session.commit()
    rem = User.query.order_by(User.id).all()
    for i in rem:
        print(i.id, i.username)
    return 'class deleted'


actionDictionary = {
    'GET': {
        'class_stats_get': class_stats_get
    },
    'POST': {
        'class_stats_post': class_stats_post,
        'class_archive': class_archive,
        'class_delete': class_delete
    }
}


@bode.route('/class/<action>', methods=['GET', 'POST'])
@login_required
def class_actions(action):
    if current_user.type == 'admin':
        return actionDictionary[request.method][action]()
    else:
        flash('Not Authorised')
        redirect('/user')


@bode.route('/addGame', methods=['POST'])
@login_required
def addGame():
    if current_user.type == 'admin':
        level = GameLevels.query.count()+1
        answer = request.form.get('level_answer')
        new = GameLevels(level=level, answer=answer)
        db.session.add(new)
        db.session.commit()
        return redirect('/user')
    else:
        flash('Not Authorised')
        redirect('/user')

