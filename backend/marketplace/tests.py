from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import setup_random_seller, setup_random_user

from authentication.token import UserTokenObtainPairSerializer

from .models import Seller, Consumer, Reservation, BundlePosting
from .views import (
    CreateBundleView,
    CreateSellerView,
    CreateReservationView,
    CreateConsumerView,
)
from django.contrib.auth import get_user_model


def create_user_get_auth_headers(username, email, password):
    user_model = get_user_model()

    user = user_model.objects.create_user(
        username=username,
        email=email,
        password=password,
    )

    token = UserTokenObtainPairSerializer.get_token(user).access_token

    return user, {"AUTHORIZATION": f"Bearer {token}"}


def make_user_a_consumer(user, display_name):

    consumer = Consumer.objects.create(
        display_name=display_name,
        user=user,
    )

    token = UserTokenObtainPairSerializer.get_token(user).access_token

    return consumer, {"AUTHORIZATION": f"Bearer {token}"}


def make_user_a_seller(user, name, location, opening_hours, contact_stub):
    seller = Seller.objects.create(
        location=location,
        opening_hours=opening_hours,
        contact_stub=contact_stub,
        name=name,
        user=user,
    )

    token = UserTokenObtainPairSerializer.get_token(user).access_token

    return seller, {"AUTHORIZATION": f"Bearer {token}"}


# Create your tests here.
class CreateBundleViewsTests(APITestCase):
    def setUp(self):
        seller_url = reverse(CreateSellerView.name)

        self.seller_user, _ = create_user_get_auth_headers(
            username="test", email="test@test.com", password="password"
        )

        self.seller, self.seller_auth_headers = make_user_a_seller(
            user=self.seller_user,
            location="CF54BB",
            opening_hours="00:00-24:00",
            contact_stub="9874325655",
            name="lauren",
        )

        self.seller_id = self.seller.pk

        bundle_url = reverse(CreateBundleView.name)

        bundle_data = {
            "seller": int(self.seller_id),
            "category": "food",
            "contents": "A bagel",
            "quantity": 8,
            "price": 55,
            "pickup_window": "00:00-24:00",
            "status": "active",
        }

        self.bundle_creation_response = self.client.post(
            bundle_url, bundle_data, format="json", headers=self.seller_auth_headers
        )

        self.bundle_id = self.bundle_creation_response.json()["posting_id"]

    def test_creation_success(self):
        self.assertEqual(
            self.bundle_creation_response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(BundlePosting.objects.count(), 1)

    def test_bundle_data_integrity(self):
        bundle = BundlePosting.objects.get(posting_id=self.bundle_id)

        self.assertEqual(bundle.seller.pk, self.seller_id)
        self.assertEqual(bundle.category, "food")
        self.assertEqual(bundle.contents, "A bagel")
        self.assertEqual(bundle.quantity, 8)
        self.assertEqual(bundle.pickup_window, "00:00-24:00")
        self.assertEqual(bundle.status, "active")


class CreateSellerViewTests(APITestCase):
    def setUp(self):
        self.url = reverse(CreateSellerView.name)

        self.user, self.headers = create_user_get_auth_headers(
            "test", "test@test.com", "password"
        )

        self.seller_data = {
            "name": "lauren",
            "location": "CF54BB",
            "opening_hours": "00:00-24:00",
            "contact_stub": "9874325655",
        }

    def post_create_seller(self):
        self.creation_response = self.client.post(
            self.url, self.seller_data, format="json", headers=self.headers
        )

        return self.creation_response.json()["seller_id"]

    def test_creation_success(self):
        self.post_create_seller()

        self.assertEqual(Seller.objects.count(), 1)

        self.assertEqual(self.creation_response.status_code, status.HTTP_201_CREATED)

    def test_data_integrity(self):
        seller_id = self.post_create_seller()

        seller = Seller.objects.get(seller_id=seller_id)

        self.assertEqual(seller.name, self.seller_data["name"])
        self.assertEqual(seller.location, self.seller_data["location"])
        self.assertEqual(seller.opening_hours, self.seller_data["opening_hours"])
        self.assertEqual(seller.contact_stub, self.seller_data["contact_stub"])


class CreateReservationViewsTests(APITestCase):
    def setUp(self):
        self.consumer_user, _ = create_user_get_auth_headers(
            "test", "test@test.com", "password"
        )

        self.consumer, self.consumer_auth_headers = make_user_a_consumer(
            user=self.consumer_user, display_name="test"
        )

        self.seller_user, _ = create_user_get_auth_headers(
            "seller", "seller@seller.com", "password"
        )

        self.seller, self.seller_auth_headers = make_user_a_seller(
            user=self.seller_user,
            name="lauren",
            location="CF54BB",
            opening_hours="00:00-24:00",
            contact_stub="9874325655",
        )

        self.seller_id = self.seller.pk

        bundle_url = reverse(CreateBundleView.name)

        bundle_data = {
            "seller": int(self.seller_id),
            "category": "food",
            "contents": "A bagel",
            "quantity": 8,
            "price": 55,
            "pickup_window": "00:00-24:00",
            "status": "active",
        }

        self.bundle_creation_response = self.client.post(
            bundle_url, bundle_data, format="json", headers=self.seller_auth_headers
        )

        self.bundle_id = self.bundle_creation_response.json()["posting_id"]

        self.consumer_id = self.consumer.pk

        reservation_url = reverse(CreateReservationView.name)

        reservation_data = {
            "posting": int(self.bundle_id),
            "claim_code": "XXXXXX",
            "status": "collected",
        }

        self.reservation_creation_response = self.client.post(
            reservation_url,
            reservation_data,
            format="json",
            headers=self.consumer_auth_headers,
        )

        self.reservation_id = self.reservation_creation_response.json()[
            "reservation_id"
        ]

    def test_creation_success(self):
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(
            self.reservation_creation_response.status_code, status.HTTP_201_CREATED
        )

    def test_data_integrity(self):
        reservation = Reservation.objects.get(reservation_id=self.reservation_id)

        self.assertEqual(reservation.posting.pk, self.bundle_id)
        self.assertEqual(reservation.consumer.pk, self.consumer_id)
        self.assertEqual(reservation.claim_code, "XXXXXX")
        self.assertEqual(reservation.status, "collected")


class CreateConsumerViewTests(APITestCase):
    def setUp(self):
        consumer_url = reverse(CreateConsumerView.name)

        self.user, self.headers = create_user_get_auth_headers(
            "test", "test@test.com", "test"
        )

        consumer_data = {
            "display_name": "name",
            "streak": 7,
        }

        self.consumer_creation_response = self.client.post(
            consumer_url, consumer_data, format="json", headers=self.headers
        )

        self.consumer_id = self.consumer_creation_response.json()["consumer_id"]

    def test_creation_success(self):
        self.assertEqual(Consumer.objects.count(), 1)
        self.assertEqual(
            self.consumer_creation_response.status_code, status.HTTP_201_CREATED
        )

    def test_data_integrity(self):
        consumer = Consumer.objects.get(consumer_id=self.consumer_id)

        self.assertEqual(consumer.display_name, "name")
        self.assertEqual(consumer.streak, 7)


class PasswordHashingTests(APITestCase):
    def setUp(self):
        self.user, self.headers = create_user_get_auth_headers(
            "test", "test@test.com", "test"
        )

    def test_password_got_hashed(self):
        self.assertNotEqual(self.user.password, "test")
