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

        ph = PasswordHasher()

        hashed_password = ph.hash(password)

        if not Consumer.objects.filter(
            username=username, password=hashed_password
        ).exists():
            raise ValidationError({"username": "Invalid username and/or password."})

        return super().validate(attrs)


class ConsumerTokenObtainPairView(TokenObtainPairView):
    serializer = ConsumerTokenPairSerializer()
