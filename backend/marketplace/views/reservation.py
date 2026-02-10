from django.http import HttpResponseNotFound
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import ReservationSerializer, Reservation


class CreateReservationView(CreateAPIView):
    name = "reservations-create"
    serializer_class = ReservationSerializer
    queryset = Reservation
    authentication_classes = [IsAuthenticated]
