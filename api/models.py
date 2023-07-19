from api import db, app
from datetime import datetime
from sqlalchemy_utils import URLType
from sqlalchemy.dialects.postgresql import ARRAY
from flask_login import UserMixin

class Client(db.Model, UserMixin):
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
    products = db.relationship('Product', backref='Client', lazy=True)
    favourite_products = db.relationship('FavouriteProducts', backref='Client', lazy=True)

    def __init__(self):
        pass # todo ???

class FavouriteProducts(db.Model):
    __tablename__ = "FavouriteProducts"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    client = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable=False)
    product = db.Column(db.Integer, db.ForeignKey('Product.id'), nullable=False) 
    registered = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    logo = db.Column(URLType)
    promo_images = db.Column(ARRAY(URLType))
    web_site = db.Column(URLType, nullable = True)
    description = db.Column(db.String(300), nullable = False)
    type = db.Column(db.Integer, db.ForeignKey('UserType.id'), nullable=False) 
    client = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable=False) 
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    favourite_products = db.relationship('FavouriteProducts', backref='Product', lazy=True)

class ProductType(db.Model):
    __tablename__ = "ProductType"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(30), nullable = False)
    products = db.relationship('Product', backref='UserType', lazy=True)

class UserType(db.Model):
    __tablename__ = "UserType"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(30), nullable = False)
    clients = db.relationship('Client', backref='UserType', lazy=True)
