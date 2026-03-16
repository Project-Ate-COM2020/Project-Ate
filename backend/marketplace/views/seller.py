from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.settings import APISettings
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response
from argon2 import PasswordHasher

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

class SellerView(RetrieveUpdateDestroyAPIView):
    name = "seller"
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]


# get all bundles by a seller
class SellerBundlesView(APIView):
    name: str = "seller-bundles"
    permission_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        try:
            seller = Seller.objects.get(pk=seller_id)

            bundle = BundlePosting.objects.get(seller=seller)

            serializer = BundlePostingSerializer(bundle)

            return Response(serializer.data)
        except BundlePosting.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# get newest bundles
class SellerBundleNewestView(APIView):
    name = "seller-bundles-newest"
    permission_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        count = request.GET.get("count", 20)


# get oldest bundles
class SellerBundleOldestView(APIView):
    name = "seller-bundles-oldest"
    permission_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        count = request.GET.get("count", 20)


# get bundles made between date range bundles
class SellerBundleBetweenView(APIView):
    name = "seller-bundles-between"
    permission_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")


# get bundles made between date range bundles
class SellerBundleOlderView(APIView):
    name = "seller-bundles-older"
    permission_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        date = request.GET.get("date")


# get bundles newer than a specified date
class SellerBundleNewerView(APIView):
    name = "seller-bundles-newer"
    permission_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        date = request.GET.get("date")
