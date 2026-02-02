from django.urls import path, include
from backend import forecasts, seller
from rest_framework.routers import DefaultRouter

from backend.seller.views import SellerAddressView, SellerNameView
from .views import ForecastInputViewSet, ForecastOutputViewSet, ForecastPredictionView

router = DefaultRouter()
router.register("forecast-input", ForecastInputViewSet, basename='forecast-input')
router.register("forecast-output", ForecastOutputViewSet, basename='forecast-output')

urlpatterns = [
    path('', include(router.urls)),
    path('forecast/', include(forecasts.urls)),
    path('seller/', include(seller.urls)),
]
