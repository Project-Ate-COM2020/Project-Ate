from django.urls import path
from .views import SellerIssuesView, SellerIssuesOverviewView, SellerIssueRespondView

urlpatterns = [
    path("seller/<int:seller_id>/", SellerIssuesView.as_view(), name="seller-issues"),
    path("seller/<int:seller_id>/overview/", SellerIssuesOverviewView.as_view(), name="seller-issues-overview"),
    path("seller/<int:seller_id>/<int:issue_id>/respond/", SellerIssueRespondView.as_view(), name="seller-issue-respond"),
]
