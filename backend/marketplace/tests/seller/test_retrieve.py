from rest_framework import status
from rest_framework.test import APITestCase

from authentication.tests import setup_seller, setup_random_seller, get_authorization_headers_for_user, \
    setup_random_consumer
from marketplace.views import SellerView
from django.urls import reverse

class RetrieveSellerViewTest(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk):
        return reverse(SellerView.name, kwargs={'pk': pk})

    def test_seller_can_retrieve_self(self):
        suser, seller = setup_random_seller()

        headers = get_authorization_headers_for_user(suser)

        response = self.client.get(self.get_url(pk=seller.pk), format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(response["seller_id"], seller.pk)

    def test_seller_cannot_retrieve_other_seller(self):
        suser, seller = setup_random_seller()

        headers = get_authorization_headers_for_user(suser)

        sellers = []

        for x in range(10):
            _, seller = setup_random_seller()

            sellers.append(seller)

        for seller in sellers:
            response = self.client.get(self.get_url(pk=seller.pk), format='json', headers=headers)

            self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_consumer_can_retrieve_any_seller(self):
        cuser, consumer = setup_random_consumer()

        headers = get_authorization_headers_for_user(cuser)

        sellers = []

        for x in range(10):
            _, seller = setup_random_seller()

            sellers.append(seller)

        for seller in sellers:
            response = self.client.get(self.get_url(pk=seller.pk), format='json', headers=headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)