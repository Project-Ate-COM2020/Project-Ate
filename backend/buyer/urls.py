from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MarkReservationAsReserveredView, MarkReservationAsUnreservedView

urlpatterns = [
    path('reservebundle/', MarkReservationAsReserveredView.as_view(), name='mark-reservation-as-reserved'),
    path('unreservebundle/', MarkReservationAsUnreservedView.as_view(), name='mark-reservation-as-unreserved')
]