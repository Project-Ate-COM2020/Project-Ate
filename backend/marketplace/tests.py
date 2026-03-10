from argon2 import PasswordHasher
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate
from django.urls import reverse

from .models import Seller, Consumer, Reservation, BundlePosting
from .views import (
    CreateBundleView,
    CreateSellerView,
    CreateReservationView,
    CreateConsumerView,
    ConsumerView,
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

        self.assertEqual(BundlePosting.objects.count(), 1)

    def test_bundle_data_integrity(self):
        bundle = BundlePosting.objects.get(id=self.bundle_id)

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

        self.creation_response = self.client.post(url, seller_data, format="json")

        self.seller_id = self.creation_response.json()["id"]

    def test_creation_success(self):
        self.assertEqual(Seller.objects.count(), 1)

        self.assertEqual(self.creation_response.status_code, status.HTTP_201_CREATED)

    def test_data_integrity(self):
        seller = Seller.objects.get(id=self.seller_id)

        self.assertEqual(seller.name, "lauren")
        self.assertEqual(seller.location, "CF54BB")
        self.assertEqual(seller.opening_hours, "00:00-24:00")
        self.assertEqual(seller.contact_stub, "9874325655")


class CreateReservationViewsTests(APITestCase):
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

        consumer_url = reverse(CreateConsumerView.name)

        consumer_data = {
            "display_name": "name",
            "password": "pass",
            "streak": 7,
            "badges": "Badge",
        }

        self.consumer_creation_response = self.client.post(
            consumer_url, consumer_data, format="json"
        )

        self.consumer_id = self.consumer_creation_response.json()["id"]

        reservation_url = reverse(CreateReservationView.name)

        reservation_data = {
            "bundle": int(self.bundle_id),
            "consumer": int(self.consumer_id),
            "claim_code": "XXXXXX",
            "status": 7,
        }

        self.reservation_creation_response = self.client.post(
            reservation_url, reservation_data, format="json"
        )

        self.reservation_id = self.reservation_creation_response.json()["id"]

    def test_creation_success(self):
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(
            self.reservation_creation_response.status_code, status.HTTP_201_CREATED
        )

    def test_data_integrity(self):
        reservation = Reservation.objects.get(id=self.reservation_id)

        self.assertEqual(reservation.bundle.id, self.bundle_id)
        self.assertEqual(reservation.consumer.id, self.consumer_id)
        self.assertEqual(reservation.claim_code, "XXXXXX")
        self.assertEqual(reservation.status, 7)


class CreateConsumerViewTests(APITestCase):
    def setUp(self):
        consumer_url = reverse(CreateConsumerView.name)

        consumer_data = {
            "display_name": "name",
            "password": "pass",
            "streak": 7,
            "badges": "Badge",
        }

        self.consumer_creation_response = self.client.post(
            consumer_url, consumer_data, format="json"
        )

        self.consumer_id = self.consumer_creation_response.json()["id"]

        pass

    def test_creation_success(self):
        self.assertEqual(Consumer.objects.count(), 1)
        self.assertEqual(
            self.consumer_creation_response.status_code, status.HTTP_201_CREATED
        )

    def test_data_integrity(self):
        consumer = Consumer.objects.get(id=self.consumer_id)

        self.assertEqual(consumer.display_name, "name")
        self.assertEqual(consumer.streak, 7)
        self.assertEqual(consumer.badges, "Badge")


class ConsumerPasswordHashingTests(APITestCase):
    def setUp(self):
        consumer_url = reverse(CreateConsumerView.name)

        consumer_data = {
            "display_name": "name",
            "password": "pass",
            "streak": 7,
            "badges": "Badge",
        }

        self.consumer_creation_response = self.client.post(
            consumer_url, consumer_data, format="json"
        )

        self.consumer_id = self.consumer_creation_response.json()["id"]

    def test_password_got_hashed(self):
        consumer = Consumer.objects.get(id=self.consumer_id)

        self.assertNotEqual(consumer.password, "pass")


class SellerPasswordHashingTests(APITestCase):
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

    def test_password_got_hashed(self):
        seller = Seller.objects.get(id=self.seller_id)

        self.assertNotEqual(seller.password, "pass")
