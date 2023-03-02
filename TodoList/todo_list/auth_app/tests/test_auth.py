from django.urls import reverse
from rest_framework.test import APITestCase

from auth_app.models import User


class AuthViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create(email="test@mail.ru")
        user.set_password("12345")
        user.save()

    def test_incorrect_register(self):
        data = {"email": "testEmailmail.ru", "password": "12345"}
        response = self.client.post("/auth/register/", data=data)
        self.assertEqual(response.status_code, 400)

    def test_correct_register(self):
        data = {"email": "testEmail@mail.ru", "password": "12345"}

        response = self.client.post("/auth/register/", data=data)
        self.assertEqual(response.status_code, 201)

        response_data_keys = [key for key in response.json()]
        self.assertEqual(response_data_keys, ["access_token", "refresh_token"])

    def test_incorrect_login(self):
        data = {"email": "testHNS@mail.ru"}

        response = self.client.post("/auth/login/", data=data)
        self.assertEqual(response.status_code, 400)

        data = {"email": "test@mail.ru", "password": 1234}

        response = self.client.post("/auth/login/", data=data)
        self.assertEqual(response.status_code, 403)

    def test_correct_login(self):
        data = {"email": "test@mail.ru", "password": 12345}

        response = self.client.post("/auth/login/", data=data)
        self.assertEqual(response.status_code, 200)
