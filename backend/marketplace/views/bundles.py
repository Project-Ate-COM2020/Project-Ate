from django.http import HttpResponseNotFound
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import Allergen
from core.serializers import AllergenSerializer
from ..models import (
    BundlePosting,
    BundlePostingSerializer,
)
from authentication.permissions import IsSeller


class AllergenListView(APIView):
    name = "allergen-list"
    permission_classes = [AllowAny]

    def get(self, request):
        allergens = Allergen.objects.all().order_by("name")
        serializer = AllergenSerializer(allergens, many=True)
        return Response(serializer.data)


class CreateBundleView(CreateAPIView):
    name = "bundle-create"
    serializer_class = BundlePostingSerializer
    queryset = BundlePosting
    permission_classes = [IsSeller]


# get all bundles
class BundlesView(APIView):
    name: str = "bundles"
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bundles = BundlePosting.objects.all()

        ids = [bundle_id for bundle_id in bundles.values_list("pk", flat=True)]

        return Response(ids)
      
    # permission_classes = [AllowAny]

    def get(self, request):
        bundles = BundlePosting.objects.all()
        serializer = BundlePostingSerializer(bundles, many=True)
        return Response(serializer.data)


# get a specific bundle
class BundleView(APIView):
    name: str = "bundle"
    # permission_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        try:
            bundle = BundlePosting.objects.get(pk=bundle_id)

            serializer = BundlePostingSerializer(bundle)

            return Response(serializer.data)
        except BundlePosting.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# get newest bundles
class BundleNewestView(APIView):
    name = "bundles-newest"
    # permission_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        count = request.GET.get("count", 20)


# get oldest bundles
class BundleOldestView(APIView):
    name = "bundles-oldest"
    # permission_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        count = request.GET.get("count", 20)


# get bundles made between date range bundles
class BundleBetweenView(APIView):
    name = "bundles-between"
    # permission_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")


# get bundles made between date range bundles
class BundleOlderView(APIView):
    name = "bundles-older"
    # permission_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        date = request.GET.get("date")


# get bundles newer than a specified date
class BundleNewerView(APIView):
    name = "bundles-newer"
    # permission_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        date = request.GET.get("date")


# get bundles with open businesses
class BundleOpenView(APIView):
    name = "bundles-open"
    # permission_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        pass


# get bundles made between date range bundles
class BundleCollectionView(APIView):
    name = "bundles-collection"
    # permission_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        pass
