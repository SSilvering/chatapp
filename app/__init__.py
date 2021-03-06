from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object('config')

with app.app_context():
    db.init_app(app)

    db.create_all()


from app import routes