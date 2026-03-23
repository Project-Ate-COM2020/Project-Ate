from rest_framework.throttling import AnonRateThrottle

class UserCreationThrottling(AnonRateThrottle):
    scope = "user_creation"