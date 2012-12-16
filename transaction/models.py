from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    user = models.ForeignKey(User)
    value = models.IntegerField()
    date = models.DateTimeField()
    details = models.CharField(max_length=256)
