from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False

        return token.get("seller_id") is not None

class IsConsumer(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False

        return token.get("consumer_id") is not None


class IsConsumerOrSeller(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False

        return (token.get("seller_id") is not None) or (token.get("consumer_id") is not None)

class IsConsumerAndSeller(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False

        return (token.get("seller_id") is not None) and (token.get("consumer_id") is not None)