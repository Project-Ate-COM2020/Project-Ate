from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("seller/", include("seller.urls")),
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("marketplace/", include("marketplace.urls")),
    path("game/", include("game.urls")),
    path("forecast/", include("forecasts.urls")),
    path("analytics/", include("analytics.urls")),
    path("maintainer/", include("maintainer.urls")),
    path("auth/", include("authentication.urls")),
]
