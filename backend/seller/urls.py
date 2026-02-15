from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddNewListingView, MarkBundleAsCollectedView, SellerAddressView, SellerNameView, SellerReservationsView

urlpatterns = [
    path('getsellername/', SellerNameView.as_view(), name='get-seller-name'),
    path('getselleraddress/', SellerAddressView.as_view(), name='get-seller-address'),
    path('getreservations/', SellerReservationsView.as_view(), name='get-reservations'),
    path('createlisting/', AddNewListingView.as_view(), name='create-listing'),
    path('collectbundle/', MarkBundleAsCollectedView.as_view(), name='mark-as-collected')
]