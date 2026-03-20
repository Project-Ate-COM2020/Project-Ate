from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from authentication.tests import (
    setup_random_user,
    setup_random_seller,
    get_authorization_headers_for_user,
)
from core.models import BundlePosting
from marketplace.views import CreateSellerView, CreateBundleView


class CreateBundleViewsTests(APITestCase):
    def setUp(self):
        seller_url = reverse(CreateSellerView.name)

        self.seller_user, self.seller = setup_random_seller()

        self.seller_auth_headers = get_authorization_headers_for_user(self.seller_user)

        self.seller_id = self.seller.pk

        bundle_url = reverse(CreateBundleView.name)

        bundle_data = {
            "seller": int(self.seller_id),
            "category": "food",
            "contents": "A bagel",
            "quantity": 8,
            "price": 55,
            "pickup_window": "00:00-24:00",
            "status": "active",
        }

        self.bundle_creation_response = self.client.post(
            bundle_url, bundle_data, format="json", headers=self.seller_auth_headers
        )

        self.bundle_id = self.bundle_creation_response.json()["posting_id"]

    def test_creation_success(self):
        self.assertEqual(
            self.bundle_creation_response.status_code, status.HTTP_201_CREATED
        )

        self.assertEqual(BundlePosting.objects.count(), 1)

    def test_bundle_data_integrity(self):
        bundle = BundlePosting.objects.get(posting_id=self.bundle_id)

        self.assertEqual(bundle.seller.pk, self.seller_id)
        self.assertEqual(bundle.category, "food")
        self.assertEqual(bundle.contents, "A bagel")
        self.assertEqual(bundle.quantity, 8)
        self.assertEqual(bundle.pickup_window, "00:00-24:00")
        self.assertEqual(bundle.status, "active")
