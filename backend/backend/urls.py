from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('forecast/', include('forecasts.urls')),
    path('api-auth', include('rest_framework.urls')),
    path('analytics/', include('analytics.urls')),
    path('seller/', include('seller.urls')),
]
