from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.tests import (
    setup_random_consumer,
    get_authorization_headers_for_user,
    setup_random_seller,
    setup_random_reservation_for_seller,
)
from marketplace.views import ListConsumerView


class ListConsumerViewTest(APITestCase):
    def setUp(self):
        self.url = reverse(ListConsumerView.name)

    def test_can_list_self(self):
        user, _ = setup_random_consumer()

        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(len(response), 1)

    def test_cannot_list_other_consumer(self):
        user, _ = setup_random_consumer()

        for x in range(5):
            _, _ = setup_random_consumer()

        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(len(response), 1)

    def test_seller_can_list_consumers_who_have_reserved_bundles(self):
        user, seller = setup_random_seller()

        for x in range(5):
            _, _, _, _ = setup_random_reservation_for_seller(seller)

        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(len(response), 5)
