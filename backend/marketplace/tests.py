from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse

from .models import Seller, Consumer, Reservation, Bundle
from .views import CreateBundleView, CreateSellerView, CreateReservationView, CreateConsumerView

# Create your tests here.
class CreateBundleViewsTests(APITestCase):
    def setUp(self):
        url = reverse(CreateBundleView.name)

        pass

class CreateSellerViewTests(APITestCase):
    def setUp(self):
        self.url = reverse(CreateSellerView.name)

        pass

class CreateReservationViewsTests(APITestCase):
    def setUp(self):
        self.url = reverse(CreateReservationView.name)

        pass

class CreateConsumerViewTests(APITestCase):
    def setUp(self):
        self.url = reverse(CreateConsumerView.name)

        pass