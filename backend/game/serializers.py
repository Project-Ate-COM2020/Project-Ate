from rest_framework import serializers
from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["reservation_id", "posting_id", "status", "collected_at"]