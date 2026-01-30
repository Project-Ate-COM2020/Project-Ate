from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from .models import ForecastInput as ForecastInputModel
from .forecasting import (
    ForecastInput,
    get_similar_listings,
    add_no_show_probability,
    aggregate_by_price,
)


class ForecastPredictionView(APIView):
    def get(self, request):
        try:
            category = request.query_params.get("category")
            day_of_week = request.query_params.get("day_of_week")
            time_window = request.query_params.get("time_window")
            weather = request.query_params.get("weather", None)

            # Load database
            df = pd.DataFrame.from_records(ForecastInputModel.objects.values())

            if len(df) == 0:
                return Response({"error": "No data available"})

            # Create forecast input
            inp = ForecastInput(
                seller_id=1,
                category=category,
                day_of_week=day_of_week,
                time_window=time_window,
                weather=weather,
            )

            # Get similar listings and compute predictions
            subset = get_similar_listings(df, inp)
            if len(subset) == 0:
                return Response({"error": "No matching listings found"})

            subset = add_no_show_probability(subset)
            avg_no_show = subset["no_show_prob"].mean()
            avg_reservations = subset["observed_reservations"].mean()

            return Response(
                {
                    "expected_reservations": float(avg_reservations),
                    "expected_no_show_probability": float(avg_no_show),
                }
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
