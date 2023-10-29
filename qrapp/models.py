from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
    name = models.CharField(max_length=255)
    num_of_visits = models.IntegerField(default=0)
