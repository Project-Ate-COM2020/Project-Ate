from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    ValidationError,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Seller
from argon2 import PasswordHasher


class SellerTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            seller = Seller.objects.get(name=username)
        except Seller.DoesNotExist:
            raise ValidationError(
                {"username": ["This field must be a valid sellers username"]}
            )

        ph = PasswordHasher()

        try:
            ph.verify(seller.password, password)
        except Exception as e:
            raise ValidationError({"password": "invalid password"})

        return super().validate(attrs)


class SellerTokenObtainPairView(TokenObtainPairView):
    serializer_class = SellerTokenObtainPairSerializer
