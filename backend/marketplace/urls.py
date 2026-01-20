from django.urls import path
from . import views

urlpatterns = [
    path("marketplace/", views.Bundles.as_view(), name="marketplace"),
]
