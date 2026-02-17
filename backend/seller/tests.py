from decimal import Decimal
from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase, APIRequestFactory

from core.models import BundlePosting, Consumer, Reservation, Seller
from seller.views import (
	AddNewListingView,
	SellerAddressView,
	SellerNameView,
	SellerReservationsView,
)


class SellerViewTests(APITestCase):
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

	def _create_posting(self, seller, price=Decimal("5.00")):
		return BundlePosting.objects.create(
			seller=seller,
			category="veg_box",
			contents="mixed",
			allergens="none",
			quantity=5,
			quantity_remaining=3,
			price=price,
			pickup_window="18:00-20:00",
			status="active",
		)

	def _create_reservation(self, posting, status, timestamp):
		claim_code = f"code-{self._claim_seq}"
		self._claim_seq += 1
		reservation = Reservation.objects.create(
			posting=posting,
			consumer=self.consumer,
			claim_code=claim_code,
			status=status,
		)
		reservation.timestamp = timestamp
		reservation.save(update_fields=["timestamp"])
		return reservation

	def test_seller_name_missing_seller_id_returns_400(self):
		request = self.factory.get("/seller/getsellername/")
		response = SellerNameView.as_view()(request)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.get("error"), "seller_id query parameter is required")

	def test_seller_name_not_found_returns_404(self):
		request = self.factory.get("/seller/getsellername/", {"seller_id": 9999})
		response = SellerNameView.as_view()(request)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data.get("error"), "Seller not found")

	def test_seller_name_returns_value(self):
		request = self.factory.get("/seller/getsellername/", {"seller_id": self.seller.seller_id})
		response = SellerNameView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, "Seller One")

	def test_seller_address_returns_value(self):
		request = self.factory.get("/seller/getselleraddress/", {"seller_id": self.seller.seller_id})
		response = SellerAddressView.as_view()(request)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, "Test Location")

	def test_seller_reservations_missing_seller_id_returns_400(self):
		request = self.factory.get("/seller/getreservations/")
		response = SellerReservationsView.as_view()(request)
		self.assertEqual(response.status_code, 400)
		self.assertEqual(response.data.get("error"), "seller_id query parameter is required")

	def test_seller_reservations_seller_not_found_returns_404(self):
		request = self.factory.get("/seller/getreservations/", {"seller_id": 9999})
		response = SellerReservationsView.as_view()(request)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data.get("error"), "Seller not found")

	def test_seller_reservations_returns_collected_and_upcoming(self):
		posting = self._create_posting(self.seller)
		other_posting = self._create_posting(self.other_seller)

		now = timezone.now()
		# collected (only last one should return)
		self._create_reservation(posting, "collected", now - timedelta(days=2))
		latest_collected = self._create_reservation(posting, "collected", now - timedelta(days=1))

		# upcoming (only next 4 should return)
		upcoming_times = [now + timedelta(hours=i) for i in range(1, 6)]
		for ts in upcoming_times:
			self._create_reservation(posting, "reserved", ts)

		# other seller should be ignored
		self._create_reservation(other_posting, "reserved", now + timedelta(hours=1))

		request = self.factory.get("/seller/getreservations/", {"seller_id": self.seller.seller_id})
		response = SellerReservationsView.as_view()(request)
		self.assertEqual(response.status_code, 200)

		collected = response.data.get("collected_reservations")
		upcoming = response.data.get("upcoming_reservations")

		self.assertEqual(len(collected), 1)
		self.assertEqual(collected[0]["reservation_id"], latest_collected.reservation_id)
		self.assertEqual(len(upcoming), 4)
		self.assertEqual(upcoming[0]["reservation_time"], upcoming_times[0])

	def test_add_new_listing_missing_fields_returns_400(self):
		request = self.factory.post("/seller/createlisting/", {"seller_id": self.seller.seller_id}, format="json")
		response = AddNewListingView.as_view()(request)
		self.assertEqual(response.status_code, 400)
		self.assertIn("error", response.data)

	def test_add_new_listing_seller_not_found_returns_404(self):
		payload = {
			"seller_id": 9999,
			"category": "veg_box",
			"contents": "mixed",
			"allergens": "none",
			"quantity": 5,
			"price": "5.00",
			"pickup_window": "18:00-20:00",
		}
		request = self.factory.post("/seller/createlisting/", payload, format="json")
		response = AddNewListingView.as_view()(request)
		self.assertEqual(response.status_code, 404)
		self.assertEqual(response.data.get("error"), "Seller not found")

	def test_add_new_listing_success_returns_201(self):
		payload = {
			"seller_id": self.seller.seller_id,
			"category": "veg_box",
			"contents": "mixed",
			"allergens": "none",
			"quantity": 5,
			"price": "5.00",
			"pickup_window": "18:00-20:00",
		}
		request = self.factory.post("/seller/createlisting/", payload, format="json")
		response = AddNewListingView.as_view()(request)
		self.assertEqual(response.status_code, 201)
		self.assertEqual(response.data.get("message"), "New listing created")
		self.assertIn("posting_id", response.data)
