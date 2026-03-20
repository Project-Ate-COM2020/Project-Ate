from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.tests import (
    setup_random_seller,
    get_authorization_headers_for_user,
    setup_random_reservation,
    setup_random_reservation_for_consumer,
)
from marketplace.views import ListSellerView


class ListSellerViewTests(APITestCase):
    def setUp(self):
        self.url = reverse(ListSellerView.name)

    def test_can_list_self(self):
        user, seller = setup_random_seller()

        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(len(response), 1)

    def test_does_not_list_other_users(self):
        user, seller = setup_random_seller()

        headers = get_authorization_headers_for_user(user)

        for x in range(5):
            _, _ = setup_random_seller()

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(len(response), 1)

    def test_consumers_can_list_sellers_who_they_have_reservations_with(self):
        (cuser, consumer), (_, _), _, _ = setup_random_reservation()

        for x in range(5):
            setup_random_reservation_for_consumer(consumer)

        headers = get_authorization_headers_for_user(cuser)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(len(response), 6)
