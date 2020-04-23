from models import db, User, Host, BloodCentre, Appointment
from main import app

db.create_all(app=app)