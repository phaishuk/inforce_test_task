from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
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

        return get_user_model().objects.create_user(**validated_data)

    def validate_status_is_staff(self, value):
        is_staff = self.initial_data.get("is_staff")
        status = self.initial_data.get("status")

        if status == "rest_rep" and is_staff:
            raise ValidationError(
                "A user with status 'rest_rep' cannot have is_staff set to True."
            )

        return value

    def validate(self, data):
        self.validate_status_is_staff(data.get("status"))
        return data
