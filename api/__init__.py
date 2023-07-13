from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

# from config import SECRET_KEY

app = Flask(__name__)
api = Api(app)

# app.config['SECRET_KEY'] = SECRET_KEY
# app.config['SQLALCHEMY_DATABAUSE_URI'] = SQLALCHEMY_DATABAUSE_URI
# app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
ma = Marshmallow(app)
db.init_app(app)