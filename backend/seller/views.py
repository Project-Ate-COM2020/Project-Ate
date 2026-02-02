from django.shortcuts import render
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from core.models import Seller


# Create your views here.
class SellerNameView(APIView):
    def get(self, request, seller_id):
        """Gets seller id and returns the seller name."""
        try:
            seller = Seller.objects.get(seller_id=seller_id)
            return Response({"seller_name": seller.name}, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)
        
class SellerAddressView(APIView):
    def get(self, request, seller_id):
        """Gets seller id and returns the seller address."""
        try:
            seller = Seller.objects.get(seller_id=seller_id)
            return Response({"seller_address": seller.location}, status=status.HTTP_200_OK)
        except Seller.DoesNotExist:
            return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)