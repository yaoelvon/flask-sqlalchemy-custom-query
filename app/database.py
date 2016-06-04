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


class MyBaseQuery(BaseQuery):
    # do stuff here

    def all(self):
        tenant_ctx = None if not request else request.environ['tenant_ctx']
        if tenant_ctx is None or hasattr(tenant_ctx, 'db_filters')is False:
            self = self
        else:
            for k, v in tenant_ctx.db_filters.items():
                self = self.filter_by(**{k: v})

        return list(self)

    def first(self):
        """改写basequery的first方法. 增加过滤条件
        """
        tenant_ctx = None if not request else request.environ['tenant_ctx']
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


class MyModel(Model):
    # in this case we're just using a custom BaseQuery class,
    # but you can add other stuff as well
    query_class = MyBaseQuery


class MySQLAlchemy(BaseSQLAlchemy):
    def make_declarative_base(self, metadata=None):
        # in this case we're just using a custom Model class,
        # but you can change the DelcarativeMeta or other stuff as well
        base = declarative_base(cls=MyModel,
                                name='Model',
                                metadata=metadata,
                                metaclass=_BoundDeclarativeMeta)
        base.query = _QueryProperty(self)
        return base

# To handle Flask-Fixtures's Bug: https://github.com/croach/Flask-Fixtures/issues/22
TEST = True
if TEST is True:
    from app.tests.test_config import db
else:
    db = MySQLAlchemy()
