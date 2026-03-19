from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import CreateMaintainerView, MaintainerView, MaintainerSQLView

urlpatterns = [
    path("create", CreateMaintainerView.as_view(), name="maintainer-create"),
    path(
        "retrieve-update-delete/<int:pk>",
        MaintainerView.as_view(),
        name="maintainer-retrieve-update-delete",
    ),
    # post an sql query: ?query="SELECT * FROM Maintainers" etc
    path("maintainer/sql", MaintainerSQLView.as_view(), name="maintainer-sql"),
]
