from django.urls import path, include
from backend import forecasts, analytics, seller
from rest_framework.routers import DefaultRouter
from .views import ForecastInputViewSet, ForecastOutputViewSet, ForecastPredictionView, AnalyticView # ignore type: ignore

from backend.seller.views import SellerAddressView, SellerNameView
from .views import ForecastInputViewSet, ForecastOutputViewSet, ForecastPredictionView

router = DefaultRouter()
router.register("forecast-input", ForecastInputViewSet, basename='forecast-input')
router.register("forecast-output", ForecastOutputViewSet, basename='forecast-output')
router.register("analytics", AnalyticView, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    path('forecast/', include(forecasts.urls)),
    path('analytics/', include(analytics.urls)),
    path('seller/', include(seller.urls)),
]
