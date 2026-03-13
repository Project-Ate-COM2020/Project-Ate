from argon2 import PasswordHasher
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from ..models import Consumer, ConsumerSerializer, RegisterConsumerSerializer


class CreateConsumerView(CreateAPIView):
    name = "consumer-create"
    queryset = Consumer
    serializer_class = RegisterConsumerSerializer
    permission_classes = [IsAuthenticated]


class ConsumerView(RetrieveUpdateDestroyAPIView):
    name = "consumer"
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    # permission_classes = [IsAuthenticated]
