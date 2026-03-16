from django.shortcuts import render
import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .models import BundlePosting, Reservation, Seller
from claimcodegeneration import generate_claim_code


class MarkReservationAsReserveredView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Marks a reservation as reserved.
        Adds reservation to the database with status "reserved".
        Expects bundle_posting, buyer id in the request data.
        """
        posting_id = request.data.get("posting_id")
        consumer_id = request.data.get("consumer_id")

        if not posting_id or not consumer_id:
            return Response(
                {"error": "posting_id and consumer_id are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            posting = BundlePosting.objects.get(posting_id=posting_id)
            if posting.quantity_remaining <= 0:
                return Response(
                    {"error": "No quantity remaining for this bundle"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            reservation = Reservation.objects.create(
                posting=posting,
                consumer_id=consumer_id,
                claim_code=generate_claim_code(),
                status="reserved",
            )

            posting.quantity_remaining -= 1
            posting.save()
            return Response(
                {
                    "message": "Reservation marked as reserved",
                    "reservation_id": reservation.reservation_id,
                },
                status=status.HTTP_200_OK,
            )
        except BundlePosting.DoesNotExist:
            return Response(
                {"error": "BundlePosting not found"}, status=status.HTTP_404_NOT_FOUND
            )


class MarkReservationAsUnreservedView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Marks a reservation as unreserved.
        Expects reservation_id in the request data.
        Deletes the reservation from the database.
        Adds quantity remaining back to the bundle_posting.
        """
        reservation_id = request.data.get("reservation_id")

        if not reservation_id:
            return Response(
                {"error": "reservation_id is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            reservation = Reservation.objects.get(reservation_id=reservation_id)
            posting = reservation.posting
            posting.quantity_remaining += 1
            posting.save()
            reservation.delete()
            return Response(
                {"message": "Reservation deleted"}, status=status.HTTP_200_OK
            )
        except Reservation.DoesNotExist:
            return Response(
                {"error": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND
            )


class GetBuyerReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, consumer_id):
        """
        Retrieves all reservations for a given consumer.
        Expects consumer_id as a URL parameter.
        """
        reservations = Reservation.objects.filter(consumer_id=consumer_id)
        reservation_data = []
        for reservation in reservations:
            reservation_data.append(
                {
                    "reservation_id": reservation.reservation_id,
                    "posting_id": reservation.posting.posting_id,
                    "claim_code": reservation.claim_code,
                    "status": reservation.status,
                    "created_at": reservation.created_at,
                }
            )
        return Response({"reservations": reservation_data}, status=status.HTTP_200_OK)
