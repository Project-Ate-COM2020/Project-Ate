from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import (
    get_authorization_headers_for_user,
    setup_random_reservation,
    setup_random_reservation_for_seller,
)
from marketplace.views import ReservationView


class RetrieveReservationsTests(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk):
        return reverse(ReservationView.name, kwargs={"pk": pk})

    def test_cannot_retrieve_nonexistent_reservation(self):
        (consumer_user, consumer), (seller_user, seller), bundle, reservation = (
            setup_random_reservation()
        )

        headers = get_authorization_headers_for_user(consumer_user)

        response = self.client.get(
            self.get_url(reservation.pk + 1), format="json", headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # test a consumer account can retrieve a list of their reservations but not any owned by another account
    def test_can_only_retrieve_own_reservations_consumer(self):
        (user1, consumer1), (seller_user, seller), bundle1, reservation1 = (
            setup_random_reservation()
        )

        user1_headers = get_authorization_headers_for_user(user1)

        user2, consumer2, bundle2, reservation2 = setup_random_reservation_for_seller(
            seller
        )

        # test user1 cannot access user2's reservation
        response = self.client.get(
            self.get_url(reservation2.pk), format="json", headers=user1_headers
        )

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        # test user1 can access their own reservation
        response = self.client.get(
            self.get_url(reservation1.pk), format="json", headers=user1_headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user2_headers = get_authorization_headers_for_user(user2)

        # test user2 can access their own reservation
        response = self.client.get(
            self.get_url(reservation2.pk), format="json", headers=user2_headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        seller_headers = get_authorization_headers_for_user(seller_user)

        # test seller can access both
        response = self.client.get(
            self.get_url(reservation1.pk), format="json", headers=seller_headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            self.get_url(reservation2.pk), format="json", headers=user2_headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
