from rest_framework import serializers
from .models import BundlePosting # type: ignore

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