import json
from flask_cors import CORS
from flask import Flask, request, render_template
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 
from flask_jwt import JWT, jwt_required, current_identity

from models import db


from models import db, User, BloodCentre, Appointment

''' Begin boilerplate code '''
def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) 
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here '''
def authenticate(emailAdd, password):
  user = User.query.filter_by(email=emailAdd).first()
  if user and user.check_password(password):
    return user

def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

@app.route('/')
def index():
    return "Welcome to Bloodline."


@app.route('/app')      #just for testing stuff
def client_app():
    return app.send_static_file('googlemaps.html')


#****************************************
#******************USER******************
#****************************************
@app.route('/user', methods=['POST'])
def signUpUser():
    userdata = request.get_json() # get userdata
    newuser = User(username=userdata['username'], email=userdata['email']) # create user object
    newuser.set_password(userdata['password']) # set password
    try:
        db.session.add(newuser)
        db.session.commit() # save user
    except IntegrityError: # attempted to insert a duplicate user
        db.session.rollback()
        return 'username or email already exists' # error message
    return 'user created' # success

@app.route('/user/<id>', methods=['GET'])
@jwt_required()
def get_user(id):
    user = User.query.filter_by(id=current_identity.id).first()
    if len(user) == 0:
        return "Invalid id or unauthorized"
    return json.dumps(user.toDict())

@app.route('/users', methods=['GET'])
@jwt_required()
def getUsers():
    users = User.query.filter_by(id=current_identity.id).all()
    users = [User.toDict() for user in users] # list comprehension which converts user objects to dictionaries
    return json.dumps(users)

@app.route('/user/<id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.filter_by(id=current_identity.id).first()
    if user == None:
        return 'Invalid id or unauthorized'
    db.session.delete(user) # delete the object
    db.session.commit()
    return 'Deleted', 204
    


#************************************
#******************APPOINTMENT*******
#************************************
@app.route('/appointment', methods=['POST'])
def signUpAppointment():
    appointmentdata = request.get_json() # get appointmentdata
    newappointment = Appointment(dateTime=appointmentdata['dateTime'], centreId=appointmentdata['centreId'], userId=appointmentdata['userId']) # create appointment object

    try:
        db.session.add(newappointment)
        db.session.commit() # save appointment
    except IntegrityError: # attempted to insert a duplicate appointment
        db.session.rollback()
        return 'appointment already exits' # error message
    return 'appointment created' # success

@app.route('/appointment/<id>/centre', methods=['GET'])
@jwt_required()
def get_appointment_centre(id):
    appointment = Appointment.query.filter_by(centreId=current_identity.id).first()
    if appointment == None:
        return 'Invalid id or unauthorized'
    return json.dumps(appointment.toDict())

@app.route('/appointment/<id>/user', methods=['GET'])
@jwt_required()
def get_appointment_user(id):
    appointment = Appointment.query.filter_by(userId=current_identity.id).first()
    if appointment == None:
        return 'Invalid id or unauthorized'
    return json.dumps(appointment.toDict())

@app.route('/appointments', methods=['GET'])
@jwt_required()
def getAppointments():
    appointments = Appointment.query.filter_by(aptId=current_identity.id).all()
    appointments = [Appointment.toDict() for appointment in appointments] # list comprehension which converts appointment objects to dictionaries
    return json.dumps(appointments)

@app.route('/appointment/<id>', methods=['DELETE'])
@jwt_required()
def delete_Appointment(id):
    appointment = Appointment.query.filter_by(aptId=current_identity.id).first()
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
@jwt_required()
def get_bloodcentre(id):
    bc = BloodCentre.query.filter_by(centreId=current_identity.id).first()
    if bc == None:
        return 'Invalid id or unauthorized'
    return json.dumps(bc.toDict())

@app.route('/bloodcentres', methods=['GET'])
@jwt_required()
def getBloodCentres():
    bc = BloodCentre.query.filter_by(centreId=current_identity.id).all()
    bc = [BloodCentre.toDict() for b in bc] # list comprehension which converts bloodcentre objects to dictionaries
    return json.dumps(bc)

@app.route('/bloodcentre/<id>', methods=['DELETE'])
@jwt_required()
def deleteCentre(id):
    bc =BloodCentre.query.filter_by(centreId=current_identity.id).first()
    if bc == None:
        return 'Invalid id or unauthorized'
    db.session.delete(bc) # delete the object
    db.session.commit()
    return 'Deleted', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)