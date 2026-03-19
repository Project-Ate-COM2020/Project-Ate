from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Reservation, Consumer, BundlePosting


class CreateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "reservation_id",
            "posting",
            "timestamp",
            "claim_code",
            "status",
            "no_show_reason",
            "collected_at",
        ]

    def create(self, validated_data):
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

        consumer = Consumer.objects.get(user=user)

        posting: BundlePosting = validated_data.get("posting")

        if posting.quantity_remaining is not None:
            posting.quantity_remaining -= 1
        else:
            posting.quantity_remaining = posting.quantity

        posting.save()

        reservation = Reservation.objects.create(consumer=consumer, **validated_data)

        return reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
