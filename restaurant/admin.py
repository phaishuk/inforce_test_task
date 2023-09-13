from django.contrib import admin
from restaurant.models import Restaurant, Menu


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "info")
    list_filter = ("name", "representative", "info")
    search_fields = ("name", "representative", "info")


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "restaurant",
        "first_course",
        "main_course",
        "drink",
        "dessert",
    )
    list_filter = ("name", "restaurant", "lunch_date", "is_winner")
    search_fields = (
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
    )
