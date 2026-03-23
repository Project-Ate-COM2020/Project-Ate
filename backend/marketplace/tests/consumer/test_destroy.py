from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import (
    setup_random_consumer,
    get_authorization_headers_for_user,
)
from core.models import Consumer
from marketplace.views import ConsumerView


class ConsumerViewDestroyViewTests(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk):
        return reverse(ConsumerView.name, kwargs={"pk": pk})

    def test_can_destroy_self(self):
        user, consumer = setup_random_consumer()

        headers = get_authorization_headers_for_user(user)

        response = self.client.delete(self.get_url(consumer.pk), headers=headers)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Consumer.objects.count(), 0)

    def test_cannot_destroy_other_consumer(self):
        user, consumer = setup_random_consumer()
        user2, consumer2 = setup_random_consumer()

        headers = get_authorization_headers_for_user(user)

        response = self.client.delete(self.get_url(consumer2.pk), headers=headers)

        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Consumer.objects.count(), 2)

        headers = get_authorization_headers_for_user(user2)

        response = self.client.delete(self.get_url(consumer.pk), headers=headers)

        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Consumer.objects.count(), 2)
