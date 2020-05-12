from models import db, User, BloodCentre, Appointment
from main import app

db.drop_all()

db.create_all(app=app)
admin1 = User(username="tim", userType="a", fName="Timothy", lName="Singh", age="22", DOB="15/01/1998")
admin2 = User(username="akeel", userType="a", fName="Akeel", lName="Henry", age="21", DOB="09/03/1999")
admin3 = User(username="kumar", userType="a", fName="Kumar", lName="Etwaroo", age="20", DOB="03/10/1999")
admin4 = User(username="romario", userType="a", fName="Romario", lName="Chung", age="22", DOB="15/04/1998")
admin1.set_password("pass")
admin2.set_password("pass")
admin3.set_password("pass")
admin4.set_password("pass")
db.session.add(admin1)
db.session.add(admin2)
db.session.add(admin3)
db.session.add(admin4)


bc1 = BloodCentre(centreName="Port-of-Spain General Hospital", centreAddress="160 Charlotte Street, Port-of-Spain")
bc2 = BloodCentre(centreName="Eric Williams Medical Sciences Complex", centreAddress="Uriah Butler Highway, Champ Fleurs")
bc3 = BloodCentre(centreName="Sangre Grande Hospital", centreAddress="Ojoe Road, Sangre Grande")
bc4 = BloodCentre(centreName="Scarborough Hospital", centreAddress="Connector Road, Signal Hill, Scarborough, Tobago")
bc5 = BloodCentre(centreName="San Fernando General Hospital", centreAddress="Paradise Pasture, Independence Avenue, San Fernando")
bc6 = BloodCentre(centreName="Point Fortin Area Hospital", centreAddress="Volunteer Road, Mahaica Road, Point Fortin")
db.session.add(bc1)
db.session.add(bc2)
db.session.add(bc3)
db.session.add(bc4)
db.session.add(bc5)
db.session.add(bc6)

db.session.commit()