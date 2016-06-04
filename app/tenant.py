# -*- coding: utf-8 -*-

# @date 2016/06/4
# @author fengyao.me
# @desc tenant class
# @record
#

import json

class TenantContext(object):
    """租户对象"""
    def __init__(self, db_filters):

        self.db_filters = {} if db_filters is None else json.loads(db_filters)
