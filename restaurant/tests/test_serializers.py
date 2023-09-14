from django.test import TestCase
from django.contrib.auth import get_user_model
from restaurant.models import Restaurant, Menu
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APIRequestFactory
from restaurant.serializers import RestaurantSerializer, MenuSerializer


class RestaurantSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpassword",
            first_name="test1",
            last_name="test2",
        )
        self.admin = get_user_model().objects.create_superuser(
            username="adminuser",
            password="adminpassword",
            first_name="test3",
            last_name="test4",
        )

    def test_create_restaurant_by_admin(self):
        data = {"name": "Test Restaurant", "info": "This is a test restaurant."}
        request = self.factory.post("/api/restaurants/", data, format="json")
        request.user = self.admin

        serializer = RestaurantSerializer(data=data, context={"request": request})

        self.assertTrue(serializer.is_valid())
        serializer.save()
        restaurant = Restaurant.objects.last()
        self.assertEqual(restaurant.name, "Test Restaurant")

    def test_create_restaurant_by_user(self):
        data = {"name": "Test Restaurant", "info": "This is a test restaurant."}
        request = self.factory.post("/api/restaurants/", data, format="json")
        request.user = self.user

        serializer = RestaurantSerializer(data=data, context={"request": request})

        with self.assertRaises(PermissionDenied):
            serializer.is_valid()


class MenuSerializerTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user_rep = get_user_model().objects.create_user(
            username="reptestuser",
            password="testpassword",
            status="rest_rep",
            first_name="test6",
            last_name="test5",
        )
        self.user_emp = get_user_model().objects.create_user(
            username="emptestuser",
            password="testpassword",
            status="employee",
            first_name="test7",
            last_name="test8",
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            info="This is a test restaurant.",
        )

    def test_create_menu_by_restaurant_representative(self):
        self.restaurant.representative.add(self.user_rep)
        data = {
            "name": "Test Menu",
            "restaurant": self.restaurant.id,
            "main_course": "Test Course",
            "lunch_date": "2023-09-01",
        }
        request = self.factory.post("/api/menus/", data, format="json")
        request.user = self.user_rep

        serializer = MenuSerializer(data=data, context={"request": request})

        self.assertTrue(serializer.is_valid())
        serializer.save()
        menu = Menu.objects.last()
        self.assertEqual(menu.name, "Test Menu")

    def test_create_menu_by_employee(self):
        data = {
            "name": "Test Menu",
            "restaurant": self.restaurant.id,
            "main_course": "Test Course",
            "lunch_date": "2023-09-01",
        }
        request = self.factory.post("/api/menus/", data, format="json")
        request.user = self.user_emp

        serializer = MenuSerializer(data=data, context={"request": request})

        with self.assertRaises(PermissionDenied):
            serializer.is_valid()
