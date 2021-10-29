from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model


class FakeAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            user = get_user_model().objects.get(username="buyer1")
        except get_user_model().DoesNotExist():
            raise Exception("Mock user not found")
        return user, None
