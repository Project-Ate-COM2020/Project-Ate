from django.http import HttpResponseNotFound
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from ..models import Bundle, BundleSerializer


class CreateBundleView(CreateAPIView):
    name = "bundle-create"
    serializer_class = BundleSerializer
    queryset = Bundle
    authentication_classes = [IsAuthenticated]


# get all bundles
class BundlesView(APIView):
    name: str = "bundles"
    authentication_classes = [IsAuthenticated]

    def get(self, request):
        bundles = Bundle.objects.all()

        ids = [bundle_id for bundle_id in bundles.values_list("pk", flat=True)]

        return Response(ids)


# get a specific bundle
class BundleView(APIView):
    name: str = "bundle"
    authentication_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        try:
            bundle = Bundle.objects.get(pk=bundle_id)

            serializer = BundleSerializer(bundle)

            return Response(serializer.data)
        except Bundle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# get newest bundles
class BundleNewestView(APIView):
    name = "bundles-newest"
    authentication_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        count = request.GET.get("count", 20)


# get oldest bundles
class BundleOldestView(APIView):
    name = "bundles-oldest"
    authentication_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        count = request.GET.get("count", 20)


# get bundles made between date range bundles
class BundleBetweenView(APIView):
    name = "bundles-between"
    authentication_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        date_from = request.GET.get("from")
        date_to = request.GET.get("to")


# get bundles made between date range bundles
class BundleOlderView(APIView):
    name = "bundles-older"
    authentication_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        date = request.GET.get("date")


# get bundles newer than a specified date
class BundleNewerView(APIView):
    name = "bundles-newer"
    authentication_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        date = request.GET.get("date")


# get bundles with open businesses
class BundleOpenView(APIView):
    name = "bundles-open"
    authentication_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        pass


# get bundles made between date range bundles
class BundleCollectionView(APIView):
    name = "bundles-collection"
    authentication_classes = [IsAuthenticated]

    def get(self, request, bundle_id):
        pass
