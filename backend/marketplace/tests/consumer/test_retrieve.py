from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import (
    setup_random_consumer,
    get_authorization_headers_for_user,
    setup_random_reservation,
    setup_random_reservation_for_consumer,
    setup_random_reservation_for_seller,
)
from core.serializers import ConsumerSerializer
from marketplace.views import ConsumerView


class ConsumerRetrieveViewTests(APITestCase):
    def setup(self):
        pass

    def get_url(self, pk):
        return reverse(ConsumerView.name, kwargs={"pk": pk})

    def test_can_retrieve_self(self):
        user, consumer = setup_random_consumer()

        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.get_url(pk=consumer.pk), headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(response["consumer_id"], consumer.pk)

    def test_consumer_cannot_retrieve_other_consumers(self):
        user, consumer = setup_random_consumer()
        user2, consumer2 = setup_random_consumer()

        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.get_url(pk=consumer2.pk), headers=headers)

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

        headers = get_authorization_headers_for_user(user2)

        response = self.client.get(self.get_url(pk=consumer.pk), headers=headers)

        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_seller_can_retrieve_consumers_who_have_reserved_a_bundle_with_them(self):
        (_, consumer), (suser, seller), bundle, reservation = setup_random_reservation()

        consumers = [consumer]

        for x in range(5):
            _, consumer, _, _ = setup_random_reservation_for_seller(seller)
            consumers.append(consumer)

        headers = get_authorization_headers_for_user(suser)

        for x in consumers:
            response = self.client.get(self.get_url(pk=x.pk), headers=headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
