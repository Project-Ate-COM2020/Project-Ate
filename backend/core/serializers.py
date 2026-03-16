from django.contrib.auth.hashers import make_password
from rest_framework.status import HTTP_404_NOT_FOUND

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
    Maintainer,
)

from argon2 import PasswordHasher

from rest_framework import serializers
from django.conf import settings
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        password = self.validated_data["password"]
        groups = validated_data.pop("groups", [])
        user_permissions = validated_data.pop("user_permissions", [])

        user = self.Meta.model(**validated_data)

        user.set_password(password)

        user.is_active = True

        user.save()

        if groups:
            user.groups.set(groups)

        if user_permissions:
            user.user_permissions.set(user_permissions)

        return user


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
        fields = ["maintainer_id"]


class RegisterMaintainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintainer
        fields = "maintainer_id"

    def create(self, validated_data):
        # we have context provided by generic framework
        context = self.context

        request = context['request']

        user = request.user

        seller = Seller.objects.create(user=user, **validated_data)

        return seller


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ["name", "location", "opening_hours", "contact_stub"]


class RegisterSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = [
            "seller_id",
            "name",
            "location",
            "opening_hours",
            "contact_stub",
        ]

    def create(self, validated_data):
        context = self.context

        request = context['request']

        user = request.user

        seller = Seller.objects.create(user=user, **validated_data)

        return seller


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["display_name", "streak"]


class RegisterConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumer
        fields = ["consumer_id", "display_name", "streak"]

    def create(self, validated_data):
        request = self.context['request']

        user = request.user

        consumer = Consumer.objects.create(user=user, **validated_data)

        return consumer


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
