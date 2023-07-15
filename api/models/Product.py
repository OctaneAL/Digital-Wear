from api import db, app
from datetime import datetime
from sqlalchemy_utils import URLType, Array

class Product(db.Model):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(100), nullable = False)
    logo = db.Column(URLType)
    promo_images = db.Column(Array(URLType))
    web_site = db.Column(URLType, nullable = True)
    description = db.Column(db.String(300), nullable = False)
    type = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False) 
    client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False) 
    registered = db.Column(db.DateTime, default=datetime.utcnow)
    favourite_products = db.relationship('FavouriteProducts', backref='product', lazy=True)
