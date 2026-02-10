import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from core.models import ForecastInput
from .forecasting import (
    calculate_recommended_price,
    get_expected_no_show_count,
    get_expected_reservations,
    get_similar_listings,
)


class ForecastPredictionView(APIView):
    def post(self, request):
        try:
            data = request.data  # DRF JSON parsing

            # Required inputs
            category = data.get("category")
            day_of_week = data.get("day_of_week")
            time_window = data.get("time_window")

            # Optional inputs
            weather = data.get("weather")
            no_bundles = data.get("no_bundles", 0)
            seller_id = 1

            if not category or not day_of_week or not time_window:
                return Response(
                    {"error": "Missing required parameters: category, day_of_week, time_window"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Load historical data
            df = pd.DataFrame.from_records(ForecastInput.objects.values())
            if df.empty:
                return Response({"error": "No data available"}, status=400)

            # Plain dict input (NO DB write)
            inp = {
                "seller_id": int(seller_id),
                "category": category,
                "day_of_week": int(day_of_week),
                "time_window": time_window,
                "weather_flag": None if weather is None else int(weather),
                "no_bundles": int(no_bundles),
            }

            subset = get_similar_listings(df, inp)

            if subset.empty:
                return Response({"error": "No matching listings found"}, status=404)

            return Response({
                "expected_no_show_count": get_expected_no_show_count(subset, inp),
                "expected_reservations": get_expected_reservations(subset, inp),
                "recommended_price": calculate_recommended_price(subset, inp),
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
