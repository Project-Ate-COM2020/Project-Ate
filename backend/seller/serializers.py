from rest_framework import serializers
from .models import Seller

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
