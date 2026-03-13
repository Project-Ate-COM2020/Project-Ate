from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.models import Seller
from core.models import Consumer


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['user_id'] = user.id

        try:
            seller = Seller.objects.get(user=user)

            token['seller_id'] = seller.pk
        except Seller.DoesNotExist:
            token['seller_id'] = -1

        try:
            consumer = Consumer.objects.get(user=user)

            token['consumer_id'] = consumer.pk
        except Consumer.DoesNotExist:
            token['consumer_id'] = -1


        return token


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer