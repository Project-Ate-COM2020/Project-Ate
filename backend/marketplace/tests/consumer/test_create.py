from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import setup_random_user, get_authorization_headers_for_user
from core.models import Consumer
from marketplace.views import CreateConsumerView


class CreateConsumerViewTests(APITestCase):
    def setUp(self):
        consumer_url = reverse(CreateConsumerView.name)

        self.user = setup_random_user()

        self.headers = get_authorization_headers_for_user(self.user)

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
