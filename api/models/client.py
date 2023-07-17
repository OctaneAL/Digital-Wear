from api import db, app
from datetime import datetime
from sqlalchemy_utils import URLType

class Client(db.Model):
    __tablename__ = 'Client'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(30), unique = True,nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    photo = db.Column(db.LargeBinary, nullable=True)
    description = db.Column(db.String(300), nullable=True)
    password = db.Column(db.String(300), nullable=False)
    auth_token = db.Column(db.String(300), nullable=True)
    type = db.Column(db.Integer, db.ForeignKey('UserType.id'), nullable=False) 
    portfolio_url = db.Column(URLType, nullable=True)
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    products = db.relationship('product', backref='client', lazy=True)
    favourite_products = db.relationship('FavouriteProducts', backref='client', lazy=True)

    def __init__(self):
        pass # todo ???