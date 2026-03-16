from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from ..models import ReservationSerializer, Reservation, CreateReservationSerializer

from authentication.permissions import IsConsumer


class CreateReservationView(CreateAPIView):
    name = "reservations-create"
    serializer_class = CreateReservationSerializer
    queryset = Reservation
    permission_classes = [IsConsumer]


class ReservationView(RetrieveUpdateDestroyAPIView):
    name = "reservations"
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAuthenticated]
