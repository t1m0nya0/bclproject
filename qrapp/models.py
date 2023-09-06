from django.contrib.auth.models import User
from django.db import models


class Ticket(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12, unique=True)
    student_id = models.CharField(max_length=20, null=True, blank=True)
    university = models.CharField(max_length=100, blank=True)
    purchase_status = models.BooleanField(default=False)
    mail = models.EmailField()
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True, editable=False)
    num_of_visits = models.IntegerField(default=0, editable=False)
    dorm_stud = models.BooleanField(default=False)

