from api import db, app

class ProductType(db.Model):
    __tablename__ = "ProductType"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    name = db.Column(db.String(30), nullable = False)
    products = db.relationship('Product', backref='type', lazy=True)
