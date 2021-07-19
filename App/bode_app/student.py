from . import bode, db
from flask_login import login_required, current_user
from flask import request, render_template, redirect, flash
from .models import GameData, GameLevels

@bode.route('/messaging', methods=['GET', 'POST'])
@login_required
def messaging():
    if current_user.type == 'admin':
        if request.method == 'GET':
            return render_template('UserProfiles/admin/messaging.html')
    elif current_user.type == 'student':
        if request.method == 'GET':
            return render_template('UserProfiles/student/messaging.html')


@bode.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    if request.method == 'GET':
        levels = GameLevels.query.count()
        return render_template('UserProfiles/student/game.html', levels=levels,
                               level=current_user.game_level)
    elif request.method == 'POST':
        guess = int(request.form.get('guess'))
        level = GameLevels.query.filter_by(level=current_user.game_level).first()
        if guess == level.answer:
            flash('Correct Answer!')
        return redirect('/game')


@bode.route('/leaderboard')
@login_required
def leaderboard():
    return render_template('UserProfiles/student/leaderboard.html')
