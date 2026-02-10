from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('game/', include('game.urls')),
    path('forecast/', include('forecasts.urls')),
    path('api-auth', include('rest_framework.urls'))
]
