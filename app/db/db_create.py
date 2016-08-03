import os
import sys
from flask import Flask
from app.database import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../db/dbTest.db'
db.init_app(app)

with app.app_context():
    db.create_all()
