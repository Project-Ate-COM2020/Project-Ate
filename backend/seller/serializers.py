from rest_framework import serializers
from .models import Seller, Reservation
from backend.core.models import Consumer

class SellerSerializer(serializers.ModelSerializer):
    seller = serializers.CharField(source="name")

    class Meta:
        model = Seller
        fields = [
            "seller_id",
            "seller",
            "location",
            "opening_hours",
            "contact_stub",
        ]

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "reservation_id",
            "posting",
            "consumer",
            "timestamp",
            "claim_code",
            "status",
            "no_show_reason",
            "collected_at",
        ]
        read_only_fields = ["reservation_id", "timestamp"]

class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = [
            "consumer_id",
            "display_name",
            "streak",
            "badges",
        ]
        read_only_fields = ["consumer_id"]