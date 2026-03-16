import json

from django.shortcuts import render

from .models import Maintainer, MaintainerSerializer, RegisterMaintainerSerializer
from authentication.permissions import IsMaintainer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from django.db import connection
from rest_framework.response import Response


class CreateMaintainerView(CreateAPIView):
    name = "maintainer-create"
    queryset = Maintainer.objects.all()
    serializer_class = RegisterMaintainerSerializer
    permission_classes = [IsMaintainer]


class MaintainerView(RetrieveUpdateDestroyAPIView):
    name = "maintainer"
    permission_classes = [IsMaintainer]
    queryset = Maintainer.objects.all()
    serializer_class = MaintainerSerializer
    lookup_url_kwarg = "maintainer_id"

class MaintainerSQLView(APIView):
    name = "maintainer-sql"
    permission_classes = [IsMaintainer]

    def post(self, request):
        query = request.data["query"]

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        return Response(result)
