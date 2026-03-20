from django.db.models.aggregates import Max
from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from decimal import Decimal

from authentication.tests import (
    setup_consumer,
    setup_random_consumer,
    setup_random_seller,
    get_authorization_headers_for_user,
    setup_random_reservation,
    setup_random_bundle_for_seller,
    setup_random_reservation_for_consumer_and_bundle,
)
from core.models import (
    Consumer,
    Seller,
    BundlePosting,
    Reservation,
    Badges,
    BadgeMapping,
)
from marketplace.views import ReservationView
from .constants import get_co2_per_item
from math import ceil

from .views import ConsumerBadgesView

CO2_PER_ITEM = get_co2_per_item()


class TestReservationUpdatesBadges(APITestCase):
    def setUp(self):
        pass

    def get_url(self, pk):
        return reverse(ReservationView.name, kwargs={"pk": pk})

    def _collect_reservation(self, suser: User, reservation: Reservation):
        headers = get_authorization_headers_for_user(suser)

        response = self.client.patch(
            self.get_url(reservation.pk),
            data={"status": "collected"},
            headers=headers,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_can_earn_all_badges(self):
        # work out the maximum value
        # helps set market conditions for fastest way to achieve badges
        m = max(CO2_PER_ITEM.values())

        max_category = None

        for k, v in CO2_PER_ITEM.items():
            if v == m:
                max_category = k

        max_badges = Badges.objects.all().aggregate(co2=Max("min_co2"))

        max_co2 = max_badges["co2"]

        number_of_bundles_needed = ceil(max_co2 / m)

        # setup market
        cuser, consumer = setup_random_consumer()
        suser, seller = setup_random_seller()

        bundles = []

        for x in range(number_of_bundles_needed):
            b = setup_random_bundle_for_seller(seller, {"category": max_category})

            bundles.append(b)

        for category in BundlePosting.CATEGORY_CHOICES:
            b = setup_random_bundle_for_seller(seller, {"category": category[0]})
            bundles.append(b)

        for bundle in bundles:
            setup_random_reservation_for_consumer_and_bundle(consumer, bundle)

        # collect all bundles as a user
        for bundle in bundles:
            self._collect_reservation(suser, bundle)

        consumer.refresh_from_db()

        # test user obtained all badges
        self.assertEqual(
            BadgeMapping.objects.filter(consumer_id=consumer).count(),
            Badges.objects.count(),
        )


class TestConsumerBadgeView(APITestCase):
    def setUp(self):
        self.url = reverse(ConsumerBadgesView.name)

    def get_url(self, pk):
        return reverse(ReservationView.name, kwargs={"pk": pk})

    def _collect_reservation(self, suser: User, reservation: Reservation):
        headers = get_authorization_headers_for_user(suser)

        response = self.client.patch(
            self.get_url(reservation.pk),
            data={"status": "collected"},
            headers=headers,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_no_badges(self):
        user, _ = setup_random_consumer()

        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_some_badges(self):
        # work out the maximum value
        # helps set market conditions for fastest way to achieve badges
        m = max(CO2_PER_ITEM.values())

        max_category = None

        for k, v in CO2_PER_ITEM.items():
            if v == m:
                max_category = k

        max_badges = Badges.objects.all().aggregate(co2=Max("min_co2"))

        max_co2 = max_badges["co2"]

        number_of_bundles_needed = ceil(max_co2 / m)

        # setup market
        cuser, consumer = setup_random_consumer()
        suser, seller = setup_random_seller()
        headers = get_authorization_headers_for_user(cuser)

        bundles = []

        for x in range(number_of_bundles_needed):
            b = setup_random_bundle_for_seller(seller, {"category": max_category})

            bundles.append(b)

        for category in BundlePosting.CATEGORY_CHOICES:
            b = setup_random_bundle_for_seller(seller, {"category": category[0]})
            bundles.append(b)

        for bundle in bundles:
            setup_random_reservation_for_consumer_and_bundle(consumer, bundle)

        # collect all bundles as a user
        for bundle in bundles:
            self._collect_reservation(suser, bundle)

        consumer.refresh_from_db()

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        returned_ids = []

        for badge in response:
            returned_ids.append(badge["badge_id"])

        for badge in Badges.objects.all():
            self.assertIn(badge.pk, returned_ids)
