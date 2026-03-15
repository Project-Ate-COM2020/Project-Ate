from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .permissions import *

from .models import User, UserSerializer, RegisterUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN
from .throttling import UserCreationThrottling

class UserCreateView(CreateAPIView):
    name = "user-create"
    throttle_classes = [UserCreationThrottling]
    queryset = User
    serializer_class = RegisterUserSerializer

class UpdatePasswordView(APIView):
    name = "update-password"
    permission_classes = [IsAuthenticated]

    def post(self, request):
        new_password = request.data["new_password"]

        request.user.set_password(new_password)

        request.user.save()

        return Response({}, status=HTTP_200_OK)


class MaintainerView(APIView):
    name = "test-maintainer"
    permission_classes = [IsMaintainer]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class SellerView(APIView):
    name = "test-seller"
    permission_classes = [IsSeller]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class ConsumerView(APIView):
    name="test-consumer"
    permission_classes = [IsConsumer]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class ConsumerOrSellerView(APIView):
    name="test-consumer-or-seller"
    permission_classes = [IsConsumerOrSeller]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class ConsumerAndSellerView(APIView):
    name="test-consumer-and-seller"
    permission_classes = [IsConsumerAndSeller]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class MaintainerOrSellerView(APIView):
    name = "test-maintainer-or-seller"
    permission_classes = [IsMaintainerOrSeller]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class MaintainerAndSellerView(APIView):
    name="test-maintainer-and-seller"
    permission_classes = [IsMaintainerAndSeller]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class MaintainerOrConsumerView(APIView):
    name="test-maintainer-or-consumer"
    permission_classes = [IsMaintainerOrConsumer]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class MaintainerAndConsumerView(APIView):
    name="test-maintainer-and-consumer"
    permission_classes = [IsMaintainerAndConsumer]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class MaintainerAndConsumerAndSellerView(APIView):
    name="test-maintainer-and-consumer-and-seller"
    permission_classes = [IsMaintainerAndConsumerAndSeller]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)

class MaintainerOrConsumerOrSellerView(APIView):
    name="test-maintainer-or-consumer-or-seller"
    permission_classes = [IsMaintainerOrConsumerOrSeller]

    def get(self, request):
        return Response({}, status=HTTP_200_OK)