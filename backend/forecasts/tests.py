from django.urls import reverse
from rest_framework.test import APITestCase
from unittest.mock import patch
import unittest
import pandas as pd

from core.models import ForecastInput, Seller
from forecasts.forecasting import (
    get_adjacent_days,
    get_adjacent_time_slots,
    get_no_show_probability,
    get_expected_no_show_count,
    get_expected_reservations,
)

class ForecastPredictionViewTests(APITestCase):
    def setUp(self):
        self.url = reverse("forecast-prediction")

        self.seller = Seller.objects.create(
            name="Seller One",
            location="Test Location",
            opening_hours="09:00-17:00",
            contact_stub="seller1@example.com",
        )

        self.valid_payload = {
            "seller_id": self.seller.seller_id,     # API expects seller_id in request payload
            "category": "veg_box",
            "day_of_week": 2,
            "time_window": "18:00-20:00",
            "weather": 1,
            "no_bundles": 2,                 # API accepts this, not stored on model
        }

    def _create_forecast_input_row(self):
        # Create 1 record so df isn't empty
        return ForecastInput.objects.create(
            day_of_week=2,
            time_window="18:00-20:00",
            seller=self.seller,
            category="veg_box",
            price=5.00,
            weather_flag=1,
            observed_reservations=8,
            observed_no_show=1,
            unreserved_stock=3,
        )

    def test_missing_required_params_returns_400(self):
        resp = self.client.post(self.url, {"category": "veg_box"}, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.data)

    def test_no_data_available_returns_400(self):
        resp = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.data.get("error"), "No data available")

    @patch("forecasts.views.get_similar_listings")
    def test_no_matching_listings_returns_404(self, mock_get_similar_listings):
        self._create_forecast_input_row()

        mock_get_similar_listings.return_value = pd.DataFrame()  # empty subset

        resp = self.client.post(self.url, self.valid_payload, format="json")
        self.assertEqual(resp.status_code, 404)
        self.assertEqual(resp.data.get("error"), "No matching listings found")

    @patch("forecasts.views.calculate_recommended_price")
    @patch("forecasts.views.get_expected_reservations")
    @patch("forecasts.views.get_expected_no_show_count")
    @patch("forecasts.views.get_similar_listings")
    def test_happy_path_returns_forecast_values(
        self,
        mock_get_similar_listings,
        mock_no_show,
        mock_reservations,
        mock_price,
    ):
        self._create_forecast_input_row()

        mock_get_similar_listings.return_value = pd.DataFrame([{"dummy": 1}])
        mock_no_show.return_value = 3
        mock_reservations.return_value = 10
        mock_price.return_value = 7.50

        resp = self.client.post(self.url, self.valid_payload, format="json")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["expected_no_show_count"], 3)
        self.assertEqual(resp.data["expected_reservations"], 10)
        self.assertEqual(resp.data["recommended_price"], 7.50)


class AdjacentDaysTests(unittest.TestCase):
    def test_get_adjacent_days_monday(self):
        """Day 1 (Monday) should return [7, 1, 2]"""
        result = get_adjacent_days(1)
        self.assertEqual(result, [7, 1, 2])


class AdjacentTimeSlotsTests(unittest.TestCase):
    def test_get_adjacent_time_slots_hourly(self):
        """Test hourly time slots"""
        result = get_adjacent_time_slots("10:00-11:00")
        self.assertEqual(result, ["09:00-10:00", "10:00-11:00", "11:00-12:00"])

class NoShowProbabilityTests(unittest.TestCase):
    def test_get_no_show_probability_empty_subset(self):
        """Empty subset should return 0.0"""
        df = pd.DataFrame()
        result = get_no_show_probability(df)
        self.assertEqual(result, 0.0)

    def test_get_no_show_probability_no_shows(self):
        """Calculate no-show probability correctly"""
        df = pd.DataFrame({
            "observed_no_show": [2, 3],
            "observed_reservations": [10, 15],
        })
        # (2 + 3) / (10 + 15) = 5 / 25 = 0.2
        result = get_no_show_probability(df)
        self.assertEqual(result, 0.2)


class ExpectedNoShowCountTests(unittest.TestCase):
    def test_get_expected_no_show_count_calculation(self):
        """Expected no-show count = no_show_probability * no_bundles"""
        df = pd.DataFrame({
            "observed_no_show": [2],
            "observed_reservations": [10],
        })
        inp = {"no_bundles": 5}
        # no_show_prob = 2/10 = 0.2, result = 0.2 * 5 = 1.0
        result = get_expected_no_show_count(df, inp)
        self.assertEqual(result, 1.0)


class ExpectedReservationsTests(unittest.TestCase):
    def test_get_expected_reservations_calculation(self):
        """Reservation rate = observed_reservations / total_stock * no_bundles"""
        df = pd.DataFrame({
            "observed_reservations": [8],
            "unreserved_stock": [2],
            "observed_no_show": [0],
        })
        inp = {"no_bundles": 10}
        # total_stock = 8 + 2 + 0 = 10
        # rate = 8/10 = 0.8, result = 0.8 * 10 = 8.0
        result = get_expected_reservations(df, inp)
        self.assertEqual(result, 8.0)
