import os

from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit

from models import *

app = Flask(__name__)
db.init_app(app)
app.config["SECRET_KEY"] = "dffac644b59fd707a3c818a488c8be058b3790df1961195fb79555771bb30e6a"
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
socketio = SocketIO(app)
db.init_app(app)

def someoneLoggedIn():
    if session["user_id"] == 0:
        pass
    else:
        return True
 
def getUserID(user):
    number = User.query.filter_by(id=session["user_id"]).all()
    if number is not None:
        return number
    else:
        return None

def isUserFree(name):
    u = len(User.query.filter_by(username=name).all())
    print(u)
    return u == 0

def isChannelFree(channelName):
    ch = len(Channel.query.filter_by(name=channelName).all())
    return ch == 0
 
@app.route("/", methods=["GET"])
def home():
    return render_template('login.html', title='Welcome to Slack!', usernameFree = True)     

@app.route("/isNameAccepted", methods=["POST"])
def isNameAccepted():
    if request.method == "POST":
        username = request.form.get("username")
        usernameFree = isUserFree(username)
        if usernameFree:
            newUser = User(username=username)
            db.session.add(newUser)
            db.session.commit()
            return redirect("/chatList", code=302)
        return render_template('login.html', title='Welcome to Slack!', usernameFree = usernameFree)

@app.route("/chat")
def chatList():
    return render_template('chat.html', title='chat')


with app.app_context():
    db.create_all()