from argon2 import PasswordHasher
from django.db import models

# Create your models here.
from rest_framework import serializers


class Seller(models.Model):
    name = models.CharField(max_length=20, unique=True)
    # just do post code for now
    location = models.CharField(max_length=6)
    # argon2id hashed
    password = models.CharField(max_length=150)
    opening_hours = models.CharField(max_length=20)
    contact_stub = models.CharField(max_length=20)

    def create(self, validated_data):
        ph = PasswordHasher()

        validated_data["password"] = ph.hash(validated_data["password"], salt=None)

        self.Meta.model.is_active = True

        return super().create(validated_data)


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
            "id",
            "seller",
            "category",
            "contents",
            "allergens",
            "quantity",
            "price",
            "pickup_window",
            "status",
        ]


class Consumer(models.Model):
    display_name = models.CharField(max_length=20)
    # argon2id hashed
    password = models.CharField(max_length=150)
    streak = models.IntegerField()
    badges = models.TextField()


class Reservation(models.Model):
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    claim_code = models.CharField(max_length=20)
    status = models.IntegerField()


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "bundle", "consumer", "claim_code", "status"]


class BundlePosting(models.Model):
    # change this if your PK column name is different
    posting_id = models.IntegerField(primary_key=True)

    category = models.CharField(max_length=20)
    contents = models.TextField()
    allergens = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    pickup_window = models.CharField(max_length=20)

    class Meta:
        managed = False  # IMPORTANT: don't migrate
        db_table = "bundle_posting"


class BundlePostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundlePosting
        fields = "__all__"
