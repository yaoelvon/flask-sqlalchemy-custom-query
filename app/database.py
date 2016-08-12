# -*- coding: utf-8 -*-

# @date 2016/06/03
# @author feng yao
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


class MyModel(Model):
    # in this case we're just using a custom BaseQuery class,
    # but you can add other stuff as well
    query_class = MyBaseQuery


def _my_declarative_constructor(self, tenant=None, **kwargs):
    """A simple constructor that allows initialization from kwargs.

    Sets attributes on the constructed instance using the names and
    values in ``kwargs``.

    Only keys that are present as
    attributes of the instance's class are allowed. These could be,
    for example, any mapped columns or relationships.
    """

    if tenant is not None:
        setattr(self, "company_id", tenant.db_filters.get('company_id'))

    cls_ = type(self)
    for k in kwargs:
        if not hasattr(cls_, k):
            raise TypeError(
                "%r is an invalid keyword argument for %s" %
                (k, cls_.__name__))
        setattr(self, k, kwargs[k])


class MySQLAlchemy(BaseSQLAlchemy):
    def make_declarative_base(self, metadata=None):
        # in this case we're just using a custom Model class,
        # but you can change the DelcarativeMeta or other stuff as well
        base = declarative_base(cls=MyModel,
                                name='Model',
                                metadata=metadata,
                                metaclass=_BoundDeclarativeMeta,
                                constructor=_my_declarative_constructor)
        base.query = _QueryProperty(self)
        return base


# Fixed Flask-Fixtures's Bug: https://github.com/croach/Flask-Fixtures/issues/22
db = MySQLAlchemy()
