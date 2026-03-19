from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from .views import CreateMaintainerView, MaintainerView, MaintainerSQLView, MaintainerListView

urlpatterns = [
    path("create", CreateMaintainerView.as_view(), name=CreateMaintainerView.name),
    path("list", MaintainerListView.as_view(), name=MaintainerListView.name),
    path("<int:pk>", MaintainerView.as_view(), name=MaintainerView.name),
    # post an sql query: ?query="SELECT * FROM Maintainers" etc
    path("sql", MaintainerSQLView.as_view(), name=MaintainerSQLView.name),
]
