from django.urls import path
from .views import (
    SellerIssuesView,
    SellerIssuesOverviewView,
    SellerIssueRespondView,
    ConsumerCreateIssueView,
    ConsumerIssuesView,
    ConsumerReportablePostingsView,
)

urlpatterns = [
    path("buyer/<int:consumer_id>/", ConsumerIssuesView.as_view(), name="consumer-issues"),
    path(
        "buyer/<int:consumer_id>/reportable-postings/",
        ConsumerReportablePostingsView.as_view(),
        name="consumer-reportable-postings",
    ),
    path("seller/<int:seller_id>/", SellerIssuesView.as_view(), name="seller-issues"),
    path("seller/<int:seller_id>/overview/", SellerIssuesOverviewView.as_view(), name="seller-issues-overview"),
    path("seller/<int:seller_id>/<int:issue_id>/respond/", SellerIssueRespondView.as_view(), name="seller-issue-respond"),
    path("report/", ConsumerCreateIssueView.as_view(), name="consumer-create-issue"),
]