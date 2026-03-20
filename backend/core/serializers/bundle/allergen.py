from rest_framework import serializers

from core.models import Allergen


class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ["allergen_id", "name"]
