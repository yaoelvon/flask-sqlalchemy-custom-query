# -*- coding: utf-8 -*-

# @date 2016/06/3
# @author yaoelvon@gmail.com
# @desc test for flask sqlalchemy custom query
# @record
#

import json
import unittest
from flask.ext.fixtures import FixturesMixin

from app.models import User, Role
from app import create_app


class QueryCustomTestCase(unittest.TestCase, FixturesMixin):
    @classmethod
    def setUpClass(cls):
        cls.app, cls.db = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.db.create_all()
        cls.app.config['FIXTURES_DIRS'] = [cls.app.root_path + '/tests/fixtures']
#        FixturesMixin.init_app(cls.app, cls.db)
    fixtures = ['user.json']

    @classmethod
    def tearDownClass(cls):
        cls.db.drop_all()
        cls.app_context.pop()

    def setUp(self):
        self.test_app = self.app.test_client()
        self.app.logger.debug("------set up finish------")

    def tearDown(self):
        self.app.logger.debug("------tear down finish------")

    # @unittest.skip('')
    def test_custom_query_first(self):
        user = User.query.first()
        self.assertEqual(user.name, 'vwms' or 'fengyao')

    # @unittest.skip('')
    def test_custom_query_all(self):
        users = User.query.all()

        self.assertEqual(len(users), 2)

    # 当请求条件为：name=vwms,只获取name为vwms的数据
    # @unittest.skip('')
    def test_request_args_normal_name(self):
        response = self.test_app.get(
            '/api/users?db_filters={"name":"vwms"}',
            content_type='application/json;charset=utf-8')

        resp = json.loads(response.data)
        self.assertEqual(resp['user'], '1')

    # 当请求参数为空时，过滤条件为空，获取到所有用户信息
    # @unittest.skip('')
    def test_request_args_null(self):
        response = self.test_app.get(
            '/api/users',
            content_type='application/json;charset=utf-8')

        resp = json.loads(response.data)
        self.assertEqual(resp['user'], '2')

    # 当请求条件为：name=vwms1, 获取用户数量为0
    # @unittest.skip('')
    def test_request_args_not_exist_name(self):
        response = self.test_app.get(
            '/api/users?db_filters={"name":"vwms1"}',
            content_type='application/json;charset=utf-8')

        resp = json.loads(response.data)
        self.assertEqual(resp['user'], '0')

    # @unittest.skip('')
    def test_custom_query_role_all(self):
        roles = Role.query.all()

        self.assertEqual(len(roles), 2)

    # @unittest.skip('')
    def test_creating_user_and_adding_company_id(self):
        response = self.test_app.post('/api/users?db_filters={"company_id": 2}',
                                      content_type='application/json;charset=utf-8',
                                      data={"name": "li"})

        print response.data

        user = json.loads(response.data)
        self.assertTrue("200" in response.status)
        self.assertEqual(user['result'], 2)


if __name__ == '__main__':
    unittest.main()
