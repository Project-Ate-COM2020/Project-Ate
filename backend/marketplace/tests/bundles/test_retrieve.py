from rest_framework import status
from rest_framework.test import APITestCase

from authentication.tests import setup_random_bundle, get_authorization_headers_for_user, setup_n_random_bundles, \
    setup_random_consumer
from marketplace.views import BundlesView
from django.urls import reverse

class RetrieveBundleViewTests(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk):
        return reverse(BundlesView.name, kwargs={'pk': pk})

    def test_can_retrieve_own_bundles(self):
        suser, seller, bundle = setup_random_bundle()

        headers = get_authorization_headers_for_user(suser)

        response = self.client.get(self.get_url(bundle.pk), format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = response.json()

        self.assertEqual(response["posting_id"], bundle.pk)

    def test_seller_cannot_retrieve_other_bundles(self):
        suser, seller, bundle = setup_random_bundle()
        _, _, bundles2 = setup_n_random_bundles(10)

        headers = get_authorization_headers_for_user(suser)

        response = self.client.get(self.get_url(bundle.pk), format='json', headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for bundle in bundles2:
            response = self.client.get(self.get_url(bundle.pk), format='json', headers=headers)

            self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_consumer_can_retrieve_all(self):
        _, _, bundles1 = setup_n_random_bundles(10)
        _, _, bundles2 = setup_n_random_bundles(10)
        cuser, consumer = setup_random_consumer()

        bundles = bundles1 + bundles2

        headers = get_authorization_headers_for_user(cuser)

        for bundle in bundles:
            response = self.client.get(self.get_url(bundle.pk), format='json', headers=headers)

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            response = response.json()

            self.assertEqual(response["posting_id"], bundle.pk)


