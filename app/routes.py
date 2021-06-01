from os import uname
from app import app, db
from app.models import Chat
from flask import render_template, request, redirect
from datetime import datetime

@app.route('/', methods=['GET'])
def index():
    ''' creates a new database file if it does not exist '''
    db.create_all()
    db.session.commit()
    return render_template('index.html', title='Chat APP')

@app.route('/<room>', methods=['GET'])
def room(room):
    return render_template('index.html', title='Chat APP')

@app.route('/api/chat/<room>', methods=['GET', 'POST'])    
def room_manage(room):
    if request.method == 'GET':
        res = ''
        if not Chat.query.filter_by(room=room).all():
            return f'No Messages\n\n{uname()}'

        for row in Chat.query.filter_by(room=room).all():
            res += f'[{row.created_at.strftime("%Y-%m-%d %H:%M:%S")}] {row.username}: {row.msg}\n'
        return f'{res}\n{uname()}'

    elif request.method == 'POST':
        new_msg = Chat(
            username=request.form['username'],
            msg=request.form['msg'],
            room=room
        )
        db.session.add(new_msg)
        try:
            db.session.commit()
        except:
            db.session.rollback()                       


    return render_template('index.html')