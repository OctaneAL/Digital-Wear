from api import db, app

class UserType(db.Model):
    __tablename__ = "UserType"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(30), nullable = False)
    clients = db.relationship('Client', backref='type', lazy=True)
