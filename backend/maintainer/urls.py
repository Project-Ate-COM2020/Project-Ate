from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .token import MaintainerTokenObtainPairView, MaintainerTokenObtainPairSerializer
from .views import CreateMaintainerView, MaintainerView, MaintainerSQLView

urlpatterns = [
    path("auth/token", MaintainerTokenObtainPairView.as_view(), name="maintainer-token-obtain"),
    path("auth/refresh", TokenRefreshView.as_view(), name="maintainer-token-refresh"),
    path("auth/verify", TokenVerifyView.as_view(), name="maintainer-token-verify"),
    path("create", CreateMaintainerView.as_view(), name="maintainer-create"),
    path("retrieve-update-delete/<int:maintainer_id>", MaintainerView.as_view(), name="maintainer-retrieve-update-delete"),
    # post an sql query: ?query="SELECT * FROM Maintainers" etc
    path("maintainer/sql", MaintainerSQLView.as_view(), name="maintainer-sql"),
]