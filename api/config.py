import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = '1111'
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')