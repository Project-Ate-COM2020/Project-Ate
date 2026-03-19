from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from authentication.token import UserTokenObtainPairSerializer
from django.conf import settings
from core.models import BundlePosting, Reservation, Seller, Consumer
from marketplace.views import CreateConsumerView
from .views import (
    TotalListingsView,
    TotalRevenueView,
    TotalReservationsView,
    FoodWasteReductionView,
    TotalNoShowsView,
    SellThroughBreakdownView,
    WasteProxyView,
    PricingEffectivenessView,
    PopularCategoriesView,
    BestPickupWindowsView,
)


class AnalyticsViewTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.user, _ = self._create_user_get_auth_headers(
            username="sellerone", password="password", email="sellerone@sellerone.com"
        )

        self.seller, self.seller_auth_headers = self._make_user_a_seller(
            self.user,
            name="Seller One",
            location="Test Location",
            opening_hours="09:00-17:00",
            contact_stub="seller1@example.com",
        )

        self.other_user, _ = self._create_user_get_auth_headers(
            "other", "other@other.com", "password"
        )

        self.other_seller, self.other_seller_headers = self._make_user_a_seller(
            self.other_user,
            name="Test seller",
            location="Other Location",
            opening_hours="09:00-17:00",
            contact_stub="seller2@example.com",
        )

        self.consumer_user, _ = self._create_user_get_auth_headers(
            "consumer", "consumer@consumer.com", "password"
        )

        self.consumer, self.consumer_user_headers = self._make_user_a_consumer(
            self.consumer_user, "Test buyer"
        )

        self._claim_seq = 1

    @staticmethod
    def _create_user_get_auth_headers(username, email, password):
        user_model = get_user_model()

        user = user_model.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        token = UserTokenObtainPairSerializer.get_token(user).access_token

        return user, {"AUTHORIZATION": f"Bearer {token}"}

    @staticmethod
    def _make_user_a_consumer(user, display_name):

        consumer = Consumer.objects.create(
            display_name=display_name,
            user=user,
        )

        token = UserTokenObtainPairSerializer.get_token(user).access_token

        return consumer, {"AUTHORIZATION": f"Bearer {token}"}

    @staticmethod
    def _make_user_a_seller(user, name, location, opening_hours, contact_stub):
        seller = Seller.objects.create(
            location=location,
            opening_hours=opening_hours,
            contact_stub=contact_stub,
            name=name,
            user=user,
        )

        token = UserTokenObtainPairSerializer.get_token(user).access_token

        return seller, {"AUTHORIZATION": f"Bearer {token}"}

    def _create_posting(
        self,
        seller,
        status="active",
        price=Decimal("5.00"),
        category="veg_box",
        pickup_window="18:00-20:00",
    ):
        return BundlePosting.objects.create(
            seller=seller,
            category=category,
            contents="mixed",
            quantity=5,
            quantity_remaining=3,
            price=price,
            pickup_window=pickup_window,
            status=status,
        )

    def _create_reservation(self, posting, status="reserved"):
        claim_code = f"code-{self._claim_seq}"
        self._claim_seq += 1
        return Reservation.objects.create(
            posting=posting,
            consumer=self.consumer,
            claim_code=claim_code,
            status=status,
        )

    # ----------- Sprint 1 tests -----------


    def test_total_listings_returns_count(self):
        self._create_posting(self.seller)
        self._create_posting(self.seller)
        self._create_posting(self.other_seller)
        request = self.factory.get(
            "/analytics/total-listings/",
            headers=self.seller_auth_headers,
        )
        response = TotalListingsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, 2)


    def test_total_revenue_counts_reserved_and_collected(self):
        posting_one = self._create_posting(self.seller, price=Decimal("5.00"))
        posting_two = self._create_posting(self.seller, price=Decimal("7.50"))
        posting_other = self._create_posting(self.other_seller, price=Decimal("9.00"))
        self._create_reservation(posting_one, status="reserved")
        self._create_reservation(posting_two, status="collected")
        self._create_reservation(posting_two, status="no-show")
        self._create_reservation(posting_other, status="reserved")
        request = self.factory.get(
            "/analytics/total-revenue/",
            headers=self.seller_auth_headers,
        )
        response = TotalRevenueView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Decimal(str(response.data)), Decimal("12.50"))


    def test_total_reservations_counts(self):
        posting_one = self._create_posting(self.seller)
        posting_two = self._create_posting(self.seller)
        posting_other = self._create_posting(self.other_seller)
        self._create_reservation(posting_one, status="reserved")
        self._create_reservation(posting_two, status="collected")
        self._create_reservation(posting_other, status="reserved")
        request = self.factory.get(
            "/analytics/total-reservations/",
            headers=self.seller_auth_headers,
        )
        response = TotalReservationsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("total_reservations"), 2)


    def test_food_waste_reduction_no_reservations_returns_zero(self):
        # No reservations exist — should return 0.0, not an error
        request = self.factory.get(
            "/analytics/food-waste-reduction/",
            headers=self.seller_auth_headers,
        )
        response = FoodWasteReductionView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("food_waste_reduction_percentage"), 0.0)

    def test_food_waste_reduction_percentage(self):
        posting = self._create_posting(self.seller)
        posting2 = self._create_posting(self.seller)
        posting_other = self._create_posting(self.other_seller)
        self._create_reservation(posting, status="collected")
        self._create_reservation(posting, status="collected")
        self._create_reservation(posting2, status="reserved")
        self._create_reservation(posting2, status="reserved")
        self._create_reservation(
            posting_other, status="collected"
        )  # other seller, excluded
        request = self.factory.get(
            "/analytics/food-waste-reduction/",
            headers=self.seller_auth_headers,
        )
        response = FoodWasteReductionView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("food_waste_reduction_percentage"), 50.0)


    def test_total_no_shows_counts(self):
        posting_one = self._create_posting(self.seller)
        posting_two = self._create_posting(self.seller)
        posting_other = self._create_posting(self.other_seller)
        self._create_reservation(posting_one, status="no-show")
        self._create_reservation(posting_two, status="no-show")
        self._create_reservation(posting_two, status="reserved")
        self._create_reservation(posting_other, status="no-show")
        request = self.factory.get(
            "/analytics/total-no-shows/",
            headers=self.seller_auth_headers,
        )
        response = TotalNoShowsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("total_no_shows"), 2)

    # ----------- Sprint 2 tests -----------


    def test_sell_through_no_data_returns_zeros(self):
        request = self.factory.get(
            "/analytics/sell-through/",
            headers=self.seller_auth_headers,
        )
        response = SellThroughBreakdownView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("total"), 0)
        self.assertEqual(response.data.get("sell_through_rate"), 0.0)

    def test_sell_through_breakdown_correct(self):
        posting = self._create_posting(self.seller)
        posting_other = self._create_posting(self.other_seller)
        self._create_reservation(posting, status="collected")
        self._create_reservation(posting, status="collected")
        self._create_reservation(posting, status="no-show")
        self._create_reservation(posting, status="expired")
        self._create_reservation(posting_other, status="collected")  # excluded
        request = self.factory.get(
            "/analytics/sell-through/",
            headers=self.seller_auth_headers,
        )
        response = SellThroughBreakdownView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("collected"), 2)
        self.assertEqual(response.data.get("no_show"), 1)
        self.assertEqual(response.data.get("expired"), 1)
        self.assertEqual(response.data.get("total"), 4)
        self.assertEqual(response.data.get("sell_through_rate"), 50.0)


    def test_waste_proxy_calculates_kg(self):
        posting = self._create_posting(self.seller)
        self._create_reservation(posting, status="collected")
        self._create_reservation(posting, status="collected")
        self._create_reservation(posting, status="no-show")
        request = self.factory.get(
            "/analytics/waste-proxy/",
            headers=self.seller_auth_headers,
        )
        response = WasteProxyView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("bundles_collected"), 2)
        self.assertAlmostEqual(response.data.get("kg_saved"), 1.2)
        self.assertEqual(response.data.get("assumed_weight_kg_per_bundle"), 0.6)


    def test_pricing_effectiveness_groups_by_price_bracket(self):
        cheap = self._create_posting(self.seller, price=Decimal("2.00"))
        expensive = self._create_posting(self.seller, price=Decimal("8.00"))
        self._create_reservation(cheap, status="collected")
        self._create_reservation(cheap, status="no-show")
        self._create_reservation(expensive, status="collected")
        request = self.factory.get(
            "/analytics/pricing-effectiveness/",
            headers=self.seller_auth_headers,
        )
        response = PricingEffectivenessView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        ranges = [item["price_range"] for item in response.data]
        self.assertIn("£0-£3", ranges)
        self.assertIn("£6-£10", ranges)
        cheap_bucket = next(i for i in response.data if i["price_range"] == "£0-£3")
        self.assertEqual(cheap_bucket["total_reservations"], 2)
        self.assertEqual(cheap_bucket["sell_through_rate"], 50.0)



    def test_popular_categories_ordered_by_reservations(self):
        bakery = self._create_posting(self.seller, category="bakery")
        veg = self._create_posting(self.seller, category="veg_box")
        self._create_reservation(bakery, status="reserved")
        self._create_reservation(bakery, status="reserved")
        self._create_reservation(bakery, status="reserved")
        self._create_reservation(veg, status="reserved")
        request = self.factory.get(
            "/analytics/popular-categories/",
            headers=self.seller_auth_headers,
        )
        response = PopularCategoriesView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["category"], "bakery")
        self.assertEqual(response.data[0]["total_reservations"], 3)
        self.assertEqual(response.data[1]["category"], "veg_box")



    def test_best_pickup_windows_ordered_by_reservations(self):
        evening = self._create_posting(self.seller, pickup_window="18:00-20:00")
        morning = self._create_posting(self.seller, pickup_window="09:00-11:00")
        self._create_reservation(evening, status="reserved")
        self._create_reservation(evening, status="reserved")
        self._create_reservation(morning, status="reserved")
        request = self.factory.get(
            "/analytics/best-pickup-windows/",
            headers=self.seller_auth_headers,
        )
        response = BestPickupWindowsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["pickup_window"], "18:00-20:00")
        self.assertEqual(response.data[0]["total_reservations"], 2)
