from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

db = SQLAlchemy()

class User(db.Model):
    userId = db.Column('userId', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False)
    email = db.Column('email', db.String(50), unique=True, nullable=True)
    password = db.Column('password', db.String(32), unique=True, nullable=False)

    def toDict(self):
        return {
        "userId": self.userId,
        "username": self.username,
        "email": self.email,
        "password":self.password
        }

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Host(db.Model):
    hostId = db.Column('hostId', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False)
    email = db.Column('email', db.String(50), unique=True, nullable=True)
    password = db.Column('password', db.String(32), unique=True, nullable=False)

    def toDict(self):
        return {
        "hostId": self.hostId,
        "username": self.username,
        "email": self.email,
        "password":self.password
        }

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class BloodCentre(db.Model):
    centreId = db.Column('centreId', db.Integer, primary_key=True)
    centreName = db.Column('centreName', db.String(50), nullable=False)
    centreAddress = db.Column('centreAddress', db.String(100), nullable=False)
    hostId = db.Column('host', db.Integer, db.ForeignKey('host.hostId'), nullable=False)
    host = db.relationship('Host')

    def toDict(self):
        return {
        "centreId": self.centreId,
        "centreName": self.centreName,
        "centreAddress": self.centreAddress,
        "manager":self.manager
        }

class Appointment(db.Model):
    aptId = db.Column('aptId', db.Integer, primary_key=True)   
    dateTime = db.Column('dateTime', db.datetime, nullable=False)
    centreId = db.Column('centreId', db.Integer, db.ForeignKey('centre.centreId'), nullable=False)
    userId = db.Column('centreId', db.Integer, db.ForeignKey('user.userId'), nullable=False)
    centre = db.relationship('BloodCentre')
    user = db.relationship('User')