import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()

    def test_login_and_profile_access(self):
        response = self.client.post(
            "/users/login",
            data={"username": "user1", "password": "password123"},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user1", response.data)

    def test_unauthorized_profile_redirect(self):
        response = self.client.get("/users/profile", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)


if __name__ == "__main__":
    unittest.main()