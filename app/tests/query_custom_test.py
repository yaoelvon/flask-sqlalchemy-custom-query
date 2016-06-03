# -*- coding: utf-8 -*-

# @date 2016/06/3
# @author fengyao.me
# @desc test for flask sqlalchemy custom query
# @record
#

import unittest

from flask.ext.fixtures import FixturesMixin
from app import create_app
from app.database import MyBaseQuery, db
from app.models import User


class QueryCustomTestCase(unittest.TestCase, FixturesMixin):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        with cls.app.test_request_context():
            db.create_all()
    #         cls.app.config['FIXTURES_DIRS'] = ['./fixtures']
    #         FixturesMixin.init_app(cls.app, db)
    # fixtures = ['user.json']

    @classmethod
    def tearDownClass(cls):
        with cls.app.test_request_context():
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
    def test_custom_query(self):
        with self.app.test_request_context():
            user1 = User()
            user2 = User()
            user1.name = 'vwms'
            user2.name = 'fengyao'
            db.session.add(user1)
            db.session.add(user2)
            db.session.commit()

            MyBaseQuery.filter_name = 'vwms'
            users = User.query.all()
            self.assertEqual(users[0].name, 'vwms')

            MyBaseQuery.filter_name = 'vwms1'
            user_first = User.query.first()
            self.assertTrue(user_first is None)

if __name__ == '__main__':
    unittest.main()
