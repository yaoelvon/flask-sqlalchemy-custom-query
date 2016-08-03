# -*- coding: utf-8 -*-

# @date 2016/06/03
# @author fengyao.me
# @desc custom methods of the query class in Flask-SQLAlchemy
# @record
#

from flask import request
from flask_sqlalchemy import (
    BaseQuery,
    Model,
    _BoundDeclarativeMeta,
    SQLAlchemy as BaseSQLAlchemy,
    _QueryProperty)
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy._compat import iteritems, itervalues, xrange, \
     string_types

class MyBaseQuery(BaseQuery):
    # do stuff here

    def all(self):
        tenant_ctx = None if not request else request.environ.get('tenant_ctx')
        if tenant_ctx is None or hasattr(tenant_ctx, 'db_filters')is False:
            self = self
        else:
            for k, v in tenant_ctx.db_filters.items():
                self = self.filter_by(**{k: v})

        return list(self)

    def first(self):
        """改写basequery的first方法. 增加过滤条件
        """
        tenant_ctx = None if not request else request.environ.get('tenant_ctx')
        if tenant_ctx is None or hasattr(tenant_ctx, 'db_filters')is False:
            self = self
        else:
            for k, v in tenant_ctx.db_filters.items():
                self = self.filter_by(**{k: v})

        if self._statement is not None:
            ret = list(self)[0:1]
        else:
            ret = list(self[0:1])
        if len(ret) > 0:
            return ret[0]
        else:
            return None


class MyBaseQuery2(BaseQuery):
    # do stuff here

    def all(self):
        return list(self)

    def first(self):
        if self._statement is not None:
            ret = list(self)[0:1]
        else:
            ret = list(self[0:1])
        if len(ret) > 0:
            return ret[0]
        else:
            return None


class MyModel(Model):
    # in this case we're just using a custom BaseQuery class,
    # but you can add other stuff as well
    query_class = MyBaseQuery


class MyModel2(Model):
    # in this case we're just using a custom BaseQuery class,
    # but you can add other stuff as well
    query_class = MyBaseQuery2


class MySQLAlchemy(BaseSQLAlchemy):
    def __init__(self):
        super(MySQLAlchemy, self).__init__(metadata=None)
        self.Model2 = self.make_declarative_base2()

    def make_declarative_base(self, metadata=None):
        # in this case we're just using a custom Model class,
        # but you can change the DelcarativeMeta or other stuff as well
        base = declarative_base(cls=MyModel,
                                name='Model',
                                metadata=metadata,
                                metaclass=_BoundDeclarativeMeta)
        base.query = _QueryProperty(self)
        return base

    def make_declarative_base2(self, metadata=None):
        # in this case we're just using a custom Model class,
        # but you can change the DelcarativeMeta or other stuff as well
        base = declarative_base(cls=MyModel2,
                                name='Model',
                                metadata=metadata,
                                metaclass=_BoundDeclarativeMeta)
        base.query = _QueryProperty(self)
        return base

    def get_tables_for_bind(self, bind=None):
        """Returns a list of all tables relevant for a bind."""
        result = []
        for table in itervalues(self.Model.metadata.tables):
            if table.info.get('bind_key') == bind:
                result.append(table)

        for table in itervalues(self.Model2.metadata.tables):
            if table.info.get('bind_key') == bind:
                result.append(table)
        return result


# Fixed Flask-Fixtures's Bug: https://github.com/croach/Flask-Fixtures/issues/22
db = MySQLAlchemy()
