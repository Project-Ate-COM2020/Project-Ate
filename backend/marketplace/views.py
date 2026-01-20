from django.http import HttpResponseNotFound
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Bundle, BundleSerializer


# get all bundles
class BundlesView(APIView):

    def get(self, request):
        bundles = Bundle.objects.all()

        ids = [bundle_id for bundle_id in bundles.values_list("pk", flat=True)]

        return Response(ids)


# get a specific bundle
class BundleView(APIView):

    def get(self, request, bundle_id):
        try:
            bundle = Bundle.objects.get(pk=bundle_id)

            serializer = BundleSerializer(bundle)

            return Response(serializer.data)
        except Bundle.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
