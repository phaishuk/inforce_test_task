from django.test import TestCase
from user.models import User


class UserModelTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "first_name": "John",
            "last_name": "Doe",
            "status": "rest_rep",
        }

    def test_create_user(self):
        User.objects.create(**self.user_data)
        self.assertEqual(User.objects.count(), 1)

    def test_user_str(self):
        user = User.objects.create(**self.user_data)
        expected_str = f"{user.last_name} {user.first_name}"
        self.assertEqual(str(user), expected_str)
