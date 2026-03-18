from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import BundlePosting, BundleAllergens, Seller, Consumer, Reservation


class UpdateSerializer(serializers.ModelSerializer):
    def get_allergens(self, obj):
        return list(
            BundleAllergens.objects.filter(bundle_id=obj)
            .select_related("allergen_id")
            .values_list("allergen_id__name", flat=True)
        )


class ConsumerUpdateSerializer(UpdateSerializer):
    class Meta:
        model = BundlePosting
        fields = "__all__"
        read_only_fields = [
            "seller",
            "created_at",
            "updated_at",
            "price",
            "pickup_window",
            "category",
            "contents",
        ]

    def update(self, instance, validated_data):
        pass


class SellerUpdateSerializer(UpdateSerializer):
    class Meta:
        model = BundlePosting
        fields = "__all__"
        read_only_fields = [
            "seller",
            "created_at",
        ]

    def update(self, instance, validated_data):
        pass


class OldUpdateSerializer(serializers.ModelSerializer):
    allergens = serializers.SerializerMethodField()

    class Meta:
        model = BundlePosting
        fields = "__all__"
        read_only_fields = [
            "seller",
            "created_at",
            "status",
        ]

    def update(self, instance, validated_data):
        context = self.context

        if context is None:
            raise ValidationError(
                {
                    f"no context passed to {self.__class__.__name__}",
                    "please provide context to this serializer",
                }
            )

        request = context["request"]

        if request is None:
            raise ValidationError(
                {
                    f"serializer context key 'request' given to {self.__class__.__name__} is None": "please provide the request as context to this serializer"
                }
            )

        user = request.user

        seller = Seller.objects.filter(user=user)

        consumer = Consumer.objects.filter(user=user)

        if seller is not None:
            # sellers cannot update bundles after a reservation has been made
            reservations = Reservation.objects.filter(posting=instance).exists()

            if reservations:
                raise ValidationError()
        else:
            pass

        if consumer is not None:
            pass
        else:
            pass
