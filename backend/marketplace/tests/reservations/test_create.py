from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import (
    get_authorization_headers_for_user,
    setup_random_consumer,
    setup_random_seller, random_reservation_args, random_reservation_args_for_bundle,
)
from core.models import Reservation
from marketplace.views import CreateBundleView, CreateReservationView


class CreateReservationViewsTests(APITestCase):
    def setUp(self):
        self.consumer_user, self.consumer = setup_random_consumer()

        self.consumer_auth_headers = get_authorization_headers_for_user(
            self.consumer_user
        )

        self.seller_user, self.seller = setup_random_seller()

        self.seller_auth_headers = get_authorization_headers_for_user(self.seller_user)

        self.seller_id = self.seller.pk

        bundle_url = reverse(CreateBundleView.name)

        bundle_data = {
            "seller": int(self.seller_id),
            "category": "food",
            "contents": "A bagel",
            "quantity": 8,
            "quantity_remaining": 7,
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

        reservation_data = random_reservation_args_for_bundle(self.bundle_id)

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
        self.assertEqual(reservation.status, "reserved")
