from django.test import TestCase
from django.contrib.auth import get_user_model
from restaurant.models import Restaurant
from user.serializers import UserSerializer


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "testuser",
            "password": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "status": "rest_rep",
            "restaurant_id": [],
        }

        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            info="This is a test restaurant.",
        )

    def test_create_user_with_existing_name(self):
        existing_user = get_user_model().objects.create_user(
            username="existinguser",
            password="existingpassword",
            first_name="Test",
            last_name="User",
            email="existing@example.com",
            status="rest_rep",
        )

        self.user_data["username"] = "existinguser"
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_user_with_rest_rep_status_and_is_staff_true(self):
        self.user_data["status"] = "rest_rep"
        self.user_data["is_staff"] = True
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_user_with_rest_rep_status_and_no_restaurant_id(self):
        self.user_data["status"] = "rest_rep"
        self.user_data["restaurant_id"] = []
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())

    def test_user_with_employee_status_and_restaurant_id(self):
        self.user_data["status"] = "employee"
        self.user_data["restaurant_id"] = [self.restaurant.id]
        serializer = UserSerializer(data=self.user_data)
        self.assertFalse(serializer.is_valid())
