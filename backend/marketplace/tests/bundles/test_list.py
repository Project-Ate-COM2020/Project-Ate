import json

from django.contrib.sites import requests
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import (
    setup_random_reservation,
    setup_random_bundle,
    setup_random_bundle_for_seller,
    setup_random_consumer,
    get_authorization_headers_for_user, setup_n_random_bundles,
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

    def test_seller_can_only_see_their_bundles(self):
        n = 10
        suser1, seller1, bundles1 = setup_n_random_bundles(n)
        suser2, seller2, bundles2 = setup_n_random_bundles(n)

        headers1 = get_authorization_headers_for_user(suser1)
        headers2 = get_authorization_headers_for_user(suser2)

        response = self.client.get(
            self.url, {"page": 1}, format="json", headers=headers1
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(response["count"], len(bundles1))

        for i, bundle in enumerate(bundles1):
            self.assertEqual(bundle.pk, response["results"][i]["posting_id"])

        response = self.client.get(
            self.url, {"page": 1}, format="json", headers=headers2
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(response["count"], len(bundles2))

        for i, bundle in enumerate(bundles2):
            self.assertEqual(bundle.pk, response["results"][i]["posting_id"])