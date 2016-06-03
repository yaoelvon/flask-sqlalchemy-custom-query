# -*- coding: utf-8 -*-

# @date 2016/06/02
# @author fengyao.me
# @desc override the query class in Flask-SQLAlchemy
# @record
#

from flask import Flask
from flask_sqlalchemy import BaseQuery, Model, _BoundDeclarativeMeta, SQLAlchemy as BaseSQLAlchemy, _QueryProperty
from sqlalchemy.ext.declarative import declarative_base


class MyBaseQuery(BaseQuery):
    # do stuff here

    # def __init__(self, *args, **kwargs):
        # super(MyBaseQuery, self).__init__(*args, **kwargs)
        # print "1   3hehe"
        # print self
        # self = self.filter_by(name='vwms').first()
        # self = self.filter_by(name="vwms")
        # print self.filter_by(name="vwms")
        # self = self.first()
        # print self.__class__
        # print self.__dict__
        # print self
        # print "haha"

    def all(self):
        return list(self.filter_by(name="vwms"))

    def first(self):
        """改写basequery的first方法. 增加过滤条件
        """
        if self._statement is not None:
            ret = list(self.filter_by(name="vwms1"))[0:1]
        else:
            ret = list(self.filter_by(name="vwms1")[0:1])
        if len(ret) > 0:
            return ret[0]
        else:
            return None


class MyModel(Model):
    # in this case we're just using a custom BaseQuery class, but you can add other stuff as well
    query_class = MyBaseQuery


class SQLAlchemy(BaseSQLAlchemy):
    def make_declarative_base(self, metadata=None):
        # in this case we're just using a custom Model class, but you can change the DelcarativeMeta or other stuff as well
        base = declarative_base(cls=MyModel,
                                name='Model',
                                metadata=metadata,
                                metaclass=_BoundDeclarativeMeta)
        base.query = _QueryProperty(self)
        return base

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

app = Flask(__name__)
db.init_app(app)

if __name__ == "__main__":
    with app.test_request_context():
        db.drop_all()
        db.create_all()

        user1 = User()
        user2 = User()
        user1.name = 'vwms'
        user2.name = 'fengyao'
        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()
        # print user1
        # print User.query.filter_by(name='vwms')
        users = User.query.all()
        for i in range(len(users)):
            print users[i].name

        user_first = User.query.first()
        # print user_first
        if user_first is None:
            print "user first is None"
        else:
            print user_first.name

    app.run(port=8765, debug=True)
