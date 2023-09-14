import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from restaurant.models import Restaurant, Menu


class RestaurantViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="test53",
            last_name="test95",
        )
        self.admin = get_user_model().objects.create_superuser(
            username="adminuser",
            password="adminpassword",
            first_name="test53",
            last_name="test45",
        )
        self.restaurant_data = {
            "name": "Test Restaurant",
            "info": "This is a test restaurant.",
        }

    def test_create_restaurant_by_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/restaurants/locations/", self.restaurant_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Restaurant.objects.count(), 0)


class MenuViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_rep = get_user_model().objects.create_user(
            username="reptestuser",
            password="testpassword",
            status="rest_rep",
            first_name="test43",
            last_name="test85",
        )
        self.user_emp = get_user_model().objects.create_user(
            username="emptestuser",
            password="testpassword",
            status="employee",
            first_name="test13",
            last_name="test83",
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant", info="This is a test restaurant."
        )
        self.menu_data = {
            "name": "Test Menu",
            "restaurant": self.restaurant.id,
            "main_course": "Test Course",
            "lunch_date": "2023-09-01",
        }

    def test_create_menu_by_restaurant_representative(self):
        self.restaurant.representative.add(self.user_rep)
        self.client.force_authenticate(user=self.user_rep)
        response = self.client.post("/api/restaurants/menus/", self.menu_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 1)

    def test_create_menu_by_employee(self):
        self.client.force_authenticate(user=self.user_emp)
        response = self.client.post("/api/restaurants/menus/", self.menu_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Menu.objects.count(), 0)
