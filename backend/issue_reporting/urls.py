from django.urls import path
from .views import SellerIssuesView, SellerIssuesOverviewView

urlpatterns = [
    path("seller/<int:seller_id>/", SellerIssuesView.as_view(), name="seller-issues"),
    path("seller/<int:seller_id>/overview/", SellerIssuesOverviewView.as_view(), name="seller-issues-overview"),
]
