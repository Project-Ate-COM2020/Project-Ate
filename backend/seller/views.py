from django.shortcuts import render
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from core.models import Reservation, Seller


# Create your views here.
class SellerNameView(APIView):
    def get(self, request, seller_id):
        """Gets seller id and returns the seller name."""
        try:
            seller = Seller.objects.get(seller_id=seller_id)
            return Response({"seller_name": seller.name}, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SellerAddressView(APIView):
    def get(self, request, seller_id):
        """Gets seller id and returns the seller address."""
        try:
            seller = Seller.objects.get(seller_id=seller_id)
            return Response({"seller_address": seller.location}, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SellerReservationsView(APIView):
    def get(self, request):
        """
        Gets last 1 collected reservation for a seller
        and next 4 upcoming reservations for a seller.
        """
        seller_id = request.query_params.get("seller_id")

        if not seller_id:
            return Response(
                {"error": "seller_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            seller = Seller.objects.get(seller_id=seller_id)

            reservations = (
                Reservation.objects
                .filter(posting__seller=seller)
                .select_related("posting", "consumer")
                .order_by("timestamp")
            )

            collected_reservations = []
            upcoming_reservations = []

            for reservation in reservations:
                res_data = {
                    "reservation_id": reservation.reservation_id,
                    "posting_id": reservation.posting.posting_id,
                    "reservation_time": reservation.timestamp,
                    "consumer_name": reservation.consumer.display_name,
                    "reservation_code": reservation.claim_code,
                    "status": reservation.status,
                }

                if reservation.status == "collected":
                    collected_reservations.append(res_data)
                else:
                    upcoming_reservations.append(res_data)

            # last 1 collected (most recent)
            collected_reservations = sorted(
                collected_reservations,
                key=lambda x: x["reservation_time"],
                reverse=True
            )[:1]

            # next 4 upcoming (soonest first)
            upcoming_reservations = sorted(
                upcoming_reservations,
                key=lambda x: x["reservation_time"]
            )[:4]

            return Response(
                {
                    "collected_reservations": collected_reservations,
                    "upcoming_reservations": upcoming_reservations,
                },
                status=status.HTTP_200_OK
            )

        except Seller.DoesNotExist:
            return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)