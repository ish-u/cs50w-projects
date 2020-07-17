import requests
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from functools import wraps
from flask_session import Session
from datetime import datetime
app = Flask(__name__)
app.config['SECRET_KEY'] = 'zzzzzzzzzzzz'
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

socketio = SocketIO(app)

#message class
class Message:
    def __init__(self,message,room,time,user):
        self.user = user
        self.room = room
        self.message = message
        self.time = time
    
    #obtain message
    def getMessage(self):
        return self.message
    #obtain room
    def getRoom(self):
        return self.room
    #obtain time
    def getTime(self):
        return self.time

#messages
messages = []
#global variables
users = ["LOL","LMAO"]

#rooms {channels}
room = set(['general','zoom'])

#current_time
now = datetime.now()

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'user_id' in session:
			return f(*args, **kwargs)
		else:
			return redirect('/login')
	return wrap
#index
@app.route("/")
@login_required
def index():
    return render_template("index.html",messages=messages,rooms=room)

#login route
@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == "POST":
        session.clear()
        user = request.form.get("user_id")
        session['user_id'] = user
        if user in users:
            flash("USER EXISTS")
            return render_template("login.html")
        users.append(user)
        session.permanent = True
        return redirect("/")
    elif request.method == "GET":
        return render_template("login.html")


#change route
@socketio.on('change')
def change(data):
    user_id = data["user"]
    old_id = data["old"]
    room = data["room"]
    for message in messages :
        if(message.user == old_id):
            message.user = user_id
    emit('change',{"username":data["user"],"old":old_id},broadcast=True)

#add room
@socketio.on('add_room')
def add_room(data):
    new_room = data["room"]
    if not(new_room in room):
        room.add(new_room)
        emit('add_room',new_room,broadcast=True)


#join room
@socketio.on('join')
def on_join(data):
    username = data["username"]
    room = data["room"]
    join_room(room)
    emit('user_message',{"msg":" has joined the ","username":username,"room":room,"flag":0,"change":0}, room=room)
    

#leave room
@socketio.on('leave')
def on_leave(data):
    username = data["username"]
    room = data["room"]
    leave_room(room)
    emit('user_message',{ "msg":" has left the ","username":username,"room":room,"flag":0,"change":0}, room=room)

#stored Message
@socketio.on('stored_message')
def blast(data):
    room = data["room"]
    for message in messages:
        if message.room == room:
            emit('stored_message', {"username":message.user,"time_stamp":message.time,"msg":message.message})

#user message
@socketio.on('user_message')
def user_message(data):
    msg = data["message"]
    room = data["room"]
    user = data["user"]
    time_stamp = now.strftime("%m/%d %H:%M")
    current_message = Message(msg,room,time_stamp,user)
    messages.append(current_message)
    emit('user_message',{"username":user,"msg":msg,"time_stamp":time_stamp,"flag":1},room=data["room"])

if __name__ == '__main__':
    socketio.run(app,debug=True,)