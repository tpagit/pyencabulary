import unittest
from flask import json

from server import create_app
from server.database import db
from server.database.management import db_manager
from server.database.model import DbUser
from server.globals import get_root_dir


class BaseTestCase(unittest.TestCase):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{path}/{db_name}'.format(path=get_root_dir(), db_name='test.dictionary.db')

    def create_test_app(self):

        app = create_app({'SQLALCHEMY_DATABASE_URI': self.SQLALCHEMY_DATABASE_URI})

        return app

    def setUp(self):
        application = self.create_test_app()
        self.app = application.test_client()

        with application.app_context():
            db_manager.delete_db()
            db_manager.create_db()
            db_manager.init_db_with_default_values()

            test_user = DbUser('test-user@domain.com', 1, '123')
            db.session.add(test_user)
            db_manager.save_db_changes()

            db.session.remove()

    def tearDown(self):
        pass

    def get_json_response(self, url, params=None, headers=None, method=None):
        if method is None or method.lower() == "post":
            raw_response = self.app.post(url, data=json.dumps(params), headers=headers,
                                         content_type='application/json').data
        else:
            raw_response = self.app.get(url, data=params, headers=headers).data

        try:
            return json.loads(raw_response)
        except Exception as ex:
            print(raw_response)
            return None

    def get_json_multipart_response(self, url, params=None, headers=None):
        raw_response = self.app.post(url, content_type='multipart/form-data', data=params, headers=headers).data

        return json.loads(raw_response)

    def get_login_response(self):
        return self.get_json_response(
            '/api/login',
            dict(
                email="test-user@domain.com",
                password="123"
            )
        )

    def print_json(self, json_dict, message=None):
        print("{}\n{}\n---------------\n".format(message, json.dumps(json_dict, indent=3, sort_keys=True, ensure_ascii=False)))
