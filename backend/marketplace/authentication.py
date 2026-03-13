from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from .models import Consumer


class ConsumerJWTAuthentication(JWTAuthentication):
    """
    Allow JWTs that carry `consumer_id` to authenticate as marketplace.Consumer.
    """

    def get_user(self, validated_token):
        consumer_id = validated_token.get("consumer_id")

        if consumer_id is None:
            raise AuthenticationFailed(
                "Token contained no recognizable user identification"
            )

        try:
            return Consumer.objects.get(id=consumer_id)
        except Consumer.DoesNotExist:
            raise AuthenticationFailed("Consumer not found")

