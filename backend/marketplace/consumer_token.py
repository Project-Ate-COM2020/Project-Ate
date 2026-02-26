from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    ValidationError,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Consumer
from argon2 import PasswordHasher


class ConsumerTokenPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        try:
            consumer = Consumer.objects.get(display_name=username)
        except Consumer.DoesNotExist:
            raise ValidationError(
                {"username": "This field must be a valid consumers username."}
            )

        ph = PasswordHasher()

        try:
            ph.verify(consumer.password, password)
        except Exception as e:
            raise ValidationError({"password": "invalid password"})

        return super().validate(attrs)


class ConsumerTokenObtainPairView(TokenObtainPairView):
    serializer = ConsumerTokenPairSerializer()
