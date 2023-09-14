from django.test import TestCase
from django.contrib.auth import get_user_model
from restaurant.models import Restaurant, Menu, Vote
from datetime import date


class RestaurantModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_create_restaurant(self):
        restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            info="This is a test restaurant.",
        )
        restaurant.representative.add(self.user)

        self.assertEqual(restaurant.name, "Test Restaurant")
        self.assertEqual(restaurant.info, "This is a test restaurant.")
        self.assertEqual(restaurant.representative.count(), 1)
        self.assertEqual(restaurant.representative.first(), self.user)
        self.assertEqual(str(restaurant), "Test Restaurant")


class MenuModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword", status="rest_rep"
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            info="This is a test restaurant.",
        )

    def test_create_menu(self):
        menu = Menu.objects.create(
            name="Test Menu",
            restaurant=self.restaurant,
            main_course="Test Course",
            lunch_date=date.today(),
        )
        menu.votes.add(self.user)

        self.assertEqual(menu.name, "Test Menu")
        self.assertEqual(menu.restaurant, self.restaurant)
        self.assertEqual(menu.main_course, "Test Course")
        self.assertEqual(menu.lunch_date, date.today())
        self.assertEqual(menu.votes.count(), 1)
        self.assertEqual(menu.votes.first(), self.user)
        self.assertEqual(str(menu), "Test Menu")


class VoteModelTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpassword", status="employee"
        )
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            info="This is a test restaurant.",
        )
        self.menu = Menu.objects.create(
            name="Test Menu",
            restaurant=self.restaurant,
            main_course="Test Course",
            lunch_date=date.today(),
        )

    def test_create_vote(self):
        vote = Vote.objects.create(
            employee=self.user,
            menu=self.menu,
        )

        self.assertEqual(vote.employee, self.user)
        self.assertEqual(vote.menu, self.menu)
