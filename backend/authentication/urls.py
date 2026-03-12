from .views import UserCreateView
from django.urls import path
from .token import UserTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    # USER creation
    path(
        "user",
        UserCreateView.as_view(),
        name=UserCreateView.name,
    ),
    path(
        "token",
        UserTokenObtainPairView.as_view(),
        name="user-token",
    ),
    path(
        "refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "verify",
        TokenVerifyView.as_view(),
        name="verify-token",
    )
]
