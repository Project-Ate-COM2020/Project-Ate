from rest_framework.generics import CreateAPIView
from .permissions import *

from .models import User, UserSerializer, RegisterUserSerializer
from rest_framework.views import APIView

class UserCreateView(CreateAPIView):
    name = "user-create"
    queryset = User
    serializer_class = RegisterUserSerializer

class MaintainerView(APIView):
    name = "test-maintainer"
    permission_classes = [IsMaintainer]

    def get(self, request):
        return True

class SellerView(APIView):
    name = "test-seller"
    permission_classes = [IsSeller]

    def get(self, request):
        return True

class ConsumerView(APIView):
    name="test-consumer"
    permission_classes = [IsConsumer]

    def get(self, request):
        return True

class ConsumerOrSellerView(APIView):
    name="test-consumer-or-seller"
    permission_classes = [IsConsumerOrSeller]

    def get(self, request):
        return True

class ConsumerAndSellerView(APIView):
    name="test-consumer-and-seller"
    permission_classes = [IsConsumerAndSeller]

    def get(self, request):
        return True

class MaintainerOrSellerView(APIView):
    name = "test-maintainer-or-seller"
    permission_classes = [IsMaintainerOrSeller]

    def get(self, request):
        return True

class MaintainerAndSellerView(APIView):
    name="test-maintainer-and-seller"
    permission_classes = [IsMaintainerAndSeller]

    def get(self, request):
        return True

class MaintainerOrConsumerView(APIView):
    name="test-maintainer-or-consumer"
    permission_classes = [IsMaintainerOrConsumer]

    def get(self, request):
        return True

class MaintainerAndConsumerView(APIView):
    name="test-maintainer-and-consumer"
    permission_classes = [IsMaintainerAndConsumer]

    def get(self, request):
        return True

class MaintainerAndConsumerAndSellerView(APIView):
    name="test-maintainer-and-consumer-and-seller"
    permission_classes = [IsMaintainerAndConsumerAndSeller]

    def get(self, request):
        return True

class MaintainerOrConsumerOrSellerView(APIView):
    name="test-maintainer-or-consumer-or-seller"
    permission_classes = [IsMaintainerOrConsumerOrSeller]

    def get(self, request):
        return True