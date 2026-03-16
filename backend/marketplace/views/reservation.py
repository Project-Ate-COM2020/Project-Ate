import django.db.models
from django.db.models import QuerySet
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsConsumerOrSeller, IsSeller
from core.models import User, BundlePosting, Consumer, Seller

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
    permission_classes = [IsConsumerOrSeller]

    def get_seller_queryset(self) -> django.db.models.QuerySet:
        user = User.objects.get(id=self.request.user.id)
        seller = Seller.objects.get(user=user)
        return Reservation.objects.filter(reservations__postings=seller)

    def get_consumer_queryset(self) -> django.db.models.QuerySet:
        user = User.objects.get(id=self.request.user.id)
        consumer = Consumer.objects.get(user=user)
        reservations = Reservation.objects.filter(consumer=consumer)
        return reservations

    # restrict dynamically the reservations a consumer or seller can see
    def get_queryset(self):
        is_seller = IsSeller().has_permission(self.request, self)
        is_consumer = IsConsumer().has_permission(self.request, self)

        if is_seller and not is_consumer:
            return self.get_seller_queryset()
        elif is_consumer and not is_seller:
            return self.get_consumer_queryset()
        else:
            return self.get_seller_queryset().union(self.get_consumer_queryset())
