from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate
from django.urls import reverse

from .views import UserCreateView

from marketplace.views import CreateSellerView

class UserTokenTest(APITestCase):
    def setUp(self):
        create_user_url = reverse(UserCreateView.name)

        self.username = "testuser"
        self.password = "pass"

        user_data = {
            "password": self.password,
            "username": self.username,
            "email": "testemail@testuser.com",
            "first_name": "testuser",
            "last_name": "testuser",
        }

        self.user = self.client.post(create_user_url, user_data, format="json")

        json = self.user.json()

        self.user_id = json["id"]

        token_url = reverse("user-token")

        data = {
            "username": self.username,
            "password": self.password,
        }

        response = self.client.post(token_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token_obtain_response = response.json()



    def test_tokens_are_returned(self):
        self.assertIsNotNone(self.token_obtain_response["access"])
        self.assertIsNotNone(self.token_obtain_response["refresh"])

    def test_token_can_create_seller(self):
        create_seller_url = reverse(CreateSellerView.name)

        data = {
            "name": "seller",
            "contact_stub": "53636",
            "user_id": self.user_id,
            "location": "exeter",
        }

        authorization_string = f"Bearer {self.token_obtain_response["access"]}"

        response = self.client.post(create_seller_url, data, format="json", headers={"AUTHORIZATION": authorization_string})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # No token
        response = self.client.post(create_seller_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

