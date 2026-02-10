from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    ValidationError,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from models import Seller
from argon2 import PasswordHasher


class SellerTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        ph = PasswordHasher()

        hpassword = ph.hash(password)

        if not (Seller.objects.filter(username=username, password=hpassword).exists()):
            raise ValidationError({"invalid": "password"})

        return super().validate(attrs)


class SellerTokenObtainPairView(TokenObtainPairView):
    serializer_class = SellerTokenObtainPairSerializer
