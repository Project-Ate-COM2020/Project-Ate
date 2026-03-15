from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.test import force_authenticate
from django.urls import reverse

from .permissions import IsSeller
from .views import UserCreateView

from marketplace.views import CreateSellerView
from marketplace.views import CreateBundleView, CreateReservationView



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

class TestIsSellerPermission(APITestCase):
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


    def test_user_cannot_access(self):
        url = reverse(CreateBundleView.name)

        response = self.client.post(url, {}, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_seller_protected_viewpoint(self):
        # create bundle is a seller protected view

        create_seller_url = reverse(CreateSellerView.name)

        data = {
            "name": "seller",
            "contact_stub": "53636",
            "user_id": self.user_id,
            "location": "exeter",
        }

        authorization_string = f"Bearer {self.token_obtain_response["access"]}"

        self.authorization_headers = {"AUTHORIZATION": authorization_string}

        seller_creation_response = self.client.post(create_seller_url, data, format="json", headers=self.authorization_headers)

        self.assertEqual(seller_creation_response.status_code, status.HTTP_201_CREATED)

        # refresh the token to clarify we are a seller
        url = reverse("token-refresh")

        refresh = self.client.post(url, {"refresh": self.token_obtain_response["refresh"]}, format="json")

        # update access token
        self.token_obtain_response["access"] = refresh.json()["access"]

        url = reverse(CreateBundleView.name)

        authorization_string = f"Bearer {self.token_obtain_response["access"]}"

        self.authorization_headers = {"AUTHORIZATION": authorization_string}

        response = self.client.post(url, {}, format="json", headers=self.authorization_headers)

        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class TestMaintainerPermission(APITestCase):
    def setUp(self):
        pass

class TestSellerPermission(APITestCase):
    def setUp(self):
        pass

class TestConsumerPermission(APITestCase):
    def setUp(self):
        pass

class TestConsumerOrSellerPermission(APITestCase):
    def setUp(self):
        pass

class TestConsumerAndSellerPermission(APITestCase):
    def setUp(self):
        pass

class TestMaintainerOrConsumerPermission(APITestCase):
    def setUp(self):
        pass

class TestMaintainerAndConsumerPermission(APITestCase):
    def setUp(self):
        pass

class TestMaintainerAndSellerPermission(APITestCase):
    def setUp(self):
        pass

class TestMaintainerOrSellerPermission(APITestCase):
    def setUp(self):
        pass

class TestMaintainerAndSellerAndConsumerPermission(APITestCase):
    def setUp(self):
        pass

class TestMaintainerOrSellerOrConsumerPermission(APITestCase):
    def setUp(self):
        pass

