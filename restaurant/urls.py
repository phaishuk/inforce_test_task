from django.urls import path, include
from rest_framework import routers

from restaurant.views import RestaurantViewSet, MenuViewSet

router = routers.DefaultRouter()
router.register("locations", RestaurantViewSet)
router.register("menus", MenuViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "menus/<int:pk>/vote/", MenuViewSet.as_view({"post": "vote"}), name="menu-vote"
    ),
    path(
        "menus/close_voting/",
        MenuViewSet.as_view({"post": "close_voting"}),
        name="menu-close_voting",
    ),
    path(
        "menus/get_available_menu/",
        MenuViewSet.as_view({"get": "get_available_menu"}),
        name="get_available_menu",
    ),
    path(
        "menus/get_voting_results/",
        MenuViewSet.as_view({"get": "get_voting_results"}),
        name="get_voting_results",
    ),
]

app_name = "restaurant"
