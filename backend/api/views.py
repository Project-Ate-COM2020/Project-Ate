from django.shortcuts import render
from rest_framework import viewsets
from .models import Item
from django.http import HttpResponse

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()


def index(request):
    return HttpResponse("This is a test page for the Project-Ate API")
