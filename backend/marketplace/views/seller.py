import django
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.settings import APISettings
from rest_framework.views import APIView
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    ListAPIView,
)
from rest_framework.response import Response
from argon2 import PasswordHasher

from authentication.permissions import IsSeller, IsConsumerOrSeller, IsConsumer
from core.models import Consumer
from ..models import (
    Seller,
    SellerSerializer,
    BundlePostingSerializer,
    RegisterSellerSerializer,
)
from ..models import BundlePosting


class CreateSellerView(CreateAPIView):
    name = "seller-create"
    queryset = Seller
    serializer_class = RegisterSellerSerializer
    permission_classes = [IsAuthenticated]


class ListSellerView(ListAPIView):
    name = "seller-list"
    serializer_class = SellerSerializer
    permission_classes = [IsConsumerOrSeller]

    # list sellers who consumers have reservations with
    def get_consumer_queryset(self) -> django.db.models.QuerySet:
        consumer = Consumer.objects.get(user=self.request.user)
        return Seller.objects.filter(bundles__reservations__consumer=consumer)

    def get_seller_queryset(self) -> django.db.models.QuerySet:
        seller = Seller.objects.filter(user=self.request.user)
        return seller

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


class ListSellerBundlesView(ListAPIView):
    name = "seller-list-bundles"
    serializer_class = BundlePostingSerializer
    permission_classes = [IsConsumerOrSeller]

    def get_queryset(self):
        pk = self.request.GET.get("pk")

        return BundlePosting.objects.filter(seller=pk)


class SellerView(RetrieveUpdateDestroyAPIView):
    name = "seller"
    serializer_class = SellerSerializer
    permission_classes = [IsConsumerOrSeller]

    def get_consumer_queryset(self) -> django.db.models.QuerySet:
        return Seller.objects.all()

    def get_seller_queryset(self) -> django.db.models.QuerySet:
        seller = Seller.objects.filter(user=self.request.user)
        return seller

    def get_queryset(self):
        match self.request.method:
            case "GET":
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
            case "PUT" | "PATCH" | "DELETE":
                # only owning user should be able to update or delete seller status
                return Seller.objects.filter(user=self.request.user)
            case _:
                return Seller.objects.none()
