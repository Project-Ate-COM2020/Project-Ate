from django.shortcuts import render
from marketplace.models import Consumer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from core.models import Consumer, Reservation, BundlePosting
from django.utils import timezone
from .serializers import ReservationSerializer

# Create your views here.

CO2_PER_ITEM = {
    "Hot Meals": 2.5,
    "Fresh Produce": 0.5,
    "Prepared Salads": 1.2,
    "Bakery": 0.8,
    "Desserts": 1.0,
    "Dairy": 1.5
}

class GameSummaryView(APIView):

    def get(self, request):
        consumer = Consumer.objects.get(consumer_id=1)
        collected = Reservation.objects.filter(consumer=consumer, status="collected").select_related("posting")
        total_co2 = 0
        for reservation in collected:
            posting = reservation.posting
            co2_per_item = CO2_PER_ITEM.get(posting.category, 1.0)
            total_co2 += co2_per_item * posting.quantity

        # Calculate if rescued this week
        now = timezone.now()
        current_week = now.isocalendar()[1]
        current_year = now.year
        has_rescued_this_week = collected.filter(
            collected_at__week=current_week,
            collected_at__year=current_year
        ).exists()

        return Response({
            "current_streak_weeks": consumer.streak,
            "has_rescued_this_week": has_rescued_this_week,
            "total_rescued_bundles": collected.count(),
            "estimated_co2e_saved_kg": total_co2
        })
    
class RecentRescuesView(ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        consumer = Consumer.objects.get(consumer_id=1)
        limit = int(self.request.query_params.get("limit", 10))
        # sets the limit at 10 so only the last 10 records are shown

        return (
            Reservation.objects.filter(consumer=consumer, status="collected").order_by("collected_at")[:limit]
            # gets all the records that are "collected" and the limit is set
        )

# test view
class TestView(APIView):
    def get(self, request):
        return Response({"ok": True})
