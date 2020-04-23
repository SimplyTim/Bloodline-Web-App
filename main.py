import json
from flask_cors import CORS
from flask import Flask, request, render_template
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 
from flask_jwt import JWT, jwt_required, current_identity

from models import db


from models import db, User, Host, BloodCentre, Appointment

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
def authenticate(uname, password):
  user = User.query.filter_by(username=uname).first()
  if user and user.check_password(password):
    return user

def identity(payload):
  return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

@app.route('/')
def index():
    return "Welcome to Bloodline."