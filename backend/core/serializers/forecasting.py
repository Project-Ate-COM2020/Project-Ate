from rest_framework import serializers

from core.models import ForecastOutput, ForecastInput


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
