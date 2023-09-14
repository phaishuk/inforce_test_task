from django.contrib.auth import get_user_model
from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    representative = models.ManyToManyField(
        to=get_user_model(), related_name="restaurant_reps", blank=True
    )
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    class VoteChoices(models.TextChoices):
        OPENED = "opened"
        CLOSED = "closed"

    name = models.CharField(max_length=255)
    restaurant = models.ForeignKey(
        to=Restaurant, on_delete=models.CASCADE, related_name="restaurants"
    )
    first_course = models.CharField(max_length=255, blank=True, null=True)
    main_course = models.CharField(max_length=255)
    drink = models.CharField(max_length=255, blank=True, null=True)
    dessert = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    lunch_date = models.DateField()
    votes = models.ManyToManyField(
        to=get_user_model(), through="Vote", related_name="liked_posts"
    )
    vote_status = models.CharField(
        max_length=255, choices=VoteChoices.choices, default="opened"
    )
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Vote(models.Model):
    employee = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    menu = models.ForeignKey(to=Menu, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
