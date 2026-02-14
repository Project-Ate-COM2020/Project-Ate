from argon2 import PasswordHasher
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from ..models import Consumer
from ..serializers import ConsumerSerializer, ConsumerWithPasswordSerializer

class CreateConsumerView(CreateAPIView):
    name = "consumer-create"
    queryset = Consumer
    serializer_class = ConsumerWithPasswordSerializer


class ConsumerView(RetrieveUpdateDestroyAPIView):
    name = "consumer"
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    permission_classes = [IsAuthenticated]
