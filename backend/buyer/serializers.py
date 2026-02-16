from rest_framework import serializers
from .models import Seller, Reservation
from backend.core.models import BundlePosting, Consumer

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
        
class BundlePostingSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(
        source="seller.name", read_only=True, allow_null=True
    )

    class Meta:
        model = BundlePosting
        fields = [
            "posting_id",
            "seller",
            "seller_name",
            "category",
            "contents",
            "allergens",
            "quantity",
            "quantity_remaining",
            "price",
            "pickup_window",
            "status",
            "created_at",
            "updated_at",
        ]