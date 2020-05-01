import json
from flask_cors import CORS
from flask import Flask, request, render_template, make_response, jsonify
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 
import jwt
import datetime
from functools import wraps
from flask.views import MethodView

from models import db

from models import db, User, BloodCentre, Appointment

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "SECRET6555"

  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here '''
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message:' : 'Token was not found.'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'message' : 'Token is invalid'}), 403
    return decorated

@app.route('/login', methods=['POST'])
def login():
    userDetails = request.get_json()
    user = User.query.filter_by(email=userDetails['email']).first()
    if user and user.check_password(userDetails['password']):
        token = jwt.encode({'email' : userDetails['email'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=90)}, app.config['SECRET_KEY'])
        return  jsonify({'token' : token.decode('UTF-8')}), 200
    return "Invalid email or password entered.", 401
''' End JWT Setup '''

def getCurrentUser(token):
    userObj = jwt.decode(token,app.config['SECRET_KEY'])
    mail = userObj['email']
    loggedIn = User.query.filter_by(email=mail).first()
    if loggedIn:
        return loggedIn.toDict()
    return None

@app.route('/')
def index():
    return "Welcome to Bloodline."


@app.route('/app')      #just for testing stuff
def client_app():
    return app.send_static_file('googlemaps.html')


#USER ROUTES

@app.route('/user', methods=['POST'])
def signUpUser():
    userdata = request.get_json()
    newUser = User(username=userdata['username'], email=userdata['email'], userType=userdata['userType'])
    newUser.set_password(userdata['password'])
    print(newUser.toDict())
    try:
        db.session.add(newUser)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return 'username or email already exists', 400
    return 'User created', 200

@app.route('/user/<id>', methods=['GET'])
@token_required
def getUser(id):
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['id'] == int(id) or account['userType']=='a':
        users = User.query.all()
        if len(users) == 0 or len(users) < int(id):
            return "Invalid id", 404
        userData = users[int(id)-1]
        return json.dumps(userData.toDict()), 200
    return "Not authorized to access this page", 401

@app.route('/users', methods=['GET'])
@token_required
def getUsers():
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['userType']=='a':
        users = User.query.all()
        if users:
            users = [user.toDict() for user in users]
            return json.dumps(users), 200
        return "No accounts registered in system.", 404
    return "Not authorized to access this page.", 401

@app.route('/user/<id>', methods=['DELETE'])
@token_required #not working idk why
def deleteUser(id):
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['id'] == int(id) or account['userType']=='a':
        toDelete = User.query.get(int(id))
        if toDelete: 
            if toDelete['userType'] == 'a':
                return "An administrator account cannot be deleted.", 400
            db.session.delete(account)
            db.session.commit()
            return "User deleted.", 204
        return "Invalid user.", 404
    return "Not authorized to access this page.", 401
    

#APPOINTMENT ROUTES

@app.route('/appointment', methods=['POST'])
@token_required
def createAppointment():
    appointmentdata = request.get_json()
    newappointment = Appointment(dateTime=appointmentdata['dateTime'], centreId=appointmentdata['centreId'], userId=appointmentdata['userId']) # create appointment object
    try:
        db.session.add(newappointment)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Appointment already created.", 400
    return "Appointment created successfully.", 200

@app.route('/appointments', methods=['GET'])
@token_required
def getAppointments():
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['userType']=='a':
        appointments = Appointment.query.all()
        if appointments:
            appointments = [appointment.toDict() for appointment in appointments]
            return json.dumps(appointments), 200
        return "No appointments found.", 404
    return "Not authorized to access this page.", 401

@app.route('/appointment/<id>/centre', methods=['GET'])
#@jwt_required()
def get_appointment_centre(id):
    appointment = Appointment.query.filter_by().first()
    if appointment == None:
        return 'Invalid id or unauthorized'
    return json.dumps(appointment.toDict())

@app.route('/appointment/<id>/user', methods=['GET'])
#@jwt_required()
def get_appointment_user(id):
    appointment = Appointment.query.filter_by().first()
    if appointment == None:
        return 'Invalid id or unauthorized'
    return json.dumps(appointment.toDict())



@app.route('/appointment/<id>', methods=['DELETE'])
#@jwt_required()
def delete_Appointment(id):
    appointment = Appointment.query.filter_by().first()
    if appointment == None:
        return 'Invalid id or unauthorized'
    db.session.delete(appointment) # delete the object
    db.session.commit()
    return 'Deleted', 204

#************************************
#******************BLOODCENTRE*******
#************************************

@app.route('/bloodcentres', methods=['POST'])
def signUpBloodCentre():
    bcdata = request.get_json() # get bcdata
    bc= BloodCentre(centreName=bc['centreName'],centreAddress=bc['centreAddress'],  hostId=bc['hostId']) # create bloodcentre object

    try:
        db.session.add(bc)
        db.session.commit() # save bloodcentre
    except IntegrityError: # attempted to insert a duplicate
        db.session.rollback()
        return 'appointment already exits' # error message
    return 'appointment created' # success

@app.route('/bloodcentre/<id>', methods=['GET'])
#@jwt_required()
def get_bloodcentre(id):
    bc = BloodCentre.query.filter_by().first()
    if bc == None:
        return 'Invalid id or unauthorized'
    return json.dumps(bc.toDict())

@app.route('/bloodcentres', methods=['GET'])
#@jwt_required()
def getBloodCentres():
    bc = BloodCentre.query.filter_by().all()
    bc = [BloodCentre.toDict() for b in bc] # list comprehension which converts bloodcentre objects to dictionaries
    return json.dumps(bc)

@app.route('/bloodcentre/<id>', methods=['DELETE'])
#@jwt_required()
def deleteCentre(id):
    bc =BloodCentre.query.filter_by().first()
    if bc == None:
        return 'Invalid id or unauthorized'
    db.session.delete(bc) # delete the object
    db.session.commit()
    return 'Deleted', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)