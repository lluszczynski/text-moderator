import unittest
import json

from moderator_app.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_home_endpoint(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Welcome to Text Moderator!')

    def test_classify_endpoint(self):
        text_data = {'text': 'This is a test message for classification.'}
        response = self.app.post('/classify', json=text_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn('scores', data)
        self.assertIn('duration_seconds', data)
        self.assertIn('OK', data["scores"])
