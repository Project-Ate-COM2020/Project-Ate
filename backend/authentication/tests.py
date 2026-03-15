import random
import string
from typing import Tuple, Any, Dict, Union

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse

from .permissions import IsSeller
from .views import *

from marketplace.views import CreateSellerView
from marketplace.views import CreateBundleView, CreateReservationView

from .token import UserTokenObtainPairSerializer
from core.models import User, Seller, Consumer, Maintainer

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



def get_random_string(k=10) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=k))

def random_user_args() -> Dict[str, Any]:
    random_string = get_random_string(10)

    random_email = f'{random_string}@{random_string}.com'

    random_password = get_random_string(10)

    user_args = {
        "username": random_string,
        "email": random_email,
        "password": random_password,
    }

    return user_args

def random_seller_args() -> Dict[str, Any]:
    name = get_random_string(10)
    location = get_random_string(6)
    opening_hours = get_random_string(8)
    contact_stub = get_random_string(7)

    seller_args = {
        "name": name,
        "location": location,
        "opening_hours": opening_hours,
        "contact_stub": contact_stub,
    }

    return seller_args

def random_consumer_args() -> Dict[str, Any]:
    display_name = get_random_string(10)
    streak = random.randint(1, 10)

    consumer_args = {
        "display_name": display_name,
        "streak": streak,
    }

    return consumer_args

def random_maintainer_args() -> Dict[str, Any]:
    return {}

class RandomMarker:
    pass

# helper functions that generate every permutation of permission
# where or is used like isMaintainerOrSeller it generates both possibilities

def setup_base_user(**kwargs) -> User:
    user_model = get_user_model()

    return user_model.objects.create_user(**kwargs)

def make_user_seller(user: User, **kwargs: Any) -> Seller:
    return Seller.objects.create(user=user, **kwargs)

def make_user_consumer(user: User, **kwargs: Any) -> Consumer:
    return Consumer.objects.create(user=user, **kwargs)

def make_user_maintainer(user: User, **kwargs: Any) -> Maintainer:
    return Maintainer.objects.create(user=user, **kwargs)

def setup_seller(user_args: Dict[str, Any], seller_args: Dict[str, Any]) -> Tuple[User, Seller]:
    user = setup_base_user(**user_args)
    seller = make_user_seller(user, **seller_args)

    return user, seller

def setup_consumer(user_args: Dict[str, Any], consumer_args: Dict[str, Any]) -> Tuple[User, Consumer]:
    user = setup_base_user(**user_args)
    consumer = make_user_consumer(user, **consumer_args)

    return user, consumer

def setup_maintainer(user_args: Dict[str, Any], maintainer_args: Dict[str, Any]) -> Tuple[User, Maintainer]:
    user = setup_base_user(**user_args)
    maintainer = make_user_maintainer(user, **maintainer_args)

    return user, maintainer

def setup_consumer_and_seller(user_args: Dict[str, Any], consumer_args: Dict[str, Any], seller_args: Dict[str, Any]) -> Tuple[User, Consumer, Seller]:
    user = setup_base_user(**user_args)
    seller = make_user_seller(user, **seller_args)
    consumer = make_user_consumer(user, **consumer_args)

    return user, consumer, seller

def setup_consumer_or_seller(consumer_args: Dict[str, Any], seller_args: Dict[str, Any]) -> Tuple[Tuple[User, Consumer], Tuple[User, Seller]]:
    return setup_consumer(**consumer_args), setup_seller(**seller_args)

def setup_maintainer_and_seller(user_args: Dict[str, Any], maintainer_args: Dict[str, Any], seller_args: Dict[str, Any]) -> Tuple[User, Maintainer, Seller]:
    user = setup_base_user(**user_args)
    maintainer = make_user_maintainer(user, **maintainer_args)
    seller = make_user_seller(user, **seller_args)
    return user, maintainer, seller

def setup_maintainer_or_seller(maintainer_args: Dict[str, Any], seller_args: Dict[str, Any]) -> Tuple[Tuple[User, Maintainer], Tuple[User, Seller]]:
    return setup_maintainer(**maintainer_args), setup_seller(**seller_args)

def setup_maintainer_and_consumer(user_args: Dict[str, Any], maintainer_args: Dict[str, Any], consumer_args: Dict[str, Any]) -> Tuple[User, Maintainer, Consumer]:
    user = setup_base_user(**user_args)
    consumer = make_user_consumer(user, **consumer_args)
    maintainer = make_user_maintainer(user, **maintainer_args)
    return user, maintainer, consumer

def setup_maintainer_or_consumer(maintainer_args: Dict[str, Any], consumer_args: Dict[str, Any]) -> Tuple[Tuple[User, Maintainer], Tuple[User, Consumer]]:
    return setup_maintainer(**maintainer_args), setup_consumer(**consumer_args)

def setup_maintainer_or_consumer_or_seller(maintainer_args: Dict[str, Any], consumer_args: Dict[str, Any], seller_args: Dict[str, Any]) -> Tuple[Tuple[User, Maintainer], Tuple[User, Consumer], Tuple[User, Seller]]:
    return setup_maintainer(**maintainer_args), setup_consumer(**consumer_args), setup_seller(**seller_args)

def setup_maintainer_and_consumer_and_seller(user_args: Union[Dict[str, Any], RandomMarker], maintainer_args: Dict[str, Any], consumer_args: Dict[str, Any], seller_args: Dict[str, Any]) -> Tuple[User, Maintainer, Consumer, Seller]:
    user = setup_base_user(**user_args)
    consumer = make_user_consumer(user, **consumer_args)
    maintainer = make_user_maintainer(user, **maintainer_args)
    seller = make_user_seller(user, **seller_args)
    return user, maintainer, consumer, seller

def setup_random_user():
    return setup_base_user(**random_user_args())

def setup_random_seller() -> Tuple[User, Seller]:
    user = setup_random_user()
    r = random_seller_args()
    seller = make_user_seller(user, **r)
    return user, seller

def setup_random_consumer() -> Tuple[User, Consumer]:
    user = setup_random_user()
    r = random_consumer_args()
    consumer = make_user_consumer(user, **r)
    return user, consumer

def setup_random_maintainer() -> Tuple[User, Maintainer]:
    user = setup_random_user()
    r = random_maintainer_args()
    maintainer = make_user_maintainer(user, **r)
    return user, maintainer

def setup_random_consumer_or_seller():
    return setup_random_consumer(), setup_random_seller()

def setup_random_consumer_and_seller():
    user = setup_random_user()
    r_consumer = random_consumer_args()
    consumer = make_user_consumer(user, **r_consumer)
    r_seller = random_seller_args()
    seller = make_user_seller(user, **r_seller)
    return user, consumer, seller

def setup_random_maintainer_and_seller():
    user = setup_random_user()
    r_maintainer = random_maintainer_args()
    maintainer = make_user_maintainer(user, **r_maintainer)
    r_seller = random_seller_args()
    seller = make_user_seller(user, **r_seller)
    return user, maintainer, seller

def setup_random_maintainer_or_seller():
    return setup_random_maintainer(), setup_random_seller()

def setup_random_maintainer_or_consumer():
    return setup_random_maintainer(), setup_random_consumer()

def setup_random_maintainer_and_consumer():
    user = setup_random_user()
    r_consumer = random_consumer_args()
    consumer = make_user_consumer(user, **r_consumer)
    r_maintainer = random_maintainer_args()
    maintainer = make_user_maintainer(user, **r_maintainer)
    return user, maintainer, consumer

def setup_random_maintainer_or_consumer_or_seller():
    return setup_random_maintainer(), setup_random_consumer(), setup_random_seller()

def setup_random_maintainer_and_consumer_and_seller():
    user = setup_random_user()
    r_consumer = random_consumer_args()
    consumer = make_user_consumer(user, **r_consumer)
    r_maintainer = random_maintainer_args()
    maintainer = make_user_maintainer(user, **r_maintainer)
    r_seller = random_seller_args()
    seller = make_user_seller(user, **r_seller)
    return user, maintainer, consumer, seller

def get_authorization_headers_for_user(user):
    token = UserTokenObtainPairSerializer.get_token(user).access_token

    return {"Authorization": f"Bearer {token}"}

class TestMaintainerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(MaintainerView.name)

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_only_maintainer_can_access(self):
        user, _ = setup_random_maintainer()
        self.expect_ok(user)

    def test_only_seller_cannot_access(self):
        user, _ = setup_random_seller()
        self.expect_forbidden(user)

    def test_only_consumer_cannot_access(self):
        user, _ = setup_random_consumer()
        self.expect_forbidden(user)

    def test_maintainer_and_consumer_can_access(self):
        user, _, _ = setup_random_maintainer_and_consumer()
        self.expect_ok(user)

    def test_maintainer_and_seller_can_access(self):
        user, _, _ = setup_random_maintainer_and_seller()
        self.expect_ok(user)

    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)

class TestSellerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(SellerView.name)

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_only_maintainer_cannot_access(self):
        user, _  = setup_random_maintainer()
        self.expect_forbidden(user)

    def test_only_seller_can_access(self):
        user, _ = setup_random_seller()
        self.expect_ok(user)

    def test_only_consumer_cannot_access(self):
        user, _ = setup_random_consumer()
        self.expect_forbidden(user)

    def test_maintainer_and_seller_can_access(self):
        user, _, _ = setup_random_maintainer_and_seller()
        self.expect_ok(user)


    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)

class TestConsumerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(ConsumerView.name)

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_only_maintainer_cannot_access(self):
        user, _ = setup_random_maintainer()
        self.expect_forbidden(user)

    def test_only_seller_cannot_access(self):
        user, _ = setup_random_seller()
        self.expect_forbidden(user)

    def test_only_consumer_can_access(self):
        user, _ = setup_random_consumer()
        self.expect_ok(user)

    def test_maintainer_and_seller_cannot_access(self):
        user, _, _ = setup_random_maintainer_and_seller()
        self.expect_forbidden(user)

    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)

class TestConsumerOrSellerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(ConsumerOrSellerView.name)

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_only_maintainer_cannot_access(self):
        user, _ = setup_random_maintainer()
        self.expect_forbidden(user)

    def test_only_seller_can_access(self):
        user, _ = setup_random_seller()
        self.expect_ok(user)

    def test_only_consumer_can_access(self):
        user, _ = setup_random_consumer()
        self.expect_ok(user)

    def test_maintainer_and_seller_can_access(self):
        user, _, _ = setup_random_maintainer_and_seller()
        self.expect_ok(user)

    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)

class TestConsumerAndSellerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(ConsumerAndSellerView.name)

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_only_maintainer_cannot_access(self):
        user, _ = setup_random_maintainer()
        self.expect_forbidden(user)

    def test_only_seller_cannot_access(self):
        user, _ = setup_random_seller()
        self.expect_forbidden(user)

    def test_only_consumer_cannot_access(self):
        user, _ = setup_random_consumer()
        self.expect_forbidden(user)

    def test_consumer_and_seller_can_access(self):
        user, _, _ = setup_random_consumer_and_seller()
        self.expect_ok(user)

    def test_maintainer_and_seller_cannot_access(self):
        user, _, _ = setup_random_maintainer_and_seller()
        self.expect_forbidden(user)

    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)

class TestMaintainerOrConsumerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(MaintainerOrConsumerView.name)

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_only_maintainer_can_access(self):
        user, _ = setup_random_maintainer()
        self.expect_ok(user)

    def test_only_seller_cannot_access(self):
        user, _ = setup_random_seller()
        self.expect_forbidden(user)

    def test_only_consumer_can_access(self):
        user, _ = setup_random_consumer()
        self.expect_ok(user)

    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)

class TestMaintainerAndConsumerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(MaintainerAndConsumerView.name)

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_only_maintainer_cannot_access(self):
        user, _ = setup_random_maintainer()
        self.expect_forbidden(user)

    def test_only_seller_cannot_access(self):
        user, _ = setup_random_seller()
        self.expect_forbidden(user)

    def test_only_consumer_cannot_access(self):
        user, _ = setup_random_consumer()
        self.expect_forbidden(user)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)

class TestMaintainerOrSellerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(MaintainerOrSellerView.name)
        pass

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_only_maintainer_can_access(self):
        user, _ = setup_random_maintainer()
        self.expect_ok(user)

    def test_only_seller_can_access(self):
        user, _ = setup_random_seller()
        self.expect_ok(user)

    def test_only_consumer_cannot_access(self):
        user, _ = setup_random_consumer()
        self.expect_forbidden(user)

    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)

class TestMaintainerAndConsumerAndSellerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(MaintainerAndConsumerAndSellerView.name)
        pass

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_only_maintainer_cannot_access(self):
        user, _ = setup_random_maintainer()
        self.expect_forbidden(user)

    def test_only_seller_cannot_access(self):
        user, _ = setup_random_seller()
        self.expect_forbidden(user)

    def test_only_consumer_cannot_access(self):
        user, _ = setup_random_consumer()
        self.expect_forbidden(user)

    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)

class TestMaintainerOrSellerOrConsumerPermission(APITestCase):
    def setUp(self):
        self.url = reverse(MaintainerOrConsumerOrSellerView.name)
        pass

    def expect_forbidden(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def expect_ok(self, user):
        headers = get_authorization_headers_for_user(user)

        response = self.client.get(self.url, headers=headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_base_user_cannot_access(self):
        self.expect_forbidden(setup_random_user())

    def test_only_maintainer_can_access(self):
        user, _ = setup_random_maintainer()
        self.expect_ok(user)

    def test_only_seller_can_access(self):
        user, _ = setup_random_seller()
        self.expect_ok(user)

    def test_only_consumer_can_access(self):
        user, _ = setup_random_consumer()
        self.expect_ok(user)

    def test_maintainer_and_consumer_and_seller_can_access(self):
        user, _, _, _ = setup_random_maintainer_and_consumer_and_seller()
        self.expect_ok(user)
