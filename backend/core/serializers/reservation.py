from django.db.models.aggregates import Count
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Reservation, Consumer, BundlePosting, Seller


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


from game.constants import CO2_PER_ITEM


class ConsumerUpdateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = []


class SellerUpdateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["status"]

    def update(self, instance, validated_data):
        user = self.context["request"].user
        seller = Seller.objects.get(user=user)

        new_status = validated_data.get("status")

        match new_status:
            case "collected":
                instance.status = "collected"

                instance.save()

                # user collected a bundle
                posting: BundlePosting = instance.posting
                consumer = instance.consumer

                categories = Reservation.objects.filter(
                    status="collected", consumer=consumer
                ).aggregate(num=Count("posting__category", distinct=True))

                consumer.categories_collected = categories["num"]

                consumer.co2_saved += CO2_PER_ITEM[posting.category.lower()]

                consumer.save()

                return instance
            case "no-show":
                pass

        return instance


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
