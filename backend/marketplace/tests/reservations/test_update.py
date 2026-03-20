from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.tests import (
    setup_random_reservation,
    get_authorization_headers_for_user,
)
from marketplace.views import ReservationView


class ReservationUpdateTest(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk):
        return reverse(ReservationView.name, kwargs={"pk": pk})

    def test_seller_can_update_status(self):
        (cuser, consumer), (suser, seller), bundle, reservation = (
            setup_random_reservation()
        )

        co2_saved = consumer.co2_saved
        cats = consumer.categories_collected

        headers = get_authorization_headers_for_user(suser)

        response = self.client.patch(
            self.get_url(reservation.pk),
            {"status": "collected"},
            format="json",
            headers=headers,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        consumer.refresh_from_db()

        self.assertNotEqual(consumer.co2_saved, co2_saved)
        self.assertNotEqual(consumer.categories_collected, cats)
