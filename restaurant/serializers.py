from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from restaurant.models import Restaurant, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ("name", "representative", "info")

    def validate(self, data):
        user = self.context["request"].user

        if not user.is_staff:
            raise PermissionDenied("Only admin can create restaurants")

        return data

    def create(self, validated_data):
        return Restaurant.objects.create(**validated_data)


class MenuSerializer(serializers.ModelSerializer):
    votes_count = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = (
            "id",
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

        if user.status != "rest_rep" and not user.is_staff:
            raise PermissionDenied(
                "Only restaurant representatives and admins can create/update menus."
            )
        if (
            user.status == "rest_rep"
            and user not in data["restaurant"].representative.all()
        ):
            raise PermissionDenied(
                "Restaurant representatives can only create "
                "menus for the restaurant they're responsible for."
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
