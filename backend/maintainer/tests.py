from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import setup_random_consumer_and_seller, get_authorization_headers_for_user, \
    random_maintainer_args, setup_random_maintainer
from maintainer.views import CreateMaintainerView, MaintainerListView, MaintainerView


class MaintainerCreateAPIViewTests(APITestCase):
    def setUp(self):
        self.url = reverse(CreateMaintainerView.name)

    def test_only_maintainer_can_create_maintainer(self):
        user, consumer, seller = setup_random_consumer_and_seller()

        headers = get_authorization_headers_for_user(user)

        response = self.client.post(self.url, data=random_maintainer_args(), headers=headers, format='json')

        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

        user, maintainer = setup_random_maintainer()

        headers = get_authorization_headers_for_user(user)

        response = self.client.post(self.url, data=random_maintainer_args(), headers=headers, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class MaintainerListAPIViewTests(APITestCase):
    def setUp(self):
        self.url = reverse(MaintainerListView.name)


class MaintainerUpdateAPIViewTests(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk):
        return reverse(MaintainerView.name, kwargs={'pk': pk})

class MaintainerRetrieveAPIViewTests(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk):
        return reverse(MaintainerView.name, kwargs={'pk': pk})

class MaintainerDeleteAPIViewTests(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk):
        return reverse(MaintainerView.name, kwargs={'pk': pk})