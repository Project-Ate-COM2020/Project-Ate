from django.http import HttpResponseNotFound
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Allergen, Seller
from core.serializers import (
    AllergenSerializer,
    BundlePostingSerializer,
    CreateBundlePostingSerializer,
)
from ..models import (
    BundlePosting,
    BundlePostingSerializer,
)
from authentication.permissions import IsSeller, IsConsumerOrSeller, IsConsumer


class AllergenListView(APIView):
    name = "allergen-list"
    permission_classes = [AllowAny]

    def get(self, request):
        allergens = Allergen.objects.all().order_by("name")
        serializer = AllergenSerializer(allergens, many=True)
        return Response(serializer.data)


class CreateBundleView(CreateAPIView):
    name = "bundle-create"
    serializer_class = CreateBundlePostingSerializer
    queryset = BundlePosting
    permission_classes = [IsSeller]


class ListBundlesView(APIView):
    name = "bundle-list"
    permission_classes = [IsConsumerOrSeller]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        is_seller = IsSeller().has_permission(self.request, self)
        is_consumer = IsConsumer().has_permission(self.request, self)

        # sellers do not need to see other sellers bundles if they are not consumers
        if is_seller and not is_consumer:
            seller = Seller.objects.get(user=self.request.user)
            return BundlePosting.objects.filter(seller=seller)
        else:
            return BundlePosting.objects.all()


# get all bundles
class BundlesView(RetrieveUpdateDestroyAPIView):
    name: str = "bundle"
    serializer_class = BundlePostingSerializer
    permission_classes = [IsConsumerOrSeller]

    def get_queryset(self):
        if self.request.method == "GET":
            return BundlePosting.objects.all()
        elif (
            self.request.method == "PATCH"
            or self.request.method == "PUT"
            or self.request.method == "DELETE"
        ):
            # only sellers can update or delete bundles
            # sellers can only update or delete their own bundles
            is_seller = IsSeller().has_permission(self.request, self)

            if is_seller:
                seller = Seller.objects.get(user=self.request.user)

                return BundlePosting.objects.filter(seller=seller)
            else:
                return None
        else:
            return None
