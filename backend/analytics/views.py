from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .analytics import (
    get_number_of_listings_by_seller,
    get_total_revenue_by_seller,
    get_total_reservations_by_seller,
    get_reduction_in_food_waste_by_seller,
    get_total_no_shows_by_seller,
    get_collected_reservations_by_seller,
    get_sell_through_breakdown,
    get_waste_proxy,
    get_pricing_effectiveness,
    get_popular_categories,
    get_best_pickup_windows,
)
from core.models import BundlePosting


class TotalListingsView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            df = pd.DataFrame.from_records(BundlePosting.objects.values())
            if df.empty:
                return Response({"error": "No data available"}, status=400)
            response = get_number_of_listings_by_seller(df, seller_id)
            return Response(response)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TotalRevenueView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            df = pd.DataFrame.from_records(BundlePosting.objects.values())
            if df.empty:
                return Response({"error": "No data available"}, status=400)
            response = get_total_revenue_by_seller(df, seller_id)
            return Response(response)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TotalReservationsView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            if not seller_id:
                return Response(
                    {"error": "seller_id query parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            response = get_total_reservations_by_seller(seller_id)
            return Response({"total_reservations": response})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class FoodWasteReductionView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            if not seller_id:
                return Response(
                    {"error": "seller_id query parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            response = get_reduction_in_food_waste_by_seller(seller_id)
            return Response({"food_waste_reduction_percentage": response})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class TotalNoShowsView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            if not seller_id:
                return Response(
                    {"error": "seller_id query parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            response = get_total_no_shows_by_seller(seller_id)
            return Response({"total_no_shows": response})
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class GetCollectedReservationsView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            if not seller_id:
                return Response(
                    {"error": "seller_id query parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            response = get_collected_reservations_by_seller(seller_id)
            return Response(response)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


# -------------- sprint 2 views ---------------

class SellThroughBreakdownView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            if not seller_id:
                return Response(
                    {"error": "seller_id query parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(get_sell_through_breakdown(seller_id))
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class WasteProxyView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            if not seller_id:
                return Response(
                    {"error": "seller_id query parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(get_waste_proxy(seller_id))
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class PricingEffectivenessView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            if not seller_id:
                return Response(
                    {"error": "seller_id query parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(get_pricing_effectiveness(seller_id))
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class PopularCategoriesView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            if not seller_id:
                return Response(
                    {"error": "seller_id query parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(get_popular_categories(seller_id))
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class BestPickupWindowsView(APIView):
    def get(self, request):
        try:
            seller_id = request.query_params.get("seller_id")
            if not seller_id:
                return Response(
                    {"error": "seller_id query parameter is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response(get_best_pickup_windows(seller_id))
        except Exception as e:
            return Response({"error": str(e)}, status=500)
