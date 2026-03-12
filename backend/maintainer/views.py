import json

from django.shortcuts import render
from .models import Maintainer, MaintainerSerializer, MaintainerWithPasswordSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from django.db import connection

class CreateMaintainerView(CreateAPIView):
    name = "maintainer-create"
    queryset = Maintainer
    serializer_class = MaintainerWithPasswordSerializer

class MaintainerView(RetrieveUpdateDestroyAPIView):
    name = "maintainer"
    queryset = Maintainer.objects.all()
    serializer_class = MaintainerSerializer


class MaintainerSQLView(APIView):
    name = "maintainer-sql"

    def post(self, request):
        query = request.data['query']

        with connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        return json.dumps(result)
