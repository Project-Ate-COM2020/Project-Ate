from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TotalListingsView,
    TotalRevenueView,
    TotalReservationsView,
    FoodWasteReductionView,
    TotalNoShowsView,
    GetCollectedReservationsView,
    SellThroughBreakdownView,
    WasteProxyView,
    PricingEffectivenessView,
    PopularCategoriesView,
    BestPickupWindowsView,
)

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('total-listings/', TotalListingsView.as_view(), name='total-listings'),
    path('total-revenue/', TotalRevenueView.as_view(), name='total-revenue'),
    path('total-reservations/', TotalReservationsView.as_view(), name='total-reservations'),
    path('food-waste-reduction/', FoodWasteReductionView.as_view(), name='food-waste-reduction'),
    path('total-no-shows/', TotalNoShowsView.as_view(), name='total_no_shows'),
    path('collected-reservations/', GetCollectedReservationsView.as_view(), name='collected-reservations'),
    # Sprint 2
    path('sell-through/', SellThroughBreakdownView.as_view(), name='sell-through'),
    path('waste-proxy/', WasteProxyView.as_view(), name='waste-proxy'),
    path('pricing-effectiveness/', PricingEffectivenessView.as_view(), name='pricing-effectiveness'),
    path('popular-categories/', PopularCategoriesView.as_view(), name='popular-categories'),
    path('best-pickup-windows/', BestPickupWindowsView.as_view(), name='best-pickup-windows'),
]
