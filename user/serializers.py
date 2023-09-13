from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from restaurant.models import Restaurant


class UserSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.ListField(required=False)

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "status",
            "is_staff",
            "restaurant_id",
        )

        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")

        existing_users = get_user_model().objects.filter(
            first_name=first_name, last_name=last_name
        )

        if existing_users.exists():
            raise ValidationError(
                "A user with this first and last name already exists."
            )

        id_restaurant_list = validated_data.pop("restaurant_id", [])

        user = get_user_model().objects.create_user(**validated_data)

        for restaurant_id in id_restaurant_list:
            try:
                restaurant = Restaurant.objects.get(id=restaurant_id)
                user.restaurant_reps.add(restaurant)
            except Restaurant.DoesNotExist:
                raise ValidationError(
                    f"Restaurant with id {restaurant_id} does not exist. "
                    f"Please provide a valid restaurant_id."
                )

        return user

    def update(self, instance, validated_data):
        restaurant_id_list = validated_data.pop("restaurant_id", [])

        instance.restaurant_reps.clear()

        for restaurant_id in restaurant_id_list:
            try:
                restaurant = Restaurant.objects.get(id=restaurant_id)
                instance.restaurant_reps.add(restaurant)
            except Restaurant.DoesNotExist:
                raise ValidationError(
                    f"Restaurant with id {restaurant_id} does not exist. "
                    f"Please provide a valid restaurant_id."
                )

        return super().update(instance, validated_data)

    def validate(self, data):
        instance = self.instance
        status = data.get("status") if not instance else instance.status
        restaurant_id = (
            data.get("restaurant_id")
            if not instance
            else instance.restaurant_reps.values_list("id", flat=True)
        )
        is_staff = data.get("is_staff") if not instance else instance.is_staff

        if status == "rest_rep" and is_staff:
            raise ValidationError(
                "A user with status 'rest_rep' cannot have is_staff set to True."
            )

        if status == "rest_rep" and not restaurant_id:
            raise ValidationError(
                "Restaurant representative have to indicate restaurant_id "
                "during profile creation or restaurant update"
            )

        if status == "employee" and restaurant_id:
            raise ValidationError(
                "Company employees cannot be a restaurant representatives"
            )

        return data
