from rest_framework.test import APITestCase, APIRequestFactory

from core.models import BundlePosting, Consumer, Reservation, Seller
from buyer.views import (
    MarkReservationAsReserveredView,
    MarkReservationAsUnreservedView,
)


class BuyerReservationTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.seller = Seller.objects.create(
            name="Test Seller",
            location="Test Location",
            opening_hours="09:00-17:00",
            contact_stub="seller@example.com",
        )
        self.consumer = Consumer.objects.create(display_name="Test Buyer")
        self.posting = BundlePosting.objects.create(
            seller=self.seller,
            category="veg_box",
            contents="mixed",
            allergens="none",
            quantity=5,
            quantity_remaining=3,
            price=5.00,
            pickup_window="18:00-20:00",
            status="active",
        )

    def _create_reservation(self, status="reserved"):
        return Reservation.objects.create(
            posting=self.posting,
            consumer=self.consumer,
            claim_code="TEST123",
            status=status,
        )

    def test_mark_reservation_as_reserved_missing_id_returns_400(self):
        request = self.factory.post("/buyer/reservebundle/", {}, format="json")
        response = MarkReservationAsReserveredView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get("error"), "reservation_id is required")

    def test_mark_reservation_as_reserved_not_found_returns_404(self):
        request = self.factory.post("/buyer/reservebundle/", {"reservation_id": 9999}, format="json")
        response = MarkReservationAsReserveredView.as_view()(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get("error"), "Reservation not found")

    def test_mark_reservation_as_reserved_success(self):
        reservation = self._create_reservation(status="expired")
        request = self.factory.post(
            "/buyer/reservebundle/",
            {"reservation_id": reservation.reservation_id},
            format="json"
        )
        response = MarkReservationAsReserveredView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Reservation marked as reserved")
        
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, "reserved")

    def test_mark_reservation_as_unreserved_missing_id_returns_400(self):
        request = self.factory.post("/buyer/unreservebundle/", {}, format="json")
        response = MarkReservationAsUnreservedView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get("error"), "reservation_id is required")

    def test_mark_reservation_as_unreserved_not_found_returns_404(self):
        request = self.factory.post("/buyer/unreservebundle/", {"reservation_id": 9999}, format="json")
        response = MarkReservationAsUnreservedView.as_view()(request)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.get("error"), "Reservation not found")

    def test_mark_reservation_as_unreserved_success_deletes(self):
        reservation = self._create_reservation()
        reservation_id = reservation.reservation_id
        
        request = self.factory.post(
            "/buyer/unreservebundle/",
            {"reservation_id": reservation_id},
            format="json"
        )
        response = MarkReservationAsUnreservedView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("message"), "Reservation deleted")
        
        # Verify deletion
        self.assertFalse(Reservation.objects.filter(reservation_id=reservation_id).exists())
