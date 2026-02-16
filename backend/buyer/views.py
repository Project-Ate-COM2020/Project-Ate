from django.shortcuts import render
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from core.models import BundlePosting, Reservation, Seller

class MarkReservationAsReserveredView(APIView):
    def post(self, request):
        """
        Marks a reservation as reserved.
        Expects reservation_id in the request data.
        """
        reservation_id = request.data.get("reservation_id")

        if not reservation_id:
            return Response(
                {"error": "reservation_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reservation = Reservation.objects.get(reservation_id=reservation_id)
            reservation.status = "reserved"
            reservation.save()
            return Response({"message": "Reservation marked as reserved"}, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
        
class MarkReservationAsUnreservedView(APIView):
    def post(self, request):
        """
        Marks a reservation as unreserved.
        Expects reservation_id in the request data.
        Deletes the reservation from the database.
        """
        reservation_id = request.data.get("reservation_id")

        if not reservation_id:
            return Response(
                {"error": "reservation_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            reservation = Reservation.objects.get(reservation_id=reservation_id)
            reservation.delete()
            return Response({"message": "Reservation deleted"}, status=status.HTTP_200_OK)
        except Reservation.DoesNotExist:
            return Response({"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)