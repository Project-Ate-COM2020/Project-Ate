from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SellerAddressView, SellerNameView

urlpatterns = [
    path('getsellername/<int:seller_id>/', SellerNameView.as_view(), name='get-seller-name'),
    path('getselleraddress/<int:seller_id>/', SellerAddressView.as_view(), name='get-seller-address'),
    
]