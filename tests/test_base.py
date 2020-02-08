import unittest

from dotenv import load_dotenv

from app import create_app


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.load_env()
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def load_env(self):
        load_dotenv('.env_test')


