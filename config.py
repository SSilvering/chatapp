import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  # loads enviroment variables

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('TRACK_MODIFICATIONS')