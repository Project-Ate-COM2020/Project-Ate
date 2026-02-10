from argon2 import PasswordHasher
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from ..models import Consumer, ConsumerSerializer


class CreateConsumerView(CreateAPIView):
    name = "consumer-create"
    queryset = Consumer
    serializer_class = ConsumerSerializer

    def post(self, request, *args, **kwargs):
        password = request.data.get("password")

        ph = PasswordHasher()

        hashed_password = ph.hash(password)

        request.data["password"] = hashed_password

        return super().post(request, *args, **kwargs)


class ConsumerView(RetrieveUpdateDestroyAPIView):
    name = "consumer"
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    authentication_classes = [IsAuthenticated]
