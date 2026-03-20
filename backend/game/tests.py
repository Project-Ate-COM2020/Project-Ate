from django.db.models.aggregates import Max
from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from decimal import Decimal

from authentication.tests import (
    setup_consumer,
    setup_random_consumer,
    setup_random_seller,
    get_authorization_headers_for_user,
)
from core.models import Consumer, Seller, BundlePosting, Reservation


class BaseAuthenticatedTest(APITestCase):

    def setUp(self):
        pass

        self.headers = get_authorization_headers_for_user(self.user)


class GameSummaryViewTests(BaseAuthenticatedTest):

    def create_posting(self, category, quantity):
        return BundlePosting.objects.create(
            seller=self.seller,
            category=category,
            quantity=quantity,
            quantity_remaining=quantity,
            price=Decimal("10.00"),
            pickup_window="9:00-17:00",
            status="active",
        )

    def create_reservation(self, posting, code, status="collected"):
        return Reservation.objects.create(
            posting=posting,
            consumer=self.consumer,
            claim_code=code,
            status=status,
            collected_at=timezone.now() if status == "collected" else None,
        )

    def test_summary_calculates_correct_values(self):
        posting1 = self.create_posting("Hot Meals", 2)
        posting2 = self.create_posting("Fresh Produce", 4)

        # Pass explicit hardcoded claim codes
        self.create_reservation(posting1, "XB9YO1")
        self.create_reservation(posting2, "AB12CD")

        response = self.client.get(reverse("game-summary"), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # CO2 calculation
        # Hot Meals: 2.5 * 2 = 5
        # Fresh Produce: 0.5 * 4 = 2
        # Total = 7
        self.assertEqual(response.data["current_streak_weeks"], 5)
        self.assertEqual(response.data["total_rescued_bundles"], 2)
        self.assertEqual(response.data["estimated_co2e_saved_kg"], 7.0)

    def test_ignores_non_collected(self):
        posting = self.create_posting("Hot Meals", 2)
        self.create_reservation(posting, "FOOD99", status="reserved")

        response = self.client.get(reverse("game-summary"))

        self.assertEqual(response.data["total_rescued_bundles"], 0)
        self.assertEqual(response.data["estimated_co2e_saved_kg"], 0)


class RecentRescuesViewTests(BaseAuthenticatedTest):

    def create_posting(self):
        return BundlePosting.objects.create(
            seller=self.seller,
            category="Bakery",
            quantity=1,
            quantity_remaining=1,
            price=Decimal("5.00"),
            pickup_window="9:00-17:00",
            status="active",
        )

    def create_reservation(self, posting, code):
        return Reservation.objects.create(
            posting=posting,
            consumer=self.consumer,
            claim_code=code,
            status="collected",
            collected_at=timezone.now(),
        )

    def test_default_limit_is_10(self):
        posting = self.create_posting()

        claim_codes = [
            "CODE01",
            "CODE02",
            "CODE03",
            "CODE04",
            "CODE05",
            "CODE06",
            "CODE07",
            "CODE08",
            "CODE09",
            "CODE10",
            "CODE11",
        ]

        for code in claim_codes:
            self.create_reservation(posting, code)

        response = self.client.get(reverse("game-recent"), headers=self.headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 10)


class GameSummaryBadgeTests(BaseAuthenticatedTest):

    def create_posting(self, category, quantity):
        return BundlePosting.objects.create(
            seller=self.seller,
            category=category,
            quantity=quantity,
            quantity_remaining=quantity,
            price=Decimal("10.00"),
            pickup_window="9:00-17:00",
            status="active",
        )

    def create_reservation(self, posting, code, status="collected"):
        return Reservation.objects.create(
            posting=posting,
            consumer=self.consumer,
            claim_code=code,
            status=status,
            collected_at=timezone.now() if status == "collected" else None,
        )

    def test_variety_badges(self):
        # 1 unique categories  should not earn any badges
        posting = self.create_posting("Hot Meals", 1)
        self.create_reservation(posting, "HOT100")

        response = self.client.get(reverse("game-summary"), headers=self.headers)

        self.assertNotIn("Explorer", response.data["badges"])
        self.assertNotIn("Discoverer", response.data["badges"])
        self.assertNotIn("Adventurer", response.data["badges"])
        self.assertNotIn("Master", response.data["badges"])

        # add 1 more category - should earn Explorer
        posting = self.create_posting("Fresh Produce", 1)
        self.create_reservation(posting, "FRESH100")

        response = self.client.get(reverse("game-summary"), headers=self.headers)
        self.assertIn("Explorer", response.data["badges"])
        self.assertNotIn("Discoverer", response.data["badges"])
        self.assertNotIn("Adventurer", response.data["badges"])
        self.assertNotIn("Master", response.data["badges"])

        # add 1 more category - should earn Discoverer
        posting = self.create_posting("Bakery", 1)
        self.create_reservation(posting, "BAKERY10")

        response = self.client.get(reverse("game-summary"), headers=self.headers)
        self.assertIn("Explorer", response.data["badges"])
        self.assertIn("Discoverer", response.data["badges"])
        self.assertNotIn("Adventurer", response.data["badges"])
        self.assertNotIn("Master", response.data["badges"])

        # add 1 more category - should earn Adventurer
        posting = self.create_posting("Dairy", 1)
        self.create_reservation(posting, "DAIRY100")

        response = self.client.get(reverse("game-summary"))
        self.assertIn("Explorer", response.data["badges"])
        self.assertIn("Discoverer", response.data["badges"])
        self.assertIn("Adventurer", response.data["badges"])
        self.assertNotIn("Master", response.data["badges"])

        # add 2 more categories - should earn Master
        categories = ["Prepared Salads", "Desserts"]
        for i, cat in enumerate(categories):
            posting = self.create_posting(cat, 1)
            self.create_reservation(posting, f"CODE{i}")

        response = self.client.get(reverse("game-summary"))
        self.assertIn("Explorer", response.data["badges"])
        self.assertIn("Discoverer", response.data["badges"])
        self.assertIn("Adventurer", response.data["badges"])
        self.assertIn("Master", response.data["badges"])

    def test_impact_badges(self):
        # Total CO2 < 100 - no badges
        posting = self.create_posting("Hot Meals", 1)  # CO2 = 2.5
        self.create_reservation(posting, "IMPACT1")
        response = self.client.get(reverse("game-summary"))
        self.assertNotIn("Eco Starter", response.data["badges"])
        self.assertNotIn("Eco Friend", response.data["badges"])
        self.assertNotIn("Climate Hero", response.data["badges"])
        self.assertNotIn("Planet Saver", response.data["badges"])

        # Total CO2 >= 100 - earns Eco Starter
        posting = self.create_posting("Hot Meals", 50)  # 50 * 2.5 = 125
        self.create_reservation(posting, "IMPACT125")
        response = self.client.get(reverse("game-summary"))
        self.assertIn("Eco Starter", response.data["badges"])
        self.assertNotIn("Eco Friend", response.data["badges"])
        self.assertNotIn("Climate Hero", response.data["badges"])
        self.assertNotIn("Planet Saver", response.data["badges"])

        # Total CO2 >= 500 - earns Eco Friend
        posting = self.create_posting("Hot Meals", 200)  # 200 * 2.5 = 500
        self.create_reservation(posting, "IMPACT500")
        response = self.client.get(reverse("game-summary"))
        self.assertIn("Eco Starter", response.data["badges"])
        self.assertIn("Eco Friend", response.data["badges"])
        self.assertNotIn("Climate Hero", response.data["badges"])
        self.assertNotIn("Planet Saver", response.data["badges"])

        # Total CO2 >= 1000 - earns Climate Friend
        posting = self.create_posting("Hot Meals", 201)  # 201 * 2.5 = 502.5
        self.create_reservation(posting, "IMPACT502")
        response = self.client.get(reverse("game-summary"))
        self.assertIn("Eco Starter", response.data["badges"])
        self.assertIn("Eco Friend", response.data["badges"])
        self.assertIn("Climate Hero", response.data["badges"])
        self.assertNotIn("Planet Saver", response.data["badges"])

        # Total CO2 >= 10000 - earns Planet Saver
        posting = self.create_posting("Hot Meals", 4000)  # 4000 * 2.5 = 10000
        self.create_reservation(posting, "IMPACT10000")
        response = self.client.get(reverse("game-summary"))
        self.assertIn("Eco Starter", response.data["badges"])
        self.assertIn("Eco Friend", response.data["badges"])
        self.assertIn("Climate Hero", response.data["badges"])
        self.assertIn("Planet Saver", response.data["badges"])
