# -*- coding: utf-8 -*-

# @date 2016/06/02
# @author fengyao.me
# @desc custom methods of the query class in Flask-SQLAlchemy
# @record
#

from flask import Flask
from app.database import db
from app.user_api import user


def create_app():
    app = Flask(__name__)
    db.init_app(app)

    app.register_blueprint(user, url_prefix="/api")

    return app, db
