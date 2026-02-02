from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import Consumer, Reservation
from .serializers import ReservationSerializer

# Create your views here.

class GameSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        consumer = request.user.consumer

        collected = Reservation.objects.filter(consumer=consumer, status="collected")
        # all the records that have been collected by the consumer
        
        return Response({
            "current_streak": consumer.streak, 
            "total_rescues": collected.count(), 
            "co2_estimate": collected.count * 2
            # using 2 as a guess for average co2 used in a meal
            # may need to go more in depth here, e.g. working out different categories of food have different co2 values
            # using the quantity from the 'bundle_posting' entity
            })
    
class RecentRescuesView(ListAPIView):
    permission_classes = [IsAuthenticated]
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
    

    