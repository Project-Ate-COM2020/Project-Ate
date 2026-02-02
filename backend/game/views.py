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
    permission_classes = IsAuthenticated

    def get(self, request):

        consumer = request.user.consumer

        collected = Reservation.objects.filter(consumer=consumer, status="collected")
        
        return Response({
            "current_streak": consumer.streak, 
            "total_rescues": collected.count(), 
            "co2_estimate": collected.count * 2
            # using 2 as a guess for average co2 used in a meal
            })
    
class RecentRescuesView(ListAPIView):
    permission_classes = IsAuthenticated
    serializer_class = ReservationSerializer

    def get_queryset(self):
        consumer = self.request.user.consumer
        limit = int(self.request.query_params.get("limit", 10))

        return (
            Reservation.objects.filter(consumer=consumer, status="collected").order_by("collected_at")[:limit]
        )

# test view
class TestView(APIView):
    def get(self, request):
        return Response({"ok": True})
    

    