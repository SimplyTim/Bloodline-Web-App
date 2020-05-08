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
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sql10338279:gQYEsx68IE@sql10.freemysqlhosting.net/sql10338279' #need to set up mysql database?
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
    user = User.query.filter_by(username=userDetails['username']).first()
    if user and user.check_password(userDetails['password']):
        token = jwt.encode({'username' : userDetails['username'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=7)}, app.config['SECRET_KEY'])
        return  jsonify({'token' : token.decode('UTF-8')}), 200
    return "Invalid username or password entered.", 401
''' End JWT Setup '''

def getCurrentUser(token):
    userObj = jwt.decode(token,app.config['SECRET_KEY'])
    uname = userObj['username']
    loggedIn = User.query.filter_by(username=uname).first()
    if loggedIn:
        return loggedIn.toDict()
    return None

def convertDate(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

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
    newUser = User(username=userdata['username'], userType=userdata['userType'], fName=userdata['fName'], lName=userdata['lName'], age=userdata['age'], DOB=userdata['DOB'])
    if 'bloodGroup' in userdata:
        newUser.addBloodType(userdata['bloodGroup'])
    
    if userdata['userType'] == 'h':
        newUser.setBloodCentre(userdata['bloodCentreId'])

    newUser.set_password(userdata['password'])
    try:
        db.session.add(newUser)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Username already exists", 400
    return "User created", 200

@app.route('/user', methods=['GET'])
@token_required
def getLoggedInUser():
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    userData = User.query.get(account['id'])
    if userData:
        return json.dumps(userData.toDict()), 200
    return "Details not found.", 404

@app.route('/user/<id>', methods=['GET'])
@token_required
def getUser(id):
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['id'] == int(id) or account['userType']=='a':
        userData = User.query.get(account['id'])
        if userData:
            return json.dumps(userData.toDict()), 200
        return "Invalid user.", 404
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

@app.route('/user/<id>', methods=['PUT'])
@token_required
def editUser(id):
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    editData = request.get_json()
    if account['id'] == int(id) or account['userType']=='a':
        toEdit = User.query.get(int(id))
        if toEdit:
            for key in editData:
                setattr(toEdit, str(key), editData[str(key)])
            db.session.add(toEdit)
            db.session.commit()
            return "Details updated successfully.", 201
        return "Invalid user.", 404
    return "Not authorized to access this page.", 401

@app.route('/user/<id>', methods=['DELETE'])
@token_required
def deleteUser(id):
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['id'] == int(id) or account['userType']=='a':
        toDelete = User.query.get(int(id))
        if toDelete: 
            toDeleteDict = toDelete.toDict()
            if toDeleteDict['userType'] == 'a':
                return "An administrator account cannot be deleted.", 400
            db.session.delete(toDelete)
            db.session.commit()
            return "User deleted.", 204
        return "Invalid user.", 404
    return "Not authorized to access this page.", 401
    

#APPOINTMENT ROUTES

@app.route('/appointment', methods=['POST'])
@token_required
def createAppointment():
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    appointmentData = request.get_json()
    newAppointment = Appointment(date=appointmentData['date'], time=appointmentData['time'], centreId=appointmentData['centreId'], userId=appointmentData['userId'])
    if account['id'] == int(appointmentData['userId']) or account['userType'] =='a':
        try:
            db.session.add(newAppointment)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "Appointment already created.", 400
        return "Appointment created successfully.", 200
    return "Not authorized to access this page.", 401

@app.route('/appointments', methods=['GET'])
@token_required
def getAppointments():
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['userType']=='a':
        appointments = Appointment.query.all()
        if appointments:
            appointmentsList = [appointment.toDict() for appointment in appointments]
            return json.dumps(appointmentsList, default = convertDate), 200
        return "No appointments found.", 404
    return "Not authorized to access this page.", 401

@app.route('/appointment/centre/<centreId>', methods=['GET'])
#@token_required
def getCentreAppointments(centreId):
    #token = request.headers.get('Authorization')
    #account = getCurrentUser(token)
    #if account['userType']=='a' or account['centreId'] == int(centreId):
    appointments = Appointment.query.filter_by(centreId = centreId).all()
    if len(appointments) == 0:
        return "No appointments found for this blood centre or blood centre not found.", 404
    appointmentsList = [appointment.toDict() for appointment in appointments]
    return json.dumps(appointmentsList, default = convertDate), 200
    #return "Not authorized to access this page", 401
  
@app.route('/appointment/user/<userId>', methods=['GET'])
@token_required
def getUserAppointments(userId):
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['userType']=='a' or account['id'] == int(userId):
        appointments = Appointment.query.filter_by(userId = userId).all()
        if len(appointments) == 0:
            return "No appointments found for this user or user not found.", 404
        appointmentsList = [appointment.toDict() for appointment in appointments]
        return json.dumps(appointmentsList, default = convertDate), 200
    return "Not authorized to access this page", 401

@app.route('/appointment/<aptId>', methods=['PUT'])
@token_required
def editAppointment(aptId):
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    editData = request.get_json()
    toEdit = Appointment.query.get(int(aptId))
    if toEdit:
        toEditDict = toEdit.toDict()
        if toEditDict['userId'] == account['id'] or toEditDict['centreId'] == account['bloodCentreId'] or account['userType'] =='a':
            for key in editData:
                setattr(toEdit, str(key), editData[str(key)])
            db.session.add(toEdit)
            db.session.commit()
            return "Details updated successfully.", 201
        return "Not authorized to access this page.", 401
    return "Invalid appointment.", 404


@app.route('/appointment/<aptId>', methods=['DELETE'])
@token_required
def deleteAppointment(aptId):
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['userType']=='a':
        appointment = Appointment.query.get(aptId)
        if appointment:
            db.session.delete(appointment)
            db.session.commit()
            return 'Deleted', 204
        return "Invalid appointment.", 404
    return "Not authorized to access this page.", 401

#BLOOD CENTRE ROUTES

@app.route('/bloodcentre', methods=['POST'])
@token_required
def createBloodCentre():
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['userType']=='a':
        bcData = request.get_json()
        bc = BloodCentre(centreName=bcData['centreName'],centreAddress=bcData['centreAddress'])
        try:
            db.session.add(bc)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "Blood Centre already exists.", 400
        return "Blood Centre created successfully.", 200
    return "Not authorized to access this page.", 401

@app.route('/bloodcentres', methods=['GET'])
def getBloodCentre():
    bc = BloodCentre.query.all()
    bc = [b.toDict() for b in bc]
    if bc:
        return json.dumps(bc), 200
    return "No blood centres in system.", 404

@app.route('/bloodcentre/<id>', methods=['DELETE'])
@token_required
def deleteCentre(id):
    token = request.headers.get('Authorization')
    account = getCurrentUser(token)
    if account['userType']=='a':
        bc = BloodCentre.query.get(int(id))
        if bc:
            db.session.delete(bc) # delete the object
            db.session.commit()
            return "Blood centre deleted successfully.", 204
        return "Invalid id or unauthorized.", 400
    return "Not authorized to access this page.", 401
'''
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
'''