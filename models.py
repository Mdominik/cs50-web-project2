from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

subs = db.Table('subs',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'))
        )

msgs = db.Table('msgs',
        db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('channel_id', db.Integer, db.ForeignKey('channels.id')),
        db.Column('message_id', db.Integer, db.ForeignKey('messages.id'))
        )

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    channelsOfUser = db.relationship('Channel', secondary = subs, 
    backref=db.backref('subscribers', lazy = 'dynamic'))  
    

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    msgsOfChannel = db.relationship('Message', secondary = msgs, 
    backref=db.backref('msgs', lazy = 'dynamic')) 


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    text = db.Column(db.String, nullable=False)
