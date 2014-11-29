from app import app

import unittest


class AppTestCase(unittest.TestCase):

    def test_root_text(self):
        tester = app.test_client(self)
        response = tester.get("/")
        self.assertTrue("Hello world!" in response.data)
