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

class IsMaintainer(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False

        return (token.get("maintainer_id") is not None)

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

class IsMaintainerOrConsumer(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False


        return (token.get("maintainer_id") is not None) or (token.get("consumer_id") is not None)

class IsMaintainerAndConsumer(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False


        return (token.get("maintainer_id") is not None) and (token.get("consumer_id") is not None)

class IsMaintainerOrSeller(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False


        return (token.get("maintainer_id") is not None) or (token.get("seller_id") is not None)

class IsMaintainerAndSeller(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False


        return (token.get("maintainer_id") is not None) and (token.get("consumer_id") is not None)

class IsMaintainerAndConsumerAndSeller(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False


        return (token.get("maintainer_id") is not None) and (token.get("consumer_id") is not None) and (token.get("seller_id") is not None)

class IsMaintainerOrConsumerAndSeller(BasePermission):
    def has_permission(self, request, view):
        token = request.auth

        if token is None:
            return False


        return (token.get("maintainer_id") is not None) or (token.get("consumer_id") is not None) or (token.get("seller_id") is not None)
