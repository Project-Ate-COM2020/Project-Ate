from rest_framework import serializers
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "reservation_id", 
            "posting_id", 
            "consumer_id",
            "timestamp",
            "claim_code", 
            "status", 
            "no_show_reason",
            "collected_at"
        ]