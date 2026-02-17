from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TotalListingsView, TotalRevenueView, TotalReservationsView, FoodWasteReductionView, TotalNoShowsView, GetCollectedReservationsView

router = DefaultRouter()
# router.register("forecast-input", ForecastInputViewSet, basename='forecast-input')
# router.register("forecast-output", ForecastOutputViewSet, basename='forecast-output')

urlpatterns = [
    path('', include(router.urls)),
    path('total-listings/', TotalListingsView.as_view(), name='total-listings'),
    path('total-revenue/', TotalRevenueView.as_view(), name='total-revenue'),
    path('total-reservations/', TotalReservationsView.as_view(), name='total-reservations'),
    path('food-waste-reduction/', FoodWasteReductionView.as_view(), name='food-waste-reduction'),
    path('total-no-shows/', TotalNoShowsView.as_view(), name='total_no_shows'),
    path('collected-reservations/', GetCollectedReservationsView.as_view(), name='collected-reservations'),
    
]