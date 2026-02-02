from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .analytics import * 
from core.models import BundlePosting

# Create your views here.
class TotalListingsView(APIView):
    def get(self, request):
        try:
            # get seller ID from query params
            seller_id = request.query_params.get("seller_id")
            
            # Load historical data, return error if empty
            df = pd.DataFrame.from_records(BundlePosting.objects.values())
            if df.empty:
                return Response({"error": "No data available"}, status=400)

            # outsource business logic for readability (analytics.py)
            response = get_number_of_listings_by_seller(df, seller_id)

            # return in JSON format
            return Response({
                "total_listings": response,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class TotalRevenueView(APIView):
    def get(self, request):
        try:
            # get seller ID from query params
            seller_id = request.query_params.get("seller_id")
            
            # Load historical data, error if empty
            df = pd.DataFrame.from_records(BundlePosting.objects.values())
            if df.empty:
                return Response({"error": "No data available"}, status=400)

            # outsource business logic for readability (analytics.py)
            response = get_total_revenue_by_seller(df, seller_id)

            # return in JSON format
            return Response({
                "total_revenue": response,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
    
class TotalReservationsView(APIView):
    def get(self, request):
        try:
            # get seller ID from query params
            seller_id = request.query_params.get("seller_id")
            
            # Load historical data, or return error if empty
            df = pd.DataFrame.from_records(BundlePosting.objects.values())
            if df.empty:
                return Response({"error": "No data available"}, status=400)

            # outsource business logic for readability (analytics.py)
            response = get_total_reservations_by_seller(df, seller_id)

            # return in JSON format
            return Response({
                "total_reservations": response,
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class FoodWasteReductionView(APIView):
    def get(self, request):
        try:
            # get seller ID from query params
            seller_id = request.query_params.get("seller_id")
            
            # Load historical data, or return error if empty
            df = pd.DataFrame.from_records(BundlePosting.objects.values())
            if df.empty:
                return Response({"error": "No data available"}, status=400)
            
            # outsource business logic for readability (analytics.py)
            response = get_reduction_in_food_waste_by_seller(df, seller_id)
            
            # return in JSON format
            return Response({
                "food_waste_reduction_percentage": response,
            })

        

        except Exception as e:
            return Response({"error": str(e)}, status=500)

