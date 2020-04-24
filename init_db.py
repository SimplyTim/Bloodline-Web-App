from models import db, User, BloodCentre, Appointment
from main import app

db.drop_all()
db.create_all(app=app)
admin = User(username="admin1", email="admin@mail.com", password="pass", userType="a")
db.session.add(admin)
db.session.commit()