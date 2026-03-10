from django.urls import path
from .views import GameSummaryView, RecentRescuesView, TestView, ConsumerBadgesView

urlpatterns = [
    path("api/game/summary/", GameSummaryView.as_view(), name="game-summary"),
    path("api/game/recent/", RecentRescuesView.as_view(), name="game-recent"),
    path("api/game/badges/", ConsumerBadgesView.as_view(), name="game-badges"),
    path("api/test/", TestView.as_view())
]