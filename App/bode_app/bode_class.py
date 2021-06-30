from . import bode, db
from flask import request, redirect, flash
from flask_login import login_required
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
                       class_id=current_class.id,
                       type='student',
                       email=c,
                       password='replace',
                       temp_password=password)
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
def leaderboard(x):
  x =[]
  for g in x:
    if g != x:
      x.append(g)
    else:
      print (g)
  
import ctypes, sys

def admin_powers():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    else:
        return False

if admin_powers():
    
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
