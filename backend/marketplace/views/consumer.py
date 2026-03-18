from unittest import case

import django.db.models
from argon2 import PasswordHasher
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import IsAuthenticated

from authentication.permissions import IsConsumer, IsConsumerOrSeller, IsSeller
from core.models import Reservation, User, Seller
from core.serializers import ReservationSerializer
from ..models import Consumer, ConsumerSerializer, RegisterConsumerSerializer


class CreateConsumerView(CreateAPIView):
    name = "consumer-create"
    queryset = Consumer
    serializer_class = RegisterConsumerSerializer
    permission_classes = [IsAuthenticated]


class ListConsumerView(ListAPIView):
    name = "consumer-list"
    serializer_class = ConsumerSerializer
    permission_classes = [IsConsumerOrSeller]

    def get_consumer_queryset(self) -> django.db.models.QuerySet:
        consumer = Consumer.objects.filter(user=self.request.user)
        return consumer

    # list consumers who sellers have reservations with
    def get_seller_queryset(self) -> django.db.models.QuerySet:
        seller = Seller.objects.get(user=self.request.user)
        return Consumer.objects.filter(reservations__posting__seller=seller)

    def get_queryset(self):
        is_seller = IsSeller().has_permission(self.request, self)
        is_consumer = IsConsumer().has_permission(self.request, self)

        if is_seller and not is_consumer:
            return self.get_seller_queryset()
        elif is_consumer and not is_seller:
            return self.get_consumer_queryset()
        elif is_seller and is_consumer:
            return self.get_seller_queryset().union(self.get_consumer_queryset())
        else:
            return Consumer.objects.none()


class ConsumerView(RetrieveUpdateDestroyAPIView):
    name = "consumer"
    serializer_class = ConsumerSerializer
    permission_classes = [IsConsumerOrSeller]

    def get_queryset_for_consumer_for_get_method(self):
        consumer = Consumer.objects.filter(user=self.request.user)
        return consumer

    def get_queryset_for_seller_for_get_method(self):
        seller = Seller.objects.get(user=self.request.user)
        return Consumer.objects.filter(reservations__posting__seller=seller)

    def get_queryset_for_get_method(self):
        is_seller = IsSeller().has_permission(self.request, self)
        is_consumer = IsConsumer().has_permission(self.request, self)

        if is_seller and not is_consumer:
            return self.get_queryset_for_seller_for_get_method()
        elif is_consumer and not is_seller:
            return self.get_queryset_for_consumer_for_get_method()
        elif is_seller and is_consumer:
            return self.get_queryset_for_seller_for_get_method().union(
                self.get_queryset_for_consumer_for_get_method()
            )
        else:
            return Consumer.objects.none()

    def get_queryset(self):
        match self.request.method:
            case "GET":
                # same logic as list method
                return self.get_queryset_for_get_method()
            case "PUT" | "PATCH" | "DELETE":
                return Consumer.objects.filter(user=self.request.user)
            case _:
                return Consumer.objects.none()
