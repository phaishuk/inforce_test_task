from rest_framework import serializers
from restaurant.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("name", "representative", "info")


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = (
            "name",
            "restaurant",
            "first_course",
            "main_course",
            "drink",
            "dessert",
            "description",
            "lunch_date",
            "votes",
            "vote_status",
            "is_winner",
        )

        read_only_fields = (
            "votes",
            "vote_status",
            "is_winner",
        )
