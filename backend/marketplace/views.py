from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Bundle, BundleSerializer


class Bundles(APIView):
    def get(self, request):
        bundles = Bundle.objects.all()

        return Response(bundles)
