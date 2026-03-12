from rest_framework.generics import CreateAPIView

from .models import User, UserSerializer, RegisterUserSerializer


class UserCreateView(CreateAPIView):
    name = "user-create"
    queryset = User
    serializer_class = RegisterUserSerializer
