from models import db, User, BloodCentre, Appointment
from main import app

db.drop_all()
db.create_all(app=app)
admin = User(username="admin1", email="admin@mail.com", userType="a")
admin.set_password("pass")
db.session.add(admin)
db.session.commit()