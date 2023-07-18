from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .config import SECRET_KEY, SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
migrate.init_app(app, db)
ma = Marshmallow(app)

from api.models.UserType import UserType
from api.models.Client import Client
from api.models.FavouriteProduct import FavouriteProducts
from api.models.Product import Product
from api.models.ProductType import ProductType

with app.app_context():
    print(UserType.query.all())
    print(Client.query.all())
    print(FavouriteProducts.query.all())
    print(Product.query.all())
    print(ProductType.query.all())


# db.init_app(app)