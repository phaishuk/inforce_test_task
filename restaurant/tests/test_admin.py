from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.urls import reverse
from restaurant.admin import RestaurantAdmin, MenuAdmin
from restaurant.models import Restaurant, Menu


class AdminPanelTest(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="adminpassword", email="admin@example.com"
        )
        self.client.login(username="admin", password="adminpassword")

    def test_restaurant_model_in_admin_registered(self):
        self.assertIn(Restaurant, admin.site._registry)

    def test_menu_model_in_admin_registered(self):
        self.assertIn(Menu, admin.site._registry)

    def test_restaurant_admin(self):
        restaurant_admin = RestaurantAdmin(model=Restaurant, admin_site=self.site)
        self.assertEqual(restaurant_admin.list_display, ("name", "info"))
        self.assertEqual(
            restaurant_admin.list_filter, ("name", "representative", "info")
        )
        self.assertEqual(
            restaurant_admin.search_fields, ("name", "representative", "info")
        )

        url = reverse("admin:restaurant_restaurant_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_menu_admin(self):
        menu_admin = MenuAdmin(model=Menu, admin_site=self.site)
        self.assertEqual(
            menu_admin.list_display,
            (
                "name",
                "restaurant",
                "first_course",
                "main_course",
                "drink",
                "dessert",
            ),
        )
        self.assertEqual(
            menu_admin.list_filter, ("name", "restaurant", "lunch_date", "is_winner")
        )
        self.assertEqual(
            menu_admin.search_fields,
            (
                "name",
                "restaurant",
                "lunch_date",
                "first_course",
                "main_course",
                "drink",
                "dessert",
                "lunch_date",
                "vote_status",
                "is_winner",
            ),
        )

        url = reverse("admin:restaurant_menu_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
