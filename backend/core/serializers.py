from .models import (
    Allergen,
    BundleAllergens,
    BundlePosting,
    Reservation,
    Consumer,
    Seller,
    BadgeMapping,
    Badges,
    IssueReport,
    ForecastInput,
    ForecastOutput,
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


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ["allergen_id", "name"]


class BundlePostingSerializer(serializers.ModelSerializer):
    allergens = serializers.SerializerMethodField()

    class Meta:
        model = BundlePosting
        fields = "__all__"

    def get_allergens(self, obj):
        return list(
            BundleAllergens.objects.filter(bundle_id=obj)
            .select_related("allergen_id")
            .values_list("allergen_id__name", flat=True)
        )


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
