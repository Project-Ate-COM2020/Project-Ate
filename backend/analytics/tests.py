from decimal import Decimal
from rest_framework.test import APITestCase, APIRequestFactory

from core.models import BundlePosting, Reservation, Seller, Consumer
from analytics.views import (
	TotalListingsView,
	TotalRevenueView,
	TotalReservationsView,
	FoodWasteReductionView,
	TotalNoShowsView,
)


class AnalyticsViewTests(APITestCase):
	def setUp(self):
		self.factory = APIRequestFactory()
		self.seller = Seller.objects.create(
			name="Seller One",
			location="Test Location",
			opening_hours="09:00-17:00",
			contact_stub="seller1@example.com",
		)
		self.other_seller = Seller.objects.create(
			name="Seller Two",
			location="Other Location",
			opening_hours="10:00-18:00",
			contact_stub="seller2@example.com",
		)
		self.consumer = Consumer.objects.create(display_name="Test Buyer")
		self._claim_seq = 1

	def _create_posting(self, seller, status="active", price=Decimal("5.00")):
		return BundlePosting.objects.create(
			seller=seller,
			category="veg_box",
			contents="mixed",
			allergens="none",
			quantity=5,
			quantity_remaining=3,
			price=price,
			pickup_window="18:00-20:00",
			status=status,
		)

	def _create_reservation(self, posting, status="reserved"):
		claim_code = f"code-{self._claim_seq}"
		self._claim_seq += 1
		return Reservation.objects.create(
			posting=posting,
			consumer=self.consumer,
			claim_code=claim_code,
			status=status,
		)

	def test_total_listings_empty_returns_400(self):
		request = self.factory.get("/analytics/total-listings/", {"seller_id": self.seller.seller_id})
		response = TotalListingsView.as_view()(request)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.get("error"), "No data available")

	def test_total_listings_returns_count(self):
		self._create_posting(self.seller)
		self._create_posting(self.seller)
		self._create_posting(self.other_seller)

		request = self.factory.get("/analytics/total-listings/", {"seller_id": self.seller.seller_id})
		response = TotalListingsView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, 2)

	def test_total_revenue_empty_returns_400(self):
		request = self.factory.get("/analytics/total-revenue/", {"seller_id": self.seller.seller_id})
		response = TotalRevenueView.as_view()(request)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.get("error"), "No data available")

	def test_total_revenue_counts_reserved_and_collected(self):
		posting_one = self._create_posting(self.seller, price=Decimal("5.00"))
		posting_two = self._create_posting(self.seller, price=Decimal("7.50"))
		posting_other = self._create_posting(self.other_seller, price=Decimal("9.00"))

		self._create_reservation(posting_one, status="reserved")
		self._create_reservation(posting_two, status="collected")
		self._create_reservation(posting_two, status="no-show")
		self._create_reservation(posting_other, status="reserved")

		request = self.factory.get("/analytics/total-revenue/", {"seller_id": self.seller.seller_id})
		response = TotalRevenueView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(Decimal(str(response.data)), Decimal("12.50"))

	def test_total_reservations_missing_seller_id_returns_400(self):
		request = self.factory.get("/analytics/total-reservations/")
		response = TotalReservationsView.as_view()(request)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.get("error"), "seller_id query parameter is required")

	def test_total_reservations_counts(self):
		posting_one = self._create_posting(self.seller)
		posting_two = self._create_posting(self.seller)
		posting_other = self._create_posting(self.other_seller)

		self._create_reservation(posting_one, status="reserved")
		self._create_reservation(posting_two, status="collected")
		self._create_reservation(posting_other, status="reserved")

		request = self.factory.get("/analytics/total-reservations/", {"seller_id": self.seller.seller_id})
		response = TotalReservationsView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.get("total_reservations"), 2)

	def test_food_waste_reduction_empty_returns_400(self):
		request = self.factory.get("/analytics/food-waste-reduction/", {"seller_id": self.seller.seller_id})
		response = FoodWasteReductionView.as_view()(request)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.get("error"), "No data available")

	def test_food_waste_reduction_percentage(self):
		self._create_posting(self.seller, status="collected")
		self._create_posting(self.seller, status="collected")
		self._create_posting(self.seller, status="active")
		self._create_posting(self.seller, status="active")
		self._create_posting(self.other_seller, status="collected")

		request = self.factory.get("/analytics/food-waste-reduction/", {"seller_id": self.seller.seller_id})
		response = FoodWasteReductionView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.get("food_waste_reduction_percentage"), 50.0)

	def test_total_no_shows_missing_seller_id_returns_400(self):
		request = self.factory.get("/analytics/total-no-shows/")
		response = TotalNoShowsView.as_view()(request)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.get("error"), "seller_id query parameter is required")

	def test_total_no_shows_counts(self):
		posting_one = self._create_posting(self.seller)
		posting_two = self._create_posting(self.seller)
		posting_other = self._create_posting(self.other_seller)

		self._create_reservation(posting_one, status="no-show")
		self._create_reservation(posting_two, status="no-show")
		self._create_reservation(posting_two, status="reserved")
		self._create_reservation(posting_other, status="no-show")

		request = self.factory.get("/analytics/total-no-shows/", {"seller_id": self.seller.seller_id})
		response = TotalNoShowsView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data.get("total_no_shows"), 2)
