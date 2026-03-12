from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .token import MaintainerTokenObtainPairView, MaintainerTokenObtainPairSerializer

urlpatterns = [
    path("auth/token", MaintainerTokenObtainPairView.as_view(), name="maintainer-token-obtain"),
    path("auth/refresh", TokenRefreshView.as_view(), name="maintainer-token-refresh"),
    path("auth/verify", TokenVerifyView.as_view(), name="maintainer-token-verify"),
]