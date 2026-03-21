from django.urls import path
from .views import GameSummaryView, RecentRescuesView, ConsumerBadgesView

urlpatterns = [
    path("summary/", GameSummaryView.as_view(), name=GameSummaryView.name),
    path("recent/", RecentRescuesView.as_view(), name=RecentRescuesView.name),
    path("badges/", ConsumerBadgesView.as_view(), name=ConsumerBadgesView.name),
]
