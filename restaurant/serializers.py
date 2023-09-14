from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

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

    def validate(self, data):
        user = self.context["request"].user
        user_status = user.status
        if user_status != "rest_rep":
            raise PermissionDenied("Only restaurant representatives can create menus.")
        if (
            user_status == "rest_rep"
            and user not in data["restaurant"].representative.all()
        ):
            raise PermissionDenied(
                "Restaurant representatives can only create "
                "menus for restaurant their responsible on."
            )
        return data

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)


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
