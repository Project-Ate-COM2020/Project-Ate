from authentication.tests import setup_random_user, get_authorization_headers_for_user
from .bundles import *
from .reservations import *
from .seller import *
from .consumer import *

from rest_framework.test import APITestCase


class PasswordHashingTests(APITestCase):
    def setUp(self):
        self.user = setup_random_user()

        self.headers = get_authorization_headers_for_user(self.user)

    def test_password_got_hashed(self):
        self.assertNotEqual(self.user.password, "test")
