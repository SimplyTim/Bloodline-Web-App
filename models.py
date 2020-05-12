from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import datetime


db = SQLAlchemy(engine_options={"pool_recycle":60})

class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, nullable=False)
    password = db.Column('password', db.String(128),  nullable=False)
    userType = db.Column('type', db.String(1), nullable=False)
    fName = db.Column('fName', db.String(20), nullable=False)
    lName = db.Column('lName', db.String(20), nullable=False)
    age = db.Column('age', db.String(3), nullable=False)
    DOB = db.Column('DOB', db.String(15), nullable=False)
    bloodGroup = db.Column('bloodGroup', db.String(10), nullable=True)
    bloodCentreId = db.Column('bloodCentreId', db.Integer, db.ForeignKey('blood_centre.centreId'), nullable=True)
    bloodcentre = db.relationship('BloodCentre')

    def toDict(self):
        return {
        "id": self.id,
        "username": self.username,
        "password":self.password,
        "userType": self.userType,
        "fName": self.fName,
        "lName": self.lName,
        "age": self.age,
        "DOB": self.DOB,
        "bloodGroup": self.bloodGroup,
        "bloodCentreId": self.bloodCentreId
        }

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def addBloodType(self, bloodType):
        self.bloodGroup = bloodType

    def setBloodCentre(self, centreId):
        self.bloodCentreId = centreId

class BloodCentre(db.Model):
    centreId = db.Column('centreId', db.Integer, primary_key=True)
    centreName = db.Column('centreName', db.String(50), nullable=False)
    centreAddress = db.Column('centreAddress', db.String(100), nullable=False)

    def toDict(self):
        return {
        "centreId": self.centreId,
        "centreName": self.centreName,
        "centreAddress": self.centreAddress
        }

class Appointment(db.Model):
    aptId = db.Column('aptId', db.Integer, primary_key=True)   
    date = db.Column('date', db.String(15), nullable=False)
    time = db.Column('time', db.String(10), nullable=False)
    centreId = db.Column('centreId', db.Integer, db.ForeignKey('blood_centre.centreId'), nullable=False)
    userId = db.Column('userId', db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column('status', db.String(10), default="Scheduled")
    bloodcentre = db.relationship('BloodCentre')
    user = db.relationship('User')

    def toDict(self):
        return {
        "aptId": self.aptId,
        "date": self.date,
        "time": self.time,
        "centreId": self.centreId,
        "userId":self.userId,
        "status":self.status
        }


