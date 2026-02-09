from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ForecastPredictionView

router = DefaultRouter()
# router.register("forecast-input", ForecastInputViewSet, basename='forecast-input')
# router.register("forecast-output", ForecastOutputViewSet, basename='forecast-output')

urlpatterns = [
    path('', include(router.urls)),
    path('prediction/', ForecastPredictionView.as_view(), name='forecast-prediction'),
]