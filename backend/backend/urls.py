from django.contrib import admin
from django.urls import path, include

urlpatterns = [
<<<<<<< HEAD
    path("admin/", admin.site.urls),
    path("api-auth", include("rest_framework.urls")),
    path("", include("marketplace.urls")),
=======
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('game/', include('game.urls'))
]
