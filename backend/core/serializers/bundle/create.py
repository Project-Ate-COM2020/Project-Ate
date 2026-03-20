from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import BundlePosting, Seller


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundlePosting
        fields = [
            "posting_id",
            "category",
            "contents",
            "quantity",
            "quantity_remaining",
            "price",
            "pickup_window",
            "status",
            "created_at",
            "updated_at",
        ]

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

        seller = Seller.objects.get(user=user)

        posting = BundlePosting.objects.create(seller=seller, **validated_data)

        return posting
