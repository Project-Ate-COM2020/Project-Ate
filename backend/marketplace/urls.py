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
        "marketplace/bundle/",
        views.CreateBundleView.as_view(),
        name=views.CreateBundleView.name,
    ),
    path("marketplace/bundles/", views.BundlesView.as_view(), name="bundles"),
    # get newest n bundles
    # GET ... /marketplace/bundles/between?from=2009?to=20019?exclusive=false
    path(
        "marketplace/bundles/between",
        views.BundlesView.as_view(),
        name=views.BundlesView.name,
    ),
    # get oldest n bundles
    # GET ... /marketplace/bundles/oldest?count=20
    path(
        "marketplace/bundles/oldest",
        views.BundleOldestView.as_view(),
        name=views.BundleOldestView.name,
    ),
    # get bundles older than a specified date
    # GET ... /marketplace/bundles/older?date=YYYY-MM-DD
    path(
        r"marketplace/bundles/older/",
        views.BundleOlderView.as_view(),
        name=views.BundleOlderView.name,
    ),
    # get bundles younger than a specified date
    # GET ... /marketplace/bundles/newer?date=YYYY-MM-DD
    path(
        "marketplace/bundles/newer/",
        views.BundleNewerView.as_view(),
        name=views.BundleNewerView.name,
    ),
    # get bundles whose shops are open now
    # GET ... /marketplace/bundles/open <- gets open now
    # GET ... /marketplace/bundles/open?from=YYYY-MM-DDTHH-MM-SS{TZD}?to=...
    # {TZD} can be plus or minus then hours minutes ahead / behind e.g +01:50 or -02:00
    # either to or from can be omitted
    path(
        "marketplace/bundles/open/",
        views.BundleOpenView.as_view(),
        name=views.BundleOpenView.name,
    ),
    # get bundles whose collections are between specific range
    # GET ... /marketplace/bundles/collection?from=YYYY-MM-DDTHH-MM-SS{TZD}?to=...
    # {TZD} can be plus or minus then hours minutes ahead / behind e.g +01:50 or -02:00
    # either to or from can be omitted
    path(
        r"marketplace/bundles/collection/",
        views.BundleCollectionView.as_view(),
        name=views.BundleCollectionView.name,
    ),
    path(
        "marketplace/bundle/<int:bundle_id>/",
        views.BundleView.as_view(),
        name=views.BundleView.name,
    ),
    #
    path(
        "marketplace/consumer",
        views.CreateConsumerView.as_view(),
        name=views.CreateConsumerView.name,
    ),
    path(
        "marketplace/consumer/<int:consumer_id>/",
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
        "marketplace/seller",
        views.CreateSellerView.as_view(),
        name=views.CreateSellerView.name,
    ),
    # get seller data
    path(
        "marketplace/seller/<int:seller_id>/",
        views.SellerView.as_view(),
        name=views.SellerView.name,
    ),
    # get bundles for a seller
    path(
        "marketplace/seller/<int:seller_id>/bundles",
        views.SellerBundlesView.as_view(),
        name=views.SellerBundlesView.name,
    ),
    path(
        "marketplace/seller/<int:seller_id>/bundles/between",
        views.SellerBundleBetweenView.as_view(),
        name=views.SellerBundleBetweenView.name,
    ),
    path(
        "marketplace/seller/<int:seller_id>/bundles/newest",
        views.SellerBundleNewestView.as_view(),
        name=views.SellerBundleNewestView.name,
    ),
    path(
        "marketplace/seller/<int:seller_id>/bundles/oldest",
        views.SellerBundleOldestView.as_view(),
        name=views.SellerBundleOldestView.name,
    ),
    path(
        "marketplace/seller/<int:seller_id>/bundles/older/",
        views.SellerBundleOlderView.as_view(),
        name=views.SellerBundleOlderView.name,
    ),
    path(
        "marketplace/seller/<int:seller_id>/bundles/younger/",
        views.BundleNewerView.as_view(),
        name=views.BundleNewerView.name,
    ),
    path(
        "marketplace/seller/<int:seller_id>/bundles/collection/",
        views.BundleCollectionView.as_view(),
        name=views.BundleCollectionView.name,
    ),
    #
    # Reservation end points
    #
    path(
        "marketplace/reservations",
        views.CreateReservationView.as_view(),
        name=views.CreateReservationView.name,
    ),
    path(
        "marketplace/reservations/<int:reservation_id>/",
        views.ReservationView.as_view(),
        name=views.ReservationView.name,
    ),
    # Seller Authentication
    path(
        "marketplace/seller/auth/token",
        SellerTokenObtainPairView.as_view(),
        name="seller-token-obtain-pair",
    ),
    path(
        "marketplace/seller/auth/token/refresh",
        TokenRefreshView.as_view(),
        name="seller-token-refresh",
    ),
    path(
        "marketplace/seller/auth/token/verify/",
        TokenVerifyView.as_view(),
        name="seller-token-verify",
    ),
    # Consumer Authentication
    path(
        "marketplace/consumer/auth/token",
        ConsumerTokenObtainPairView.as_view(),
        name="consumer-token-obtain-pair",
    ),
    path(
        "marketplace/consumer/auth/token/refresh",
        TokenRefreshView.as_view(),
        name="consumer-token-refresh",
    ),
    path(
        "marketplace/consumer/auth/token/verify/",
        TokenVerifyView.as_view(),
        name="consumer-token-verify",
    ),
]
