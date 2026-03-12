from django.urls import path
from . import views

from .consumer_token import ConsumerTokenObtainPairView
from .seller_token import SellerTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    #
    #
    #   GLOBAL OPERATIONS ON RETRIEVAL OF BUNDLES
    #
    #
    # create bundles
    path(
        "bundle/",
        views.CreateBundleView.as_view(),
        name=views.CreateBundleView.name,
    ),
    path("bundles/", views.BundlesView.as_view(), name="bundles"),
    # get newest n bundles
    # GET ... /marketplace/bundles/between?from=2009?to=20019?exclusive=false
    path(
        "bundles/between",
        views.BundlesView.as_view(),
        name=views.BundlesView.name,
    ),
    # get oldest n bundles
    # GET ... /marketplace/bundles/oldest?count=20
    path(
        "bundles/oldest",
        views.BundleOldestView.as_view(),
        name=views.BundleOldestView.name,
    ),
    # get bundles older than a specified date
    # GET ... /marketplace/bundles/older?date=YYYY-MM-DD
    path(
        r"bundles/older/",
        views.BundleOlderView.as_view(),
        name=views.BundleOlderView.name,
    ),
    # get bundles younger than a specified date
    # GET ... /marketplace/bundles/newer?date=YYYY-MM-DD
    path(
        "bundles/newer/",
        views.BundleNewerView.as_view(),
        name=views.BundleNewerView.name,
    ),
    # get bundles whose shops are open now
    # GET ... /marketplace/bundles/open <- gets open now
    # GET ... /marketplace/bundles/open?from=YYYY-MM-DDTHH-MM-SS{TZD}?to=...
    # {TZD} can be plus or minus then hours minutes ahead / behind e.g +01:50 or -02:00
    # either to or from can be omitted
    path(
        "bundles/open/",
        views.BundleOpenView.as_view(),
        name=views.BundleOpenView.name,
    ),
    # get bundles whose collections are between specific range
    # GET ... /marketplace/bundles/collection?from=YYYY-MM-DDTHH-MM-SS{TZD}?to=...
    # {TZD} can be plus or minus then hours minutes ahead / behind e.g +01:50 or -02:00
    # either to or from can be omitted
    path(
        r"bundles/collection/",
        views.BundleCollectionView.as_view(),
        name=views.BundleCollectionView.name,
    ),
    path(
        "bundle/<int:bundle_id>/",
        views.BundleView.as_view(),
        name=views.BundleView.name,
    ),
    #
    path(
        "consumer",
        views.CreateConsumerView.as_view(),
        name=views.CreateConsumerView.name,
    ),
    path(
        "consumer/<int:consumer_id>/",
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
    # get seller data
    path(
        "seller/<int:seller_id>/",
        views.SellerView.as_view(),
        name=views.SellerView.name,
    ),
    # get bundles for a seller
    path(
        "seller/<int:seller_id>/bundles",
        views.SellerBundlesView.as_view(),
        name=views.SellerBundlesView.name,
    ),
    path(
        "seller/<int:seller_id>/bundles/between",
        views.SellerBundleBetweenView.as_view(),
        name=views.SellerBundleBetweenView.name,
    ),
    path(
        "seller/<int:seller_id>/bundles/newest",
        views.SellerBundleNewestView.as_view(),
        name=views.SellerBundleNewestView.name,
    ),
    path(
        "seller/<int:seller_id>/bundles/oldest",
        views.SellerBundleOldestView.as_view(),
        name=views.SellerBundleOldestView.name,
    ),
    path(
        "seller/<int:seller_id>/bundles/older/",
        views.SellerBundleOlderView.as_view(),
        name=views.SellerBundleOlderView.name,
    ),
    path(
        "seller/<int:seller_id>/bundles/younger/",
        views.BundleNewerView.as_view(),
        name=views.BundleNewerView.name,
    ),
    path(
        "seller/<int:seller_id>/bundles/collection/",
        views.BundleCollectionView.as_view(),
        name=views.BundleCollectionView.name,
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
        "reservations/<int:reservation_id>/",
        views.ReservationView.as_view(),
        name=views.ReservationView.name,
    ),
]
