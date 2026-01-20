from django.db import models


class Seller(models.Model):
    name = models.CharField(max_length=20)
    # just do post code for now
    location = models.CharField(max_length=6)
    opening_hours = models.CharField(max_length=20)
    contact_stub = models.CharField(max_length=20)


class Bundle(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.CharField(max_length=20)
    contents = models.TextField()
    allergens = models.TextField()
    quantity = models.IntegerField()
    price = models.FloatField()
    pickup_window = models.CharField(max_length=20)
    status = models.IntegerField()
