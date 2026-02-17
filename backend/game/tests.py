from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from decimal import Decimal

from core.models import Consumer, Seller, BundlePosting, Reservation

class BaseAuthenticatedTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser")

        self.consumer = Consumer.objects.create(
            consumer_id=1,
            display_name="Test User",
            streak=5
        )

        self.user.consumer = self.consumer

        self.seller = Seller.objects.create(
            name="Test Seller",
            location="Test Location"
        )

        self.client.force_authenticate(user=self.user)


class GameSummaryViewTests(BaseAuthenticatedTest):

    def create_posting(self, category, quantity):
        return BundlePosting.objects.create(
            seller=self.seller,
            category=category,
            quantity=quantity,
            quantity_remaining=quantity,
            price=Decimal("10.00"),
            pickup_window="9:00-17:00",
            status="active"
        )

    def create_reservation(self, posting, code, status="collected"):
        return Reservation.objects.create(
            posting=posting,
            consumer=self.consumer,
            claim_code=code,
            status=status,
            collected_at=timezone.now() if status == "collected" else None
        )

    def test_summary_calculates_correct_values(self):
        posting1 = self.create_posting("Hot Meals", 2)
        posting2 = self.create_posting("Fresh Produce", 4)

        # Pass explicit hardcoded claim codes
        self.create_reservation(posting1, "XB9YO1")
        self.create_reservation(posting2, "AB12CD")

        response = self.client.get(reverse("game-summary"))

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
            status="active"
        )

    def create_reservation(self, posting, code):
        return Reservation.objects.create(
            posting=posting,
            consumer=self.consumer,
            claim_code=code,
            status="collected",
            collected_at=timezone.now()
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

        response = self.client.get(reverse("game-recent"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)
