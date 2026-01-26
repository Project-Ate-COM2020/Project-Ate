from django.urls import path
from .views import GameSummaryView, RecentRescuesView

urlpatterns = [
    path("api/game/summary/", GameSummaryView.as_view(), name="game-summary"),
    path("api/game/recent/", RecentRescuesView.as_view(), name="game-recent")
]