from rest_framework import serializers
from .models import Seller, Reservation
from backend.core.models import Consumer

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