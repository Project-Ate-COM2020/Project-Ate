from .models import (
    BundlePosting,
    Reservation,
    Consumer,
    Seller,
    BadgeMapping,
    Badges,
    IssueReport,
)

from argon2 import PasswordHasher

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

    def create(self, validated_data):
        ph = PasswordHasher()

        validated_data["password"] = ph.hash(validated_data["password"], salt=None)

        self.Meta.model.is_active = True

        return super().create(validated_data)


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["display_name", "streak"]


class ConsumerWithPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["consumer_id", "display_name", "password", "streak"]

    def create(self, validated_data):
        ph = PasswordHasher()

        validated_data["password"] = ph.hash(validated_data["password"], salt=None)

        self.Meta.model.is_active = True

        return super().create(validated_data)


class BundlePostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundlePosting
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"


class IssueReportingSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueReport
        fields = "__all__"
