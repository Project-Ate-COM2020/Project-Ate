from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import setup_random_seller, get_authorization_headers_for_user, setup_random_consumer
from core.models import Consumer, Seller
from marketplace.views import SellerView

class DestroySellerViewTest(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk: int):
        return reverse(SellerView.name, kwargs={'pk': pk})

    def test_seller_can_delete_self(self):
        user, seller = setup_random_seller()

        headers = get_authorization_headers_for_user(user)

        response = self.client.delete(self.get_url(pk=seller.pk), format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Consumer.objects.count(), 0)

    def test_seller_cannot_delete_other_seller(self):
        user1, seller1 = setup_random_seller()
        user2, seller2 = setup_random_seller()

        headers = get_authorization_headers_for_user(user1)

        response = self.client.delete(self.get_url(pk=seller2.pk), format='json', headers=headers)

        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Seller.objects.count(), 2)

        headers = get_authorization_headers_for_user(user2)

        response = self.client.delete(self.get_url(pk=seller1.pk), format='json', headers=headers)

        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Seller.objects.count(), 2)

    def test_consumer_cannot_delete_seller(self):
        user, consumer = setup_random_consumer()

        suser, seller = setup_random_seller()

        headers = get_authorization_headers_for_user(user)

        response = self.client.delete(self.get_url(pk=seller.pk), format='json', headers=headers)

        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Seller.objects.count(), 1)