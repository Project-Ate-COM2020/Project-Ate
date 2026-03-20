import json

from django.shortcuts import render

from .models import Maintainer, MaintainerSerializer, RegisterMaintainerSerializer
from authentication.permissions import IsMaintainer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response


class CreateMaintainerView(CreateAPIView):
    name = "maintainer-create"
    queryset = Maintainer.objects.all()
    serializer_class = RegisterMaintainerSerializer
    permission_classes = [IsMaintainer]

class MaintainerListView(ListAPIView):
    name = "maintainer-list"
    permission_classes = [IsMaintainer]
    serializer_class = MaintainerSerializer

    def get_queryset(self):
        maintainer = Maintainer.objects.filter(user=self.request.user)
        return maintainer

class MaintainerView(RetrieveUpdateDestroyAPIView):
    name = "maintainer"
    permission_classes = [IsMaintainer]
    queryset = Maintainer.objects.all()
    serializer_class = MaintainerSerializer
    lookup_url_kwarg = "maintainer_id"

    def get_queryset(self):
        match self.request.method:
            case "GET" | "PUT" | "PATCH" | "DELETE":
                return Maintainer.objects.filter(user=self.request.user)
            case _:
               return Maintainer.objects.none()


class MaintainerSQLView(APIView):
    name = "maintainer-sql"
    permission_classes = [IsMaintainer]

    def post(self, request):
        query = request.data["query"]

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        return Response(result)
