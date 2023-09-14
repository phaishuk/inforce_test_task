from rest_framework import serializers
from restaurant.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("name", "representative", "info")


class MenuSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

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
            "votes_count",
            "vote_status",
            "is_winner",
        )

        read_only_fields = (
            "votes",
            "vote_status",
            "is_winner",
        )

    def get_votes_count(self, obj):
        return obj.votes.count()


class ResultsSerializer(MenuSerializer):
    class Meta(MenuSerializer.Meta):
        fields = (
            "name",
            "restaurant",
            "votes_count",
            "is_winner",
        )

        read_only_fields = (
            "votes_count",
            "is_winner",
        )
