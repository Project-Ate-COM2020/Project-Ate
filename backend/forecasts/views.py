import json

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
from core.models import ForecastInput
from .forecasting import (
    calculate_recommended_price,
    evaluate_baselines,
    generate_recommendation,
    get_confidence_level,
    get_expected_no_show_count,
    get_expected_reservations,
    get_similar_listings,
    moving_average_predict,
    seasonal_naive_predict,
    similarity_predict,
    _best_approach,
)


class ForecastPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data

            # Required inputs
            category = data.get("category")
            day_of_week = data.get("day_of_week")
            time_window = data.get("time_window")

            if not category or not day_of_week or not time_window:
                return Response(
                    {
                        "error": "Missing required parameters: category, day_of_week, time_window"
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Optional inputs
            weather = data.get("weather")
            no_bundles = int(data.get("no_bundles", 1))
            seller_id = data.get("seller_id")
            price = data.get("price")  # posted price (for price-sensitivity)

            # Load historical data
            df = pd.DataFrame.from_records(ForecastInput.objects.values())
            if df.empty:
                return Response({"error": "No historical data available"}, status=400)

            inp = {
                "seller_id": int(seller_id) if seller_id is not None else None,
                "category": category,
                "day_of_week": int(day_of_week),
                "time_window": time_window,
                "weather_flag": int(weather) if weather is not None else None,
                "no_bundles": no_bundles,
                "price": float(price) if price is not None else None,
            }

            # ── run all three approaches ──────────────────────────────────────
            sn_reservations, sn_no_show = seasonal_naive_predict(df, inp)
            ma_reservations, ma_no_show = moving_average_predict(df, inp)
            sim_reservations, sim_no_show = similarity_predict(df, inp)

            # Guard: if the main approach found no neighbours, fall back to seasonal naive
            subset = get_similar_listings(df, inp)
            if subset.empty:
                return Response(
                    {
                        "error": "No matching historical listings found for this category/slot"
                    },
                    status=404,
                )

            # ── baseline comparison via leave-one-out cross-validation ────────
            baseline_metrics = evaluate_baselines(df)
            best_approach = _best_approach(baseline_metrics)
            best_rmse = (baseline_metrics.get(best_approach) or {}).get("rmse")

            # ── confidence & recommendation ───────────────────────────────────
            confidence = get_confidence_level(len(subset), best_rmse)
            recommendation = generate_recommendation(
                inp, sim_reservations, sim_no_show, len(subset)
            )

            # ── recommended price (from similarity neighbourhood) ─────────────
            rec_price = calculate_recommended_price(subset, inp)

            return Response(
                {
                    # Primary forecast (best approach used for recommendation)
                    "primary_forecast": {
                        "approach": "similarity",
                        "predicted_reservations": sim_reservations,
                        "no_show_probability": sim_no_show,
                    },
                    # All three model outputs side-by-side
                    "model_predictions": {
                        "seasonal_naive": {
                            "predicted_reservations": sn_reservations,
                            "no_show_probability": sn_no_show,
                            "description": (
                                "Average of identical day/slot/category historical records. "
                                "No parameters – a simple but robust baseline."
                            ),
                        },
                        "moving_average": {
                            "predicted_reservations": ma_reservations,
                            "no_show_probability": ma_no_show,
                            "description": (
                                "Rolling average of the last 10 records for this category. "
                                "Captures recent trends but ignores day/time patterns."
                            ),
                        },
                        "similarity": {
                            "predicted_reservations": sim_reservations,
                            "no_show_probability": sim_no_show,
                            "description": (
                                "Weighted neighbourhood of similar day/slot/category records. "
                                "Weather-flag matching is double-weighted; "
                                "price sensitivity adjusts the rate by ±50%."
                            ),
                        },
                    },
                    # Leave-one-out error metrics for all three approaches
                    "baseline_comparison": {
                        "method": "leave-one-out cross-validation on full historical dataset",
                        "metrics": baseline_metrics,
                        "best_approach": best_approach,
                    },
                    # Pricing recommendation
                    "recommended_price": rec_price,
                    # Seller-facing recommendation with rationale
                    "recommendation": {
                        "action": recommendation["action"],
                        "rationale": recommendation["rationale"],
                        "confidence": confidence,
                    },
                }
            )

        except Exception as e:
            return Response({"error": str(e)}, status=500)
