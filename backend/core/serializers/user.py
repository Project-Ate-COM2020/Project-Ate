from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "email",
            "password",
            "username",
            "first_name",
            "last_name",
        ]

    def create(self, validated_data):
        password = self.validated_data["password"]
        groups = validated_data.pop("groups", [])
        user_permissions = validated_data.pop("user_permissions", [])

        user = self.Meta.model(**validated_data)

        user.set_password(password)

        user.is_active = True

        user.save()

        if groups:
            user.groups.set(groups)

        if user_permissions:
            user.user_permissions.set(user_permissions)

        return user
