from api import db, app
from datetime import datetime

class FavouriteProducts(db.Model):
    __tablename__ = "FavouriteProducts"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    client = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    product = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) 
    registered = db.Column(db.DateTime, default=datetime.utcnow)
