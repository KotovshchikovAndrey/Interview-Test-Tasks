import datetime
import typing as tp
from abc import ABC, abstractmethod

import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from auth_app.models import Token


class ITokenService(ABC):
    @abstractmethod
    def set_token(self, user, token) -> None:
        raise NotImplementedError()

    @abstractmethod
    def update_token_in_db(self, user_id, old_token, new_token) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete_token_from_db(self, user, token):
        raise NotImplementedError()

    @abstractmethod
    def decode_token(self, token) -> tp.Dict[str, tp.Any]:
        raise NotImplementedError()

    @abstractmethod
    def generate_access_token(self, payload) -> tp.Dict[str, tp.Any]:
        raise NotImplementedError()

    @abstractmethod
    def generate_refresh_token(self, payload) -> tp.Dict[str, tp.Any]:
        raise NotImplementedError()


class TokenService(ITokenService):
    def set_token(self, user, token):
        Token.objects.create(user=user, value=token)
        return

    def update_token_in_db(self, user_id, old_token, new_token):
        token_in_db = Token.objects.filter(user__id=user_id, value=old_token).first()
        if token_in_db is None:
            raise AuthenticationFailed("Токен не найден!")

        token_in_db.value = new_token
        token_in_db.save(update_fields=["value"])

        return

    def delete_token_from_db(self, user, token):
        Token.objects.filter(user=user, value=token).delete()
        return

    def decode_token(self, token):
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=["HS256"],
            )
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Невалидный Токен!")

        return payload

    def generate_access_token(self, payload):
        token_time = datetime.datetime.now(
            tz=datetime.timezone.utc
        ) + datetime.timedelta(minutes=30)

        payload.update(exp=token_time)

        token = jwt.encode(
            payload=payload,
            key=settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token

    def generate_refresh_token(self, payload):
        token_time = datetime.datetime.now(
            tz=datetime.timezone.utc
        ) + datetime.timedelta(days=30)

        payload.update(exp=token_time)

        token = jwt.encode(
            payload=payload,
            key=settings.SECRET_KEY,
            algorithm="HS256",
        )

        return token


def get_token_service() -> ITokenService:
    return TokenService()
