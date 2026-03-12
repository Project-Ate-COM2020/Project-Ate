from django.shortcuts import render
from .models import Maintainer, MaintainerSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView

class CreateMaintainerView(CreateAPIView):
    name = "maintainer-create"
    queryset = Maintainer
    serializer_class = MaintainerSerializer

class MaintainerView(RetrieveUpdateDestroyAPIView):
    name = "maintainer"
    queryset = Maintainer.objects.all()
    serializer_class = MaintainerSerializer