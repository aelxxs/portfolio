
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
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>Alexis Vielma</title>" in html
        # TODO Add more tests relating to the home page


        # respose = self.client.get()
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline" in json
        assert len(json["timeline"]) == 0

        # TODO add more tests relating to the /api/timeline_post get and post apis

        respo = self.client.post("/api/timeline_post", data={
            "name": "angel", "email":   "angeldzambrano99@gmail.com", "content": "angel was here!"
        })

        assert respo.status_code == 200

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data=
        { "email":"john@example.com", "content":"Hello world, I'm John!" })

        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post("/api/timeline_post", data=
        { "name":"John Doe", "email":"john@example.com", "content":"" })

        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data=
        {"name":"John Doe", "email":"not-an-email", "content":"Hello world, I'm John!" })

        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
