from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from core.models import Consumer, Reservation, BundlePosting
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

        consumer = request.user.consumer

        collected = Reservation.objects.filter(consumer=consumer, status="collected").select_related("posting_id")
        # all the records that have been collected by the consumer

        total_co2 = 0

        for reservation in collected:
            posting = reservation.posting_id
            co2_per_item = CO2_PER_ITEM.get(posting.category, 1.0)
            total_co2 = total_co2 + (co2_per_item * posting.quantity)
        
        return Response({
            "current_streak": consumer.streak, 
            "total_rescues": collected.count(), 
            "co2_estimate": total_co2
            })
    
class RecentRescuesView(ListAPIView):
    serializer_class = ReservationSerializer

    def get_queryset(self):
        consumer = self.request.user.consumer
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
    

    