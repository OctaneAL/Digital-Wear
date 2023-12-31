from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER
from flask_login import LoginManager



app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLACLHEMY_TRACK_MODIFICATIONS'] = True
app.config['UPLOADED_PHOTOS_DEST'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
migrate.init_app(app, db)
ma = Marshmallow(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# db.init_app(app)