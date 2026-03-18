from rest_framework import serializers

from core.models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["consumer_id", "display_name", "streak"]


class RegisterConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = ["consumer_id", "display_name", "streak"]

    def create(self, validated_data):
        request = self.context["request"]

        user = request.user

        consumer = Consumer.objects.create(user=user, **validated_data)

        return consumer
