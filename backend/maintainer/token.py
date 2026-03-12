
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView
from argon2 import PasswordHasher
from .models import Maintainer, MaintainerSerializer, MaintainerWithPasswordSerializer


class MaintainerTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
            maintainer = Maintainer.objects.get(name=username)
        except Maintainer.DoesNotExist:
            raise ValidationError(
                {"username": ["This field must be a valid maintainers username"]}
            )

        ph = PasswordHasher()

        try:
            ph.verify(maintainer.password, password)
        except Exception as e:
            raise ValidationError({"password": "invalid password"})

        return super().validate(attrs)


class MaintainerTokenObtainPairView(TokenObtainPairView):
    serializer_class = MaintainerTokenObtainPairSerializer

