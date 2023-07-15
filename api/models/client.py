from api import db, app
from datetime import datetime
from sqlalchemy_utils import URLType
from UserType import UserType

class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique = True,nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    photo = db.Column(db.LargeBinary, nullable=True)
    description = db.Column(db.String(300), nullable=True)
    password = db.Column(db.String(300), nullable=False)
    auth_token = db.Column(db.String(300), nullable=True)
    type = db.Column(db.Integer, db.ForeignKey('UsetType.id'), nullable=False) 
    portfolio_url = db.Column(URLType, nullable=True)
    registered = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self):
        pass # todo ???