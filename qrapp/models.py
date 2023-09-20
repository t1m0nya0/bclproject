from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True)
    student_id = models.CharField(max_length=20)
    university = models.CharField(max_length=100)
    purchase_status = models.BooleanField(default=False)
    num_of_visits = models.IntegerField(default=0)
    dorm_stud = models.BooleanField(default=False)
    bcl_admin = models.ForeignKey(User, on_delete=models.CASCADE)
