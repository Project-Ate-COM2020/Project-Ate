from datetime import timedelta

from django.db.models.aggregates import Count
from django.utils import timezone
from django.db.models.aggregates import Count
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import (
    Reservation,
    Consumer,
    BundlePosting,
    Seller,
    Badges,
    BadgeMapping,
)


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


from game.constants import get_co2_per_item

CO2_PER_ITEM = get_co2_per_item()


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
                instance.collected_at = timezone.now()

                instance.save()

                # user collected a bundle
                posting: BundlePosting = instance.posting
                consumer = instance.consumer

                # update consumer states
                categories = Reservation.objects.filter(
                    status="collected", consumer=consumer
                ).aggregate(num=Count("posting__category", distinct=True))

                consumer.categories_collected = categories["num"]

                number_to_add = CO2_PER_ITEM[posting.category.lower()]

                consumer.co2_saved += number_to_add

                consumer.save()

                consumer.refresh_from_db()

                # create new badge mappings
                badges_can_have = Badges.objects.filter(
                    min_categories__lte=consumer.categories_collected,
                    min_co2__lte=consumer.co2_saved,
                )

                already_have = Badges.objects.filter(
                    consumers_who_have_earned__consumer_id=consumer,
                )

                badges_to_add = badges_can_have.difference(already_have)

                join = [
                    BadgeMapping(consumer_id=consumer, badge_id=b)
                    for b in badges_to_add
                ]

                BadgeMapping.objects.bulk_create(join)

                last_collected = (
                    Reservation.objects.filter(status="collected")
                    .order_by("-collected_at")
                    .first()
                )

                if last_collected is not None:
                    # check
                    timestamp = last_collected.collected_at
                    now = instance.collected_at

                    satisfies_streak = now.date() == (
                        timestamp.date() + timedelta(days=1)
                    )

                    if satisfies_streak:
                        consumer.streak += 1

                consumer.save()

                consumer.refresh_from_db()

                # create new badge mappings
                badges_can_have = Badges.objects.filter(
                    min_categories__lte=consumer.categories_collected,
                    min_co2__lte=consumer.co2_saved,
                )

                already_have = Badges.objects.filter(
                    consumers_who_have_earned__consumer_id=consumer,
                )

                badges_to_add = badges_can_have.difference(already_have)

                join = [
                    BadgeMapping(consumer_id=consumer, badge_id=b)
                    for b in badges_to_add
                ]

                BadgeMapping.objects.bulk_create(join)

                last_collected = (
                    Reservation.objects.filter(status="collected")
                    .order_by("-collected_at")
                    .first()
                )

                if last_collected is not None:
                    # check
                    timestamp = last_collected.collected_at
                    now = instance.collected_at

                    satisfies_streak = now.date() == (
                        timestamp.date() + timedelta(days=1)
                    )

                    if satisfies_streak:
                        consumer.streak += 1

                consumer.save()

                return instance
            case "no-show":
                pass

        return instance


class ReservationSerializer(serializers.ModelSerializer):
    bundleCategory = serializers.CharField(source="posting.category", read_only=True)
    consumerDisplayName = serializers.CharField(source="consumer.display_name", read_only=True)
    sellerLocation = serializers.CharField(source="posting.seller.location", read_only=True)

    class Meta:
        model = Reservation
        fields = "__all__"
