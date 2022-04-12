from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)

    country = models.CharField(null=True, blank=True, max_length=256)
    city = models.CharField(null=True, blank=True, max_length=256)
    address = models.CharField(null=True, blank=True, max_length=256)

    allowed_subscriptions = models.PositiveIntegerField(default=3)
    # subscribed_to_home = models.BooleanField

    class Meta:
        db_table = "user_profiles"


class Subscription(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT)
    country = models.CharField(null=True, blank=True, max_length=256)
    city = models.CharField(null=True, blank=True, max_length=256)
    subscription_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "subscriptions"


# class Sampling