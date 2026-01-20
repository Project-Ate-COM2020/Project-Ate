from django.db import models


# Create your models here.
class Seller(models.Model):
    name = models.CharField(max_length=20)
    # just do post code for now
    location = models.CharField(max_length=6)
    opening_hours = models.CharField(max_length=20)
    contact_stub = models.CharField(max_length=20)
