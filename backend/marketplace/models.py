from django.db import models

from rest_framework import serializers


class Seller(models.Model):
    name = models.CharField(max_length=20)
    # just do post code for now
    location = models.CharField(max_length=6)
    opening_hours = models.CharField(max_length=20)
    contact_stub = models.CharField(max_length=20)


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["name", "location", "opening_hours", "contact_stub"]


class Bundle(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.CharField(max_length=20)
    contents = models.TextField()
    allergens = models.TextField()
    quantity = models.IntegerField()
    price = models.FloatField()
    pickup_window = models.CharField(max_length=20)
    status = models.IntegerField()


class BundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bundle
        fields = [
            "seller",
            "category",
            "contents",
            "allergens",
            "quantity",
            "price",
            "pickup_window",
        ]


class Consumer(models.Model):
    display_name = models.CharField(max_length=20)
    streak = models.IntegerField()
    badges = models.TextField()


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["display_name", "streak", "badges"]
