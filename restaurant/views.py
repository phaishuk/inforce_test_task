import datetime

from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from restaurant.models import Restaurant, Menu
from restaurant.serializers import (
    RestaurantSerializer,
    MenuSerializer,
    ResultsSerializer,
)


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticated,)


class MenuViewSet(ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = (IsAuthenticated,)

    @action(detail=True, methods=["POST"])
    def vote(self, request, pk=None):
        menu = self.get_object()

        if request.user.status != "employee":
            return Response({"message": "Only employees can vote."})

        if menu.lunch_date != datetime.date.today():
            return Response({"message": "You can't vote for menus from other dates."})

        if menu.vote_status == "closed":
            winner_menu = Menu.objects.filter(
                lunch_date=datetime.date.today(), is_winner=True
            ).first()
            if winner_menu:
                return Response(
                    {
                        "message": f"Voting is closed."
                        f"Today we are eating {winner_menu.name}"
                        f" in {winner_menu.restaurant.name}."
                    },
                    status=400,
                )

        if request.user in menu.votes.all():
            menu.votes.remove(request.user)
            return Response({"message": "You have successfully removed your vote."})

        menu.votes.add(request.user)
        return Response({"message": "You have voted successfully!"})

    @action(detail=False, methods=["POST"])
    def close_voting(self, request):
        today_menus = Menu.objects.filter(lunch_date=datetime.date.today())

        if not request.user.is_staff:
            return Response({"message": "Only staff employee can close the voting"})

        for menu in today_menus:
            menu.vote_status = "closed"
            menu.save()

        winner_menu = (
            today_menus.annotate(num_votes=Count("vote")).order_by("-num_votes").first()
        )
        if winner_menu:
            winner_menu.is_winner = True
            winner_menu.save()

        return Response(
            {
                "message": f"Voting for today's menu "
                f"is closed. Today we eating {winner_menu.name} in "
                f"{winner_menu.restaurant.name}"
            }
        )

    @action(detail=False, methods=["GET"])
    def get_available_menu(self, request):
        today = datetime.date.today()
        winner_menu = Menu.objects.filter(is_winner=True, lunch_date=today).first()

        if winner_menu:
            return Response(
                {
                    "message": f"Voting is closed."
                    f"Today we are eating {winner_menu.name}"
                    f" in {winner_menu.restaurant.name}."
                }
            )
        else:
            today_menus = Menu.objects.filter(lunch_date=today, vote_status="opened")
            serializer = self.get_serializer(today_menus, many=True)

            return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def get_voting_results(self, request):
        requested_date = request.query_params.get("date", None)

        if requested_date:
            try:
                date_obj = datetime.datetime.strptime(requested_date, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"message": "Invalid date format. Please use YYYY-MM-DD."},
                    status=400,
                )
        else:
            date_obj = datetime.date.today()

        queryset = Menu.objects.filter(lunch_date=date_obj)
        serializer = ResultsSerializer(queryset, many=True)

        return Response(serializer.data)
