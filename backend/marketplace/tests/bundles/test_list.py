import json

from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import (
    setup_random_reservation,
    setup_random_bundle,
    setup_random_bundle_for_seller,
    setup_random_consumer,
    get_authorization_headers_for_user,
)
from marketplace.views import ListBundlesView


class ListBundleViewsTests(APITestCase):
    def setUp(self):
        self.url = reverse(ListBundlesView.name)

    def test_user_can_see_bundles(self):
        cuser, consumer = setup_random_consumer()

        headers = get_authorization_headers_for_user(cuser)

        suser, seller, bundle = setup_random_bundle()

        bundles = [bundle]

        for x in range(5):
            bundle = setup_random_bundle_for_seller(seller)

            bundles.append(bundle)

        response = self.client.get(
            self.url, {"page": 1}, format="json", headers=headers
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(response["count"], 6)

        self.assertEqual(len(response["results"]), 6)

        for i, bundle in enumerate(bundles):
            self.assertEqual(bundle.pk, response["results"][i]["posting_id"])