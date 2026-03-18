from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import Maintainer, Seller


class MaintainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintainer
        fields = ["maintainer_id"]


class RegisterMaintainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintainer
        fields = "maintainer_id"

    def create(self, validated_data):
        context = self.context

        if context is None:
            raise ValidationError(
                {
                    f"no context passed to {self.__class__.__name__}",
                    "please provide context to this serializer",
                }
            )

        request = context["request"]

        if request is None:
            raise ValidationError(
                {
                    f"serializer context key 'request' given to {self.__class__.__name__} is None": "please provide the request as context to this serializer"
                }
            )

        user = request.user

        seller = Seller.objects.create(user=user, **validated_data)

        return seller
