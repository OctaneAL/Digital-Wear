from api import db, app
from datetime import datetime
from sqlalchemy_utils import URLType
from sqlalchemy.dialects.postgresql import ARRAY
from flask_login import UserMixin

class UserType(db.Model):
    __tablename__ = "UserType"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(30), nullable = False)

    client = db.relationship('Client', back_populates='client_type')


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
    portfolio_url = db.Column(URLType, nullable=True)
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    client_type_id = db.Column(db.Integer, db.ForeignKey('UserType.id'), nullable=False)

    favourite_products = db.relationship('FavouriteProducts', back_populates='client')
    client_type = db.relationship('UserType', back_populates='client')
    product = db.relationship('Product', back_populates='client')

    def __init__(self):
        pass # todo ???

class FavouriteProducts(db.Model):
    __tablename__ = "FavouriteProducts"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable=False)

    product = db.relationship('Product', back_populates='favourite_products')
    client = db.relationship('Client', back_populates='favourite_products')

class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    logo = db.Column(db.String)  
    promo_images = db.Column(db.ARRAY(db.String))  
    web_site = db.Column(db.String)  
    description = db.Column(db.String(300), nullable=False)
    product_type_id = db.Column(db.Integer, db.ForeignKey('ProductType.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable=False)

    product_type = db.relationship('ProductType', back_populates='products')
    favourite_products = db.relationship('FavouriteProducts', back_populates='product')
    client = db.relationship('Client', back_populates='product')

class ProductType(db.Model):
    __tablename__ = "ProductType"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)

    # One-to-many relationship with Product
    products = db.relationship('Product', back_populates='product_type')
