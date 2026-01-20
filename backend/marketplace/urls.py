from django.urls import path
from . import views

urlpatterns = [
    path("marketplace/bundles", views.BundlesView.as_view(), name="bundles"),
    path(
        "marketplace/bundle/<int:bundle_id>/", views.BundleView.as_view(), name="bundle"
    ),
]
