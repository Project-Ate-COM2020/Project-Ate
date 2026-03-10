from backend.core.models import (
    BundlePosting,
    Reservation,
    Consumer,
    Seller,
    BadgeMapping,
    Badges,
)

from rest_framework import serializers


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badges
        fields = "__all__"


class BadgeMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeMapping
        fields = "__all__"


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["name", "location", "opening_hours", "contact_stub"]


class SellerWithPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            "seller_id",
            "name",
            "password",
            "location",
            "opening_hours",
            "contact_stub",
        ]
