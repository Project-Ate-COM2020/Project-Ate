from rest_framework import serializers
from argon2 import PasswordHasher
from .models import Seller, Bundle, Consumer, Reservation, BundlePosting

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

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ("id", "posting", "consumer", "claim_code", "status")

class BundlePostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundlePosting
        fields = (
            "posting_id",
            "category",
            "contents", 
            "allergens",
            "quantity",
            "price",
            "pickup_window",
            "status",
            "created_at",
            "updated_at",
            "seller_id",
        )
