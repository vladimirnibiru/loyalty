from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save


class Account(models.Model):
    user = models.OneToOneField(User)
    points = models.IntegerField(default=0)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
