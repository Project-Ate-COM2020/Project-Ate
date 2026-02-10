from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from backend.marketplace.models import Consumer, ConsumerSerializer


class CreateConsumerView(CreateAPIView):
    name = "consumer-create"
    queryset = Consumer
    serializer_class = ConsumerSerializer


class ConsumerView(RetrieveUpdateDestroyAPIView):
    name = "consumer"
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
