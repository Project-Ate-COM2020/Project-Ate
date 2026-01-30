from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ForecastInputViewSet, ForecastOutputViewSet, ForecastPredictionView

router = DefaultRouter()
router.register(r'forecast-input', ForecastInputViewSet, basename='forecast-input')
router.register(r'forecast-output', ForecastOutputViewSet, basename='forecast-output')

urlpatterns = [
    path('', include(router.urls)),
    path('forecast-prediction/', ForecastPredictionView.as_view(), name='forecast-prediction'),
]
