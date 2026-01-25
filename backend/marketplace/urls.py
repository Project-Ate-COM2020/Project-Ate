from django.urls import path
from . import views

urlpatterns = [
    #
    #
    #   GLOBAL OPERATIONS ON RETRIEVAL OF BUNDLES
    #
    #
    path("marketplace/bundles/", views.BundlesView.as_view(), name="bundles"),
    # get newest n bundles
    # GET ... /marketplace/bundles/between?from=2009?to=20019?exclusive=false
    path(
        "marketplace/bundles/between",
        views.BundlesView.as_view(),
        name="bundles-newest",
    ),
    # get the newest n bundles
    # GET ... /marketplace/bundles/newest?count=20
    path(
        "marketplace/bundles/newest",
        views.BundlesView.as_view(),
        name="bundles-newest",
    ),
    # get newest n bundles
    # GET ... /marketplace/bundles/oldest?count=20
    path(
        "marketplace/bundles/oldest",
        views.BundlesView.as_view(),
        name="bundles-oldest",
    ),
    # get bundles older than a specified date
    # GET ... /marketplace/bundles/older?date=YYYY-MM-DD
    path(
        r"marketplace/bundles/older/",
        views.BundlesView.as_view(),
        name="bundles-older",
    ),
    # get bundles younger than a specified date
    # GET ... /marketplace/bundles/newer?date=YYYY-MM-DD
    path(
        r"marketplace/bundles/younger/",
        views.BundlesView.as_view(),
        name="bundles-younger",
    ),
    # get bundles whose shops are open now
    # GET ... /marketplace/bundles/open <- gets open now
    # GET ... /marketplace/bundles/open?from=YYYY-MM-DDTHH-MM-SS{TZD}?to=...
    # {TZD} can be plus or minus then hours minutes ahead / behind e.g +01:50 or -02:00
    # either to or from can be omitted
    path(
        r"marketplace/bundles/open/",
        views.BundlesView.as_view(),
        name="bundles-open",
    ),
    # get bundles whose collections are between specific range
    # GET ... /marketplace/bundles/collection?from=YYYY-MM-DDTHH-MM-SS{TZD}?to=...
    # {TZD} can be plus or minus then hours minutes ahead / behind e.g +01:50 or -02:00
    # either to or from can be omitted
    path(
        r"marketplace/bundles/collection/",
        views.BundlesView.as_view(),
        name="bundles-open",
    ),
    path(
        "marketplace/bundle/<int:bundle_id>/", views.BundleView.as_view(), name="bundle"
    ),
    #
    #
    #    USAGE SAME AS ABOVE ONLY DIFFERENCE IS THAT IT ONLY OPERATES ON SELLERS BUNDLES INSTEAD OF GLOBALLY
    #
    #
    # get seller data
    path(
        "marketplace/seller/<int:seller_id>/", views.BundleView.as_view(), name="seller"
    ),
    # get bundles for a seller
    path(
        "marketplace/seller/<int:seller_id>/bundles",
        views.BundleView.as_view(),
        name="seller-bundles",
    ),
    path(
        "marketplace/seller/<int:seller_id>/bundles/between",
        views.BundlesView.as_view(),
        name="seller-bundles-newest",
    ),
    path(
        "marketplace/seller/<int:seller_id>/bundles/newest",
        views.BundlesView.as_view(),
        name="seller-bundles-newest",
    ),
    path(
        "marketplace/seller/<int:seller_id>/bundles/oldest",
        views.BundlesView.as_view(),
        name="seller-bundles-oldest",
    ),
    path(
        r"marketplace/seller/<int:seller_id>/bundles/older/",
        views.BundlesView.as_view(),
        name="seller-bundles-older",
    ),
    path(
        r"marketplace/seller/<int:seller_id>/bundles/younger/",
        views.BundlesView.as_view(),
        name="seller-bundles-younger",
    ),
    path(
        r"marketplace/seller/<int:seller_id>/bundles/collection/",
        views.BundlesView.as_view(),
        name="seller-bundles-open",
    ),
]
