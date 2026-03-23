from rest_framework import serializers

from core.models import Badges, BadgeMapping


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badges
        fields = "__all__"


class BadgeMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BadgeMapping
        fields = "__all__"
