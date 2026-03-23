from datetime import timedelta

from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.permissions import IsConsumer
from core.models import Badges, Consumer, Reservation
from game.constants import get_co2_per_item


CO2_PER_ITEM = get_co2_per_item()


class GameSummaryView(APIView):
    name = "game-summary"
    permission_classes = [IsConsumer]

    def get(self, request, *args, **kwargs):
        consumer = Consumer.objects.get(user=request.user)
        collected_qs = Reservation.objects.filter(
            consumer=consumer,
            status="collected",
            collected_at__isnull=False,
        )

        now = timezone.now()
        this_week_start = now.date() - timedelta(days=now.weekday())

        rescued_week_starts = {
            reservation.collected_at.date() - timedelta(days=reservation.collected_at.weekday())
            for reservation in collected_qs
        }

        has_rescued_this_week = collected_qs.filter(
            collected_at__week=now.isocalendar()[1],
            collected_at__year=now.year,
        ).exists()

        # If they have not rescued this week yet, streak currently ends at last week.
        streak_cursor = this_week_start if has_rescued_this_week else this_week_start - timedelta(days=7)
        current_streak_weeks = 0
        while streak_cursor in rescued_week_starts:
            current_streak_weeks += 1
            streak_cursor -= timedelta(days=7)

        badges = list(
            Badges.objects.filter(consumers_who_have_earned__consumer_id=consumer)
            .values_list("name", flat=True)
            .distinct()
        )

        unique_categories_rescued = (
            collected_qs.values("posting__category").distinct().count()
        )

        estimated_co2e_saved_kg = round(
            sum(
                float(CO2_PER_ITEM.get(str(reservation.posting.category).lower(), 0))
                for reservation in collected_qs.select_related("posting")
            ),
            2,
        )

        return Response(
            {
                "current_streak_weeks": current_streak_weeks,
                "has_rescued_this_week": has_rescued_this_week,
                "total_rescued_bundles": collected_qs.count(),
                "estimated_co2e_saved_kg": estimated_co2e_saved_kg,
                "badges": badges,
                "unique_categories_rescued": unique_categories_rescued,
            }
        )
