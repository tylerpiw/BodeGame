from . import bode, login_manager
from flask import request, render_template, redirect
from flask_login import login_required, login_user, logout_user, current_user


@bode.route('/create_class', methods=['POST'])
@login_required
def create_class():
    class_csv = request.files.get('class_csv', '')
    name = request.form.get('class_name')
    ext = class_csv.filename.split('.')[-1]
    if ext == 'txt':
        class_csv.save('App/Class_CSV/' + name + '.csv')
    return redirect('/')
