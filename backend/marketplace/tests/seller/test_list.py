from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import (
    setup_random_reservation,
    get_authorization_headers_for_user,
    setup_random_reservation_for_seller,
)
from marketplace.views import ListReservationView


class ListReservationViewsTests(APITestCase):
    def setUp(self):
        self.url = reverse(ListReservationView.name)

    def test_list_reservation_doesnt_leak(self):
        (user1, consumer1), (seller_user, seller), bundle1, reservation1 = (
            setup_random_reservation()
        )

        user1_headers = get_authorization_headers_for_user(user1)

        user2, consumer2, bundle2, reservation2 = setup_random_reservation_for_seller(
            seller
        )

        user2_headers = get_authorization_headers_for_user(user2)

        seller_headers = get_authorization_headers_for_user(seller_user)

        # test user1 gets their reservations

        response = self.client.get(self.url, format="json", headers=user1_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        # check length matched
        # check pk matches
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["reservation_id"], reservation1.pk)

        # check user2 gets their reservations
        response = self.client.get(self.url, format="json", headers=user2_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(len(response), 1)
        self.assertEqual(response[0]["reservation_id"], reservation2.pk)

        # check seller gets both
        response = self.client.get(self.url, format="json", headers=seller_headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["reservation_id"], reservation1.pk)
        self.assertEqual(response[1]["reservation_id"], reservation2.pk)
