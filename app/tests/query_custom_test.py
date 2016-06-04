# -*- coding: utf-8 -*-

# @date 2016/06/3
# @author fengyao.me
# @desc test for flask sqlalchemy custom query
# @record
#

import unittest
from flask.ext.fixtures import FixturesMixin

from app.database import MyBaseQuery
from app.models import User
from app.tests.test_config import app, db
from app import create_app


class QueryCustomTestCase(unittest.TestCase, FixturesMixin):
    @classmethod
    def setUpClass(cls):
        db.create_all()
        cls.app, _ = create_app()
        cls.app.config['FIXTURES_DIRS'] = [cls.app.root_path + '/tests/fixtures']
        FixturesMixin.init_app(app, db)
    fixtures = ['user.json']

    @classmethod
    def tearDownClass(cls):
        # with cls.app.test_request_context():
        db.drop_all()

    def setUp(self):
        # self.app_context = self.app.app_context()
        # self.app_context.push()
        # self.test_app = self.app.test_client()
        self.app.logger.debug("------set up finish------")

    def tearDown(self):
        # self.app_context.pop()
        self.app.logger.debug("------tear down finish------")

    # @unittest.skip('')
    def test_custom_query_all_filter_vwms(self):
        MyBaseQuery.filter_base = 'vwms'
        users = User.query.all()

        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, 'vwms')

    # @unittest.skip('')
    def test_custom_query_first_filter_vwms(self):
        MyBaseQuery.filter_base = 'vwms'
        user = User.query.first()

        self.assertEqual(user.name, 'vwms')

    # @unittest.skip('')
    def test_custom_query_all_not_exist_vwms1(self):
        MyBaseQuery.filter_base = 'vwms1'
        users = User.query.all()

        self.assertEqual(len(users), 0)

    # @unittest.skip('')
    def test_custom_query_first_not_exist_vwms1(self):
        MyBaseQuery.filter_base = 'vwms1'
        user = User.query.first()

        self.assertTrue(user is None)

if __name__ == '__main__':
    unittest.main()
