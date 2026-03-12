from .models import (
    BundlePosting,
    Reservation,
    Consumer,
    Seller,
    BadgeMapping,
    Badges,
    IssueReport,
    ForecastInput,
    ForecastOutput,
    Maintainer,
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


class MaintainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintainer
        fields = ["name", "email"]


class MaintainerWithPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintainer
        fields = ["maintainer_id", "name", "email", "password"]


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


class ForecastInputSerializer(serializers.ModelSerializer):
    seller_name = serializers.CharField(
        source="seller.name", read_only=True, allow_null=True
    )

    class Meta:
        model = ForecastInput
        fields = [
            "record_id",
            "day_of_week",
            "time_window",
            "seller",
            "seller_name",
            "category",
            "price",
            "weather_flag",
            "observed_reservations",
            "observed_no_show",
            "unreserved_stock",
        ]


class ForecastOutputSerializer(serializers.ModelSerializer):
    posting_details = serializers.SerializerMethodField()

    class Meta:
        model = ForecastOutput
        fields = [
            "output_id",
            "posting",
            "posting_details",
            "predicted_reservations",
            "predicted_no_show_prob",
            "confidence",
            "rationale",
            "created_at",
        ]

    def get_posting_details(self, obj):
        if obj.posting:
            return {
                "posting_id": obj.posting.posting_id,
                "category": obj.posting.category,
                "seller_name": obj.posting.seller.name if obj.posting.seller else None,
            }
        return None
