from models import db, User, BloodCentre, Appointment
from main import app

db.drop_all()
db.create_all(app=app)
admin = User(username="tim", email="tim@mail.com", userType="a", name="Timothy Singh", age="22", DOB="15/01/1998")
admin.set_password("pass")
db.session.add(admin)
db.session.commit()