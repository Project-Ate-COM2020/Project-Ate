from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.settings import APISettings
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView
from rest_framework.response import Response

from ..models import Seller, SellerSerializer, BundleSerializer
from ..models import Bundle


class CreateSellerView(CreateAPIView):
    name = "seller-create"
    queryset = Seller
    serializer_class = SellerSerializer
    authentication_classes = [AllowAny]


class SellerView(RetrieveUpdateDestroyAPIView):
    name = "seller"
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    authentication_classes = [IsAuthenticated]


# get all bundles by a seller
class SellerBundlesView(APIView):
    name: str = "seller-bundles"
    authentication_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        try:
            seller = Seller.objects.get(pk=seller_id)

            bundle = Bundle.objects.get(seller=seller)

            serializer = BundleSerializer(bundle)

            return Response(serializer.data)
        except Bundle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# get newest bundles
class SellerBundleNewestView(APIView):
    name = "seller-bundles-newest"
    authentication_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        count = request.GET.get("count", 20)


# get oldest bundles
class SellerBundleOldestView(APIView):
    name = "seller-bundles-oldest"
    authentication_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        count = request.GET.get("count", 20)


# get bundles made between date range bundles
class SellerBundleBetweenView(APIView):
    name = "seller-bundles-between"
    authentication_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")


# get bundles made between date range bundles
class SellerBundleOlderView(APIView):
    name = "seller-bundles-older"
    authentication_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        date = request.GET.get("date")


# get bundles newer than a specified date
class SellerBundleNewerView(APIView):
    name = "seller-bundles-newer"
    authentication_classes = [IsAuthenticated]

    def get(self, request, seller_id):
        date = request.GET.get("date")
