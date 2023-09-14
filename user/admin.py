from django.contrib import admin
from django.contrib.auth import get_user_model

from restaurant.models import Restaurant

from django.utils.translation import gettext as _


class RestaurantInline(admin.TabularInline):
    model = Restaurant.representative.through
    extra = 1


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "status")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    inlines = [RestaurantInline]  # Додавання Inline моделі

    list_display = ("name", "status", "email", "get_restaurants")
    list_filter = (
        "last_name",
        "first_name",
        "status",
        "restaurant_reps__name",
    )

    def name(self, obj):
        return f"{obj.last_name} {obj.first_name}"

    def get_restaurants(self, obj):
        restaurants = Restaurant.objects.filter(representative=obj)
        return ", ".join([restaurant.name for restaurant in restaurants])

    get_restaurants.short_description = "Restaurants"
