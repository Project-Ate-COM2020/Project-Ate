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
    path("consumer/", ConsumerIssuesView.as_view(), name=ConsumerIssuesView.name),
    path(
        "comsumer/reportable",
        ConsumerReportablePostingsView.as_view(),
        name=ConsumerReportablePostingsView.name
    ),
    path("seller/<int:seller_id>/issues", SellerIssuesView.as_view(), name=SellerIssuesView.name),
    path("seller/<int:seller_id>/overview/", SellerIssuesOverviewView.as_view(), name=SellerIssuesOverviewView.name),
    path("seller/<int:issue_id>/respond/", SellerIssueRespondView.as_view(), name=SellerIssueRespondView.name),
    path("report/", ConsumerCreateIssueView.as_view(), name=ConsumerCreateIssueView.name),
]