# -*- coding: utf-8 -*-

# @date 2016/06/02
# @author fengyao.me
# @desc custom methods of the query class in Flask-SQLAlchemy
# @record
#

from flask import Flask
from app.database import db

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app, db
