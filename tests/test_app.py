
# tests/test_app.y
import unittest
import os

os.environ[ 'TESTING'] = 'true'

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    # testing the home page
    def test_home(self):
        response = self.client.get("/")
        #assert response.status_code == 200
        #html = response.get_data(as_text=True)
        #assert "«title>Alexis Vielma;</title>" in html
        # TODO Add more tests relating to the home page


        # respose = self.client.get()
