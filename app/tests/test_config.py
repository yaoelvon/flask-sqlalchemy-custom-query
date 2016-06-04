# -*- coding: utf-8 -*-

# @date 2016/06/04
# @author fengyao.me
# @desc This file used for dealling with Flask-Fixtures's Bug:
#       https://github.com/croach/Flask-Fixtures/issues/22
# @record
#

from flask import Flask
# from flask.ext.sqlalchemy import SQLAlchemy
from app.database import MySQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess'
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbTest.db'

db = MySQLAlchemy(app)
