import django.db.models
from django.db.models import QuerySet
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsConsumerOrSeller, IsSeller
from core.models import User, BundlePosting, Consumer, Seller
from core.serializers import (
    SellerUpdateReservationSerializer,
    ConsumerUpdateReservationSerializer,
)

from ..models import ReservationSerializer, Reservation, CreateReservationSerializer

from authentication.permissions import IsConsumer


class RestrictsQuerysetToOwned:
    def get_seller_queryset(self) -> django.db.models.QuerySet:
        user = User.objects.get(id=self.request.user.id)
        seller = Seller.objects.get(user=user)
        return Reservation.objects.filter(posting__seller=seller)

    def get_consumer_queryset(self) -> django.db.models.QuerySet:
        user = User.objects.get(id=self.request.user.id)
        consumer = Consumer.objects.get(user=user)
        reservations = Reservation.objects.filter(consumer=consumer)
        return reservations

    def get_queryset(self):
        is_seller = IsSeller().has_permission(self.request, self)
        is_consumer = IsConsumer().has_permission(self.request, self)

        if is_seller and not is_consumer:
            return self.get_seller_queryset()
        elif is_consumer and not is_seller:
            return self.get_consumer_queryset()
        elif is_consumer and is_seller:
            return self.get_seller_queryset().union(self.get_consumer_queryset())
        else:
            return None


class CreateReservationView(CreateAPIView):
    name = "reservations-create"
    serializer_class = CreateReservationSerializer
    queryset = Reservation
    permission_classes = [IsConsumer]


class ListReservationView(RestrictsQuerysetToOwned, ListAPIView):
    name = "reservations-list"
    serializer_class = ReservationSerializer
    permission_classes = [IsConsumerOrSeller]


class ReservationView(RestrictsQuerysetToOwned, RetrieveUpdateDestroyAPIView):
    name = "reservations"
    permission_classes = [IsConsumerOrSeller]

    def get_serializer_class(self):
        is_seller = IsSeller().has_permission(self.request, self)

        match self.request.method:
            case "PUT" | "PATCH":
                match is_seller:
                    case True:
                        return SellerUpdateReservationSerializer
                    case _:
                        return ConsumerUpdateReservationSerializer
            case _:
                return ReservationSerializer
