from django.urls import path
from .views import GameSummaryView, RecentRescuesView, TestView, ConsumerBadgesView

urlpatterns = [
    path("summary/", GameSummaryView.as_view(), name="game-summary"),
    path("recent/", RecentRescuesView.as_view(), name="game-recent"),
    path("badges/", ConsumerBadgesView.as_view(), name="game-badges"),
]
