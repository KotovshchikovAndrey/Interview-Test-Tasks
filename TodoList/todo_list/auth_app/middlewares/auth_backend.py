import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthenticationBackend(authentication.BaseAuthentication):
    def authenticate(self, request):
        authorization = request.headers.get("authorization")
        if not authorization:
            raise AuthenticationFailed("Токен не был получен!")

        access_token = authorization.split()[-1]
        if not access_token:
            raise AuthenticationFailed("Неверный Токен!")

        return self.authenticate_credentials(request, access_token)

    def authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Невалидный Токен!")

        current_user = get_user_model().objects.filter(id=payload["id"]).first()
        if current_user is None:
            raise AuthenticationFailed("Пользователь не найден!")

        return current_user, token
