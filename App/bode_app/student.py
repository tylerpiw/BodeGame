from . import bode, db
from flask_login import login_required, current_user
from flask import request, render_template, redirect


@bode.route('/messaging', methods=['GET', 'POST'])
@login_required
def messaging():
    if current_user.type == 'admin':
        if request.method == 'GET':
            return render_template('UserProfiles/admin/messaging.html')
    elif current_user.type == 'student':
        if request.method == 'GET':
            return render_template('UserProfiles/student/messaging.html')


@bode.route('/game')
@login_required
def game():
    return redirect('/static/html/BodeGame.html')


@bode.route('/leaderboard')
@login_required
def leaderboard():
    return render_template('UserProfiles/student/leaderboard.html')
