from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import setup_random_user, get_authorization_headers_for_user
from core.models import Seller
from marketplace.views import CreateSellerView


class CreateSellerViewTests(APITestCase):
    def setUp(self):
        self.url = reverse(CreateSellerView.name)

        self.user = setup_random_user()

        self.headers = get_authorization_headers_for_user(self.user)

        self.seller_data = {
            "name": "lauren",
            "location": "CF54BB",
            "opening_hours": "00:00-24:00",
            "contact_stub": "9874325655",
        }

    def post_create_seller(self):
        self.creation_response = self.client.post(
            self.url, self.seller_data, format="json", headers=self.headers
        )

        return self.creation_response.json()["seller_id"]

    def test_creation_success(self):
        self.post_create_seller()

        self.assertEqual(Seller.objects.count(), 1)

        self.assertEqual(self.creation_response.status_code, status.HTTP_201_CREATED)

    def test_data_integrity(self):
        seller_id = self.post_create_seller()

        seller = Seller.objects.get(seller_id=seller_id)

        self.assertEqual(seller.name, self.seller_data["name"])
        self.assertEqual(seller.location, self.seller_data["location"])
        self.assertEqual(seller.opening_hours, self.seller_data["opening_hours"])
        self.assertEqual(seller.contact_stub, self.seller_data["contact_stub"])
