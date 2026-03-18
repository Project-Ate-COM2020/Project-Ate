from rest_framework.test import APITestCase
from django.urls import reverse

from marketplace.views import ListBundlesView


class ListBundleViewsTests(APITestCase):
    def setUp(self):
        self.url = reverse(ListBundlesView.name)

    def test_user_can_see_bundles(self):
        pass
