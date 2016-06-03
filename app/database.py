# -*- coding: utf-8 -*-

# @date 2016/06/03
# @author fengyao.me
# @desc custom methods of the query class in Flask-SQLAlchemy
# @record
#


from flask_sqlalchemy import BaseQuery, Model, _BoundDeclarativeMeta, SQLAlchemy as BaseSQLAlchemy, _QueryProperty
from sqlalchemy.ext.declarative import declarative_base


class MyBaseQuery(BaseQuery):
    # do stuff here
    filter_name = ""

    def all(self):
        return list(self.filter_by(name=self.filter_name))

    def first(self):
        """改写basequery的first方法. 增加过滤条件
        """
        if self._statement is not None:
            ret = list(self.filter_by(name=self.filter_name))[0:1]
        else:
            ret = list(self.filter_by(name=self.filter_name)[0:1])
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