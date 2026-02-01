import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from core.models import ForecastInput
from .forecasting import (
    get_similar_listings,
    get_no_show_probability
)


class ForecastPredictionView(APIView):
    def post(self, request):
        try:
            data = json.loads(request.body)
            category = data.get("category")
            day_of_week = data.get("day_of_week")
            time_window = data.get("time_window")
            weather = data.get("weather", None)
            # Load database
            df = pd.DataFrame.from_records(ForecastInput.objects.values())
            
            if not category or not day_of_week or not time_window:
                return Response(
                    {"error": "Missing required parameters: category, day_of_week, time_window"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if len(df) == 0:
                return Response({"error": "No data available"})

            # Create forecast input
            inp = ForecastInput(
                seller_id=1,
                category=category,
                day_of_week=day_of_week,
                time_window=time_window,
                weather_flag=weather,
            )

            # Get similar listings and compute predictions
            subset = get_similar_listings(df, inp)
            if len(subset) == 0:
                return Response({"error": "No matching listings found"})
            else:
                response_data = get_no_show_probability(subset)
                return Response(response_data)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )