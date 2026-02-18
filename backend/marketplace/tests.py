from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from .models import Seller, Consumer, Reservation, Bundle
from .views import (
    CreateBundleView,
    CreateSellerView,
    CreateReservationView,
    CreateConsumerView,
)


# Create your tests here.
class CreateBundleViewsTests(APITestCase):
    def setUp(self):
        seller_url = reverse(CreateSellerView.name)

        seller_data = {
            "name": "lauren",
            "location": "CF54BB",
            "password": "pass",
            "opening_hours": "00:00-24:00",
            "contact_stub": "9874325655",
        }

        self.seller_creation_response = self.client.post(
            seller_url, seller_data, format="json"
        )

        self.seller_id = self.seller_creation_response.json()["id"]

        bundle_url = reverse(CreateBundleView.name)

        bundle_data = {
            "seller": int(self.seller_id),
            "category": "food",
            "contents": "A bagel",
            "allergens": "lots",
            "quantity": 8,
            "price": 55,
            "pickup_window": "00:00-24:00",
            "status": 7,
        }

        self.bundle_creation_response = self.client.post(
            bundle_url, bundle_data, format="json"
        )

        self.bundle_id = self.bundle_creation_response.json()["id"]

    def test_creation_success(self):
        self.assertEqual(Seller.objects.count(), 1)

        self.assertEqual(
            self.seller_creation_response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(
            self.bundle_creation_response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(Bundle.objects.count(), 1)

    def test_bundle_data_integrity(self):
        bundle = Bundle.objects.get(id=self.bundle_id)

        self.assertEqual(bundle.seller.id, self.seller_id)
        self.assertEqual(bundle.category, "food")
        self.assertEqual(bundle.contents, "A bagel")
        self.assertEqual(bundle.allergens, "lots")
        self.assertEqual(bundle.quantity, 8)
        self.assertEqual(bundle.pickup_window, "00:00-24:00")
        self.assertEqual(bundle.status, 7)


class CreateSellerViewTests(APITestCase):
    def setUp(self):
        url = reverse(CreateSellerView.name)

        seller_data = {
            "name": "lauren",
            "location": "CF54BB",
            "password": "pass",
            "opening_hours": "00:00-24:00",
            "contact_stub": "9874325655",
        }

        pass


class CreateReservationViewsTests(APITestCase):
    def setUp(self):
        url = reverse(CreateReservationView.name)

        pass


class CreateConsumerViewTests(APITestCase):
    def setUp(self):
        url = reverse(CreateConsumerView.name)

        pass
