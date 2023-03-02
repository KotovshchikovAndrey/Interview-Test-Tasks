from django.urls import reverse
from rest_framework.test import APITestCase

from auth_app.models import User
from todo_app.models import Task


class AuthViewSetTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        user_owner = User.objects.create(email="test@mail.ru")
        user_owner.set_password("12345")
        user_owner.save()

        any_user = User.objects.create(email="test2@mail.ru")
        any_user.set_password("12345")
        any_user.save()

        Task.objects.create(title="testTitle", description="testDesc", user=user_owner)

    def test_forbidden(self):
        owner_data = {"email": "test@mail.ru", "password": 12345}
        any_user_data = {"email": "test2@mail.ru", "password": 12345}

        owner_response = self.client.post("/auth/login/", data=owner_data).json()
        owner_token = owner_response["access_token"]

        any_user_response = self.client.post("/auth/login/", data=any_user_data).json()
        any_user_token = any_user_response["access_token"]

        owner_task_response = self.client.get(
            "/todo/1/",
            HTTP_AUTHORIZATION=owner_token,
        )
        any_user_task_response = self.client.get(
            "/todo/1/",
            HTTP_AUTHORIZATION=any_user_token,
        )

        self.assertEqual(owner_task_response.status_code, 200)
        self.assertEqual(any_user_task_response.status_code, 403)
