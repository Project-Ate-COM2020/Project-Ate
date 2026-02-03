from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SellerAddressView, SellerNameView, SellerReservationsView

urlpatterns = [
    path('getsellername/', SellerNameView.as_view(), name='get-seller-name'),
    path('getselleraddress/', SellerAddressView.as_view(), name='get-seller-address'),
    path('getreservations/', SellerReservationsView.as_view(), name='get-reservations')
]