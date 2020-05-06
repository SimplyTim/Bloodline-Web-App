from models import db, User, BloodCentre, Appointment
from main import app

db.drop_all()
db.create_all(app=app)
admin = User(username="tim", userType="a", fName="Timothy", lName="Singh", age="22", DOB="15/01/1998")
admin.set_password("pass")
db.session.add(admin)


bc1 = BloodCentre(centreName="Port-of-Spain General Hospital", centreAddress="")
bc2 = BloodCentre(centreName="Eric Williams Medical Sciences Complex", centreAddress="")
bc3 = BloodCentre(centreName="Sangre Grande Hospital", centreAddress="")
bc4 = BloodCentre(centreName="Scarborough Hospital", centreAddress="")
bc5 = BloodCentre(centreName="San Fernando General Hospital", centreAddress="")
bc6 = BloodCentre(centreName="Point Fortin Area Hospital", centreAddress="")
db.session.add(bc1)
db.session.add(bc2)
db.session.add(bc3)
db.session.add(bc4)
db.session.add(bc5)
db.session.add(bc6)

db.session.commit()