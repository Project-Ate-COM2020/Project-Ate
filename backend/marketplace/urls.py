from django.urls import path
from . import views

from .views.bundles import AllergenListView, ListBundlesView, BundlesView

urlpatterns = [
    # get all allergens (UK Food Information Regulations 2014 - 14 allergens)
    # GET ... /marketplace/allergens/
    path("allergens/", AllergenListView.as_view(), name="allergen-list"),
    #
    #
    #   GLOBAL OPERATIONS ON RETRIEVAL OF BUNDLES
    #
    #
    # create bundles
    path(
        "bundle/create",
        views.CreateBundleView.as_view(),
        name=views.CreateBundleView.name,
    ),
    path(
        "bundle/list",
        views.ListBundlesView.as_view(),
        name=views.ListBundlesView.name,
    ),
    path(
        "bundle/<int:pk>/",
        views.BundlesView.as_view(),
        name=views.BundlesView.name,
    ),
    path(
        "consumer",
        views.CreateConsumerView.as_view(),
        name=views.CreateConsumerView.name,
    ),
    path(
        "consumer/list",
        views.ListConsumerView.as_view(),
        name=views.ListConsumerView.name,
    ),
    path(
        "consumer/<int:pk>/",
        views.ConsumerView.as_view(),
        name=views.ConsumerView.name,
    ),
    #
    #
    #    USAGE SAME AS ABOVE ONLY DIFFERENCE IS THAT IT ONLY OPERATES ON SELLERS BUNDLES INSTEAD OF GLOBALLY
    #
    #
    # create seller
    path(
        "seller",
        views.CreateSellerView.as_view(),
        name=views.CreateSellerView.name,
    ),
    path(
        "seller/list",
        views.ListSellerView.as_view(),
        name=views.ListSellerView.name,
    ),
    # get seller data
    path(
        "seller/<int:pk>/",
        views.SellerView.as_view(),
        name=views.SellerView.name,
    ),
    path(
        "seller/<int:pk>/bundles",
        views.ListSellerBundlesView.as_view(),
        name=views.ListSellerBundlesView.name,
    ),
    #
    # Reservation end points
    #
    path(
        "reservations",
        views.CreateReservationView.as_view(),
        name=views.CreateReservationView.name,
    ),
    path(
        "reservations/list",
        views.ListReservationView.as_view(),
        name=views.ListReservationView.name,
    ),
    path(
        "reservations/<int:pk>/",
        views.ReservationView.as_view(),
        name=views.ReservationView.name,
    ),
]
