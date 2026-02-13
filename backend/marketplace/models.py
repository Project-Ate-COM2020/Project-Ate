from django.db import models

<<<<<<< HEAD
# Create your models here.
=======
from rest_framework import serializers


class Seller(models.Model):
    name = models.CharField(max_length=20)
    # just do post code for now
    location = models.CharField(max_length=6)
    # argon2id hashed
    password = models.CharField(max_length=150)
    opening_hours = models.CharField(max_length=20)
    contact_stub = models.CharField(max_length=20)


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["name", "location", "opening_hours", "contact_stub"]


class SellerWithPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["name", "password", "location", "opening_hours", "contact_stub"]

    def create(self, validated_data):
        ph = PasswordHasher()

        validated_data["password"] = ph.hash(validated_data["password"])

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
    # argon2id hashed
    password = models.CharField(max_length=150)
    streak = models.IntegerField()
    badges = models.TextField()


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["display_name", "streak", "badges"]


class ConsumerWithPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["display_name", "password", "streak", "badges"]

    def create(self, validated_data):
        ph = PasswordHasher()

        validated_data["password"] = ph.hash(validated_data["password"])

        return super().create(validated_data)


class Reservation(models.Model):
    bundle = models.ForeignKey(Bundle, on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    claim_code = models.CharField(max_length=20)
    status = models.IntegerField()


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["bundle", "consumer", "claim_code", "status"]

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
        managed = False          # IMPORTANT: don't migrate
        db_table = "bundle_posting"
        
class BundlePostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundlePosting
        fields = "__all__"

>>>>>>> f0acf40 (Works_with_no_security)
