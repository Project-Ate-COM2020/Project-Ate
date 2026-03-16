from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch
import unittest
import pandas as pd
from django.conf import settings
from rest_framework.test import force_authenticate

from core.models import ForecastInput, Seller
from forecasts.forecasting import (
    get_adjacent_days,
    get_adjacent_time_slots,
    get_no_show_probability,
    get_expected_no_show_count,
    get_expected_reservations,
    seasonal_naive_predict,
    moving_average_predict,
    similarity_predict,
    evaluate_baselines,
    generate_recommendation,
    get_confidence_level,
)
from rest_framework_simplejwt.tokens import RefreshToken

# ── helpers ───────────────────────────────────────────────────────────────────


def _make_df(rows):
    """Build a minimal ForecastInput-shaped DataFrame from a list of dicts."""
    defaults = {
        "record_id": 1,
        "category": "veg_box",
        "day_of_week": 2,
        "time_window": "18:00-19:00",
        "price": 5.0,
        "weather_flag": 0,
        "observed_reservations": 8,
        "observed_no_show": 1,
        "unreserved_stock": 1,
        "seller_id": 1,
    }
    records = [{**defaults, "record_id": i + 1, **r} for i, r in enumerate(rows)]
    return pd.DataFrame(records)


# ── integration tests ─────────────────────────────────────────────────────────


class ForecastPredictionViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("forecast-prediction")

        self.user_model = get_user_model()

        self.user = self.user_model.objects.create_user(
            "user", "user@user.com", "password"
        )

        self.seller = Seller.objects.create(
            name="Seller One",
            location="Test Location",
            opening_hours="09:00-17:00",
            contact_stub="seller1@example.com",
            user=self.user,
        )

        self.valid_payload = {
            "seller_id": self.seller.seller_id,
            "category": "veg_box",
            "day_of_week": 2,
            "time_window": "18:00-19:00",
            "weather": 0,
            "no_bundles": 10,
        }

        response = self.client.post(
            reverse("user-token"),
            {"username": "user", "password": "password"},
            format="json",
        ).json()

        self.auth_header = {"AUTHORIZATION": f"Bearer {response.get('access')}"}

    def _create_forecast_input_row(self, **kwargs):
        defaults = dict(
            day_of_week=2,
            time_window="18:00-19:00",
            seller=self.seller,
            category="veg_box",
            price=5.00,
            weather_flag=0,
            observed_reservations=8,
            observed_no_show=1,
            unreserved_stock=1,
        )
        defaults.update(kwargs)
        return ForecastInput.objects.create(**defaults)

    # ── error cases ───────────────────────────────────────────────────────────

    def test_missing_required_params_returns_400(self):
        resp = self.client.post(
            self.url, {"category": "veg_box"}, format="json", headers=self.auth_header
        )
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.data)

    def test_no_data_available_returns_400(self):
        resp = self.client.post(
            self.url, self.valid_payload, format="json", headers=self.auth_header
        )
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data.get("error"), "No historical data available")

    @patch("forecasts.views.get_similar_listings")
    def test_no_matching_listings_returns_404(self, mock_get_similar_listings):
        self._create_forecast_input_row()
        mock_get_similar_listings.return_value = pd.DataFrame()
        resp = self.client.post(
            self.url, self.valid_payload, format="json", headers=self.auth_header
        )
        self.assertEqual(resp.status_code, 404)
        self.assertIn("error", resp.data)

    # ── happy path ────────────────────────────────────────────────────────────

    def test_happy_path_returns_expected_keys(self):
        """A valid request with matching data must return the full forecast structure."""
        self._create_forecast_input_row()
        resp = self.client.post(
            self.url, self.valid_payload, format="json", headers=self.auth_header
        )
        self.assertEqual(resp.status_code, 200)

        # Top-level keys
        self.assertIn("primary_forecast", resp.data)
        self.assertIn("model_predictions", resp.data)
        self.assertIn("baseline_comparison", resp.data)
        self.assertIn("recommended_price", resp.data)
        self.assertIn("recommendation", resp.data)

    def test_primary_forecast_fields(self):
        self._create_forecast_input_row()
        resp = self.client.post(
            self.url, self.valid_payload, format="json", headers=self.auth_header
        )
        self.assertEqual(resp.status_code, 200)
        pf = resp.data["primary_forecast"]
        self.assertEqual(pf["approach"], "similarity")
        self.assertIn("predicted_reservations", pf)
        self.assertIn("no_show_probability", pf)

    def test_model_predictions_has_all_three_approaches(self):
        self._create_forecast_input_row()
        resp = self.client.post(
            self.url, self.valid_payload, format="json", headers=self.auth_header
        )
        self.assertEqual(resp.status_code, 200)
        models = resp.data["model_predictions"]
        self.assertIn("seasonal_naive", models)
        self.assertIn("moving_average", models)
        self.assertIn("similarity", models)

    def test_baseline_comparison_fields(self):
        self._create_forecast_input_row()
        resp = self.client.post(
            self.url, self.valid_payload, format="json", headers=self.auth_header
        )
        self.assertEqual(resp.status_code, 200)
        bc = resp.data["baseline_comparison"]
        self.assertIn("metrics", bc)
        self.assertIn("best_approach", bc)
        metrics = bc["metrics"]
        for approach in ("seasonal_naive", "moving_average", "similarity"):
            self.assertIn(approach, metrics)

    def test_recommendation_fields(self):
        self._create_forecast_input_row()
        resp = self.client.post(
            self.url, self.valid_payload, format="json", headers=self.auth_header
        )
        self.assertEqual(resp.status_code, 200)
        rec = resp.data["recommendation"]
        self.assertIn("action", rec)
        self.assertIn("rationale", rec)
        self.assertIn("confidence", rec)
        self.assertIn(rec["confidence"], ("low", "medium", "high"))

    def test_price_input_accepted(self):
        """Passing a price should not cause an error."""
        self._create_forecast_input_row()
        payload = {**self.valid_payload, "price": 4.50}
        resp = self.client.post(
            self.url, payload, format="json", headers=self.auth_header
        )
        self.assertEqual(resp.status_code, 200)


# ── unit tests – helper functions ─────────────────────────────────────────────


class AdjacentDaysTests(unittest.TestCase):
    def test_monday_wraps_to_sunday(self):
        self.assertEqual(get_adjacent_days(1), [7, 1, 2])

    def test_sunday_wraps_to_monday(self):
        self.assertEqual(get_adjacent_days(7), [6, 7, 1])

    def test_midweek(self):
        self.assertEqual(get_adjacent_days(4), [3, 4, 5])


class AdjacentTimeSlotsTests(unittest.TestCase):
    def test_hourly_slot(self):
        self.assertEqual(
            get_adjacent_time_slots("10:00-11:00"),
            ["09:00-10:00", "10:00-11:00", "11:00-12:00"],
        )

    def test_two_hour_slot(self):
        result = get_adjacent_time_slots("18:00-20:00")
        self.assertEqual(result, ["16:00-18:00", "18:00-20:00", "20:00-22:00"])


class NoShowProbabilityTests(unittest.TestCase):
    def test_empty_subset_returns_zero(self):
        self.assertEqual(get_no_show_probability(pd.DataFrame()), 0.0)

    def test_no_reservations_returns_zero(self):
        df = pd.DataFrame({"observed_no_show": [3], "observed_reservations": [0]})
        self.assertEqual(get_no_show_probability(df), 0.0)

    def test_standard_calculation(self):
        df = pd.DataFrame(
            {
                "observed_no_show": [2, 3],
                "observed_reservations": [10, 15],
            }
        )
        # (2+3)/(10+15) = 0.2
        self.assertAlmostEqual(get_no_show_probability(df), 0.2)


class ExpectedNoShowCountTests(unittest.TestCase):
    def test_calculation(self):
        df = pd.DataFrame(
            {
                "observed_no_show": [2],
                "observed_reservations": [10],
            }
        )
        inp = {"no_bundles": 5}
        # 0.2 * 5 = 1.0
        self.assertAlmostEqual(get_expected_no_show_count(df, inp), 1.0)


class ExpectedReservationsTests(unittest.TestCase):
    def test_calculation(self):
        df = pd.DataFrame(
            {
                "observed_reservations": [8],
                "unreserved_stock": [2],
                "observed_no_show": [0],
            }
        )
        inp = {"no_bundles": 10}
        # rate = 8/10 = 0.8, result = 8.0
        self.assertAlmostEqual(get_expected_reservations(df, inp), 8.0)


# ── unit tests – new forecasting approaches ───────────────────────────────────


class SeasonalNaivePredictTests(unittest.TestCase):
    def _make_inp(self, **kwargs):
        base = {
            "category": "veg_box",
            "day_of_week": 2,
            "time_window": "18:00-19:00",
            "no_bundles": 10,
            "weather_flag": 0,
            "price": None,
        }
        base.update(kwargs)
        return base

    def test_exact_match_predicts_correctly(self):
        # 8 reserved out of 10 total → rate 0.8 → 8.0 for 10 bundles
        df = _make_df(
            [
                {
                    "day_of_week": 2,
                    "time_window": "18:00-19:00",
                    "observed_reservations": 8,
                    "unreserved_stock": 2,
                    "observed_no_show": 0,
                },
            ]
        )
        preds, no_show = seasonal_naive_predict(df, self._make_inp())
        self.assertAlmostEqual(preds, 8.0)

    def test_falls_back_to_category_when_no_exact_slot(self):
        # Different day/time but same category
        df = _make_df(
            [
                {
                    "day_of_week": 5,
                    "time_window": "10:00-11:00",
                    "observed_reservations": 6,
                    "unreserved_stock": 4,
                    "observed_no_show": 0,
                },
            ]
        )
        preds, _ = seasonal_naive_predict(df, self._make_inp())
        self.assertGreater(preds, 0)

    def test_empty_df_returns_zeros(self):
        df = pd.DataFrame(
            columns=[
                "category",
                "day_of_week",
                "time_window",
                "observed_reservations",
                "observed_no_show",
                "unreserved_stock",
                "record_id",
            ]
        )
        preds, no_show = seasonal_naive_predict(df, self._make_inp())
        self.assertEqual(preds, 0.0)
        self.assertEqual(no_show, 0.0)


class MovingAveragePredictTests(unittest.TestCase):
    def _make_inp(self, **kwargs):
        base = {
            "category": "veg_box",
            "day_of_week": 2,
            "time_window": "18:00-19:00",
            "no_bundles": 10,
            "weather_flag": 0,
            "price": None,
        }
        base.update(kwargs)
        return base

    def test_uses_last_window_records(self):
        # 15 rows; the last 10 all have 100% reservation rate
        old_rows = [
            {"observed_reservations": 5, "unreserved_stock": 5, "observed_no_show": 0}
        ] * 5
        new_rows = [
            {"observed_reservations": 10, "unreserved_stock": 0, "observed_no_show": 0}
        ] * 10
        df = _make_df(old_rows + new_rows)
        preds, _ = moving_average_predict(df, self._make_inp(), window=10)
        self.assertAlmostEqual(preds, 10.0)

    def test_empty_df_returns_zeros(self):
        df = pd.DataFrame(
            columns=[
                "category",
                "day_of_week",
                "time_window",
                "observed_reservations",
                "observed_no_show",
                "unreserved_stock",
                "record_id",
            ]
        )
        preds, no_show = moving_average_predict(df, self._make_inp())
        self.assertEqual(preds, 0.0)


class SimilarityPredictTests(unittest.TestCase):
    def _make_inp(self, **kwargs):
        base = {
            "category": "veg_box",
            "day_of_week": 2,
            "time_window": "18:00-19:00",
            "no_bundles": 10,
            "weather_flag": 0,
            "price": None,
        }
        base.update(kwargs)
        return base

    def test_basic_prediction(self):
        df = _make_df(
            [
                {
                    "day_of_week": 2,
                    "time_window": "18:00-19:00",
                    "observed_reservations": 8,
                    "unreserved_stock": 2,
                    "observed_no_show": 0,
                    "weather_flag": 0,
                },
            ]
        )
        preds, _ = similarity_predict(df, self._make_inp())
        self.assertAlmostEqual(preds, 8.0)

    def test_price_sensitivity_lowers_prediction_for_high_price(self):
        # avg historical price = 5.0; posting at 10.0 should reduce predicted reservations
        df = _make_df(
            [
                {
                    "price": 5.0,
                    "day_of_week": 2,
                    "time_window": "18:00-19:00",
                    "observed_reservations": 8,
                    "unreserved_stock": 2,
                    "observed_no_show": 0,
                },
            ]
        )
        preds_normal, _ = similarity_predict(df, self._make_inp(price=5.0))
        preds_expensive, _ = similarity_predict(df, self._make_inp(price=10.0))
        self.assertLessEqual(preds_expensive, preds_normal)

    def test_weather_weighting(self):
        # Weather match should weight those records more heavily
        df = _make_df(
            [
                {
                    "weather_flag": 1,
                    "observed_reservations": 2,
                    "unreserved_stock": 8,
                    "observed_no_show": 0,
                },  # bad weather → low uptake
                {
                    "weather_flag": 0,
                    "observed_reservations": 9,
                    "unreserved_stock": 1,
                    "observed_no_show": 0,
                },  # good weather → high uptake
            ]
        )
        # Request is good-weather → prediction should lean towards high uptake
        preds_good, _ = similarity_predict(df, self._make_inp(weather_flag=0))
        preds_bad, _ = similarity_predict(df, self._make_inp(weather_flag=1))
        self.assertGreater(preds_good, preds_bad)

    def test_empty_subset_returns_zeros(self):
        df = _make_df([{"category": "sushi"}])
        preds, ns = similarity_predict(df, self._make_inp(category="unknown_cat"))
        self.assertEqual(preds, 0.0)
        self.assertEqual(ns, 0.0)


# ── unit tests – evaluate_baselines ──────────────────────────────────────────


class EvaluateBaselinesTests(unittest.TestCase):
    def test_returns_all_three_approaches(self):
        df = _make_df(
            [
                {
                    "observed_reservations": 8,
                    "unreserved_stock": 2,
                    "observed_no_show": 0,
                },
                {
                    "observed_reservations": 7,
                    "unreserved_stock": 3,
                    "observed_no_show": 1,
                },
                {
                    "observed_reservations": 6,
                    "unreserved_stock": 4,
                    "observed_no_show": 0,
                },
            ]
        )
        result = evaluate_baselines(df)
        for approach in ("seasonal_naive", "moving_average", "similarity"):
            self.assertIn(approach, result)

    def test_metrics_have_mae_rmse_n(self):
        df = _make_df(
            [
                {
                    "observed_reservations": 8,
                    "unreserved_stock": 2,
                    "observed_no_show": 0,
                },
                {
                    "observed_reservations": 7,
                    "unreserved_stock": 3,
                    "observed_no_show": 1,
                },
            ]
        )
        result = evaluate_baselines(df)
        for m in result.values():
            self.assertIn("mae", m)
            self.assertIn("rmse", m)
            self.assertIn("n", m)

    def test_rmse_is_non_negative(self):
        df = _make_df(
            [
                {
                    "observed_reservations": 8,
                    "unreserved_stock": 2,
                    "observed_no_show": 1,
                },
            ]
            * 5
        )
        result = evaluate_baselines(df)
        for m in result.values():
            if m["rmse"] is not None:
                self.assertGreaterEqual(m["rmse"], 0)

    def test_single_row_returns_n_zero(self):
        # LOO with 1 row → train is always empty → n=0
        df = _make_df(
            [{"observed_reservations": 8, "unreserved_stock": 2, "observed_no_show": 0}]
        )
        result = evaluate_baselines(df)
        for m in result.values():
            self.assertEqual(m["n"], 0)


# ── unit tests – confidence ───────────────────────────────────────────────────


class ConfidenceLevelTests(unittest.TestCase):
    def test_fewer_than_5_records_is_low(self):
        self.assertEqual(get_confidence_level(4, 1.0), "low")

    def test_high_rmse_is_low(self):
        self.assertEqual(get_confidence_level(20, 6.0), "low")

    def test_20_records_low_rmse_is_high(self):
        self.assertEqual(get_confidence_level(20, 1.5), "high")

    def test_medium_band(self):
        self.assertEqual(get_confidence_level(10, 3.0), "medium")


# ── unit tests – recommendation ───────────────────────────────────────────────


class GenerateRecommendationTests(unittest.TestCase):
    def _make_inp(self, no_bundles=12, weather_flag=0, price=None):
        return {
            "category": "veg_box",
            "day_of_week": 2,
            "time_window": "18:00-19:00",
            "no_bundles": no_bundles,
            "weather_flag": weather_flag,
            "price": price,
        }

    def test_returns_action_and_rationale(self):
        rec = generate_recommendation(
            self._make_inp(), predicted_reservations=8.0, no_show_prob=0.1, n_records=10
        )
        self.assertIn("action", rec)
        self.assertIn("rationale", rec)

    def test_recommends_reduction_when_low_fill_rate(self):
        # 5 expected from 12 posted = 42% fill rate → should suggest fewer
        rec = generate_recommendation(
            self._make_inp(no_bundles=12),
            predicted_reservations=5.0,
            no_show_prob=0.05,
            n_records=20,
        )
        self.assertIn("instead of", rec["action"].lower())

    def test_no_reduction_when_fill_rate_high(self):
        # 11 expected from 12 = 92% fill rate → should say quantity is appropriate
        rec = generate_recommendation(
            self._make_inp(no_bundles=12),
            predicted_reservations=11.0,
            no_show_prob=0.05,
            n_records=20,
        )
        self.assertNotIn("instead of", rec["action"].lower())

    def test_elevated_no_show_mentioned_in_rationale(self):
        rec = generate_recommendation(
            self._make_inp(),
            predicted_reservations=9.0,
            no_show_prob=0.35,
            n_records=15,
        )
        self.assertIn("no-show", rec["rationale"].lower())

    def test_weather_flag_mentioned_in_rationale(self):
        rec = generate_recommendation(
            self._make_inp(weather_flag=1),
            predicted_reservations=9.0,
            no_show_prob=0.1,
            n_records=15,
        )
        self.assertIn("weather", rec["rationale"].lower())

    def test_price_mentioned_when_provided(self):
        rec = generate_recommendation(
            self._make_inp(price=4.50),
            predicted_reservations=9.0,
            no_show_prob=0.1,
            n_records=15,
        )
        self.assertIn("4.50", rec["rationale"])
