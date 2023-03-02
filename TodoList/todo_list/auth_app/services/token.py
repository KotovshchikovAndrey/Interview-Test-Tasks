import datetime

import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

from auth_app.models import RepositoryFactory, Token


class TokenService:
    def __init__(self) -> None:
        self.repository = RepositoryFactory.get_repository("TokenRepository")

    def set_token(self, user, token):
        self.repository.create(user=user, value=token)
        return

    def update_token_in_db(self, user_id, old_token, new_token):
        token_in_db = self.repository.filter(user__id=user_id, value=old_token).first()
        if token_in_db is None:
            raise AuthenticationFailed("Токен не найден!")

        token_in_db.value = new_token
        token_in_db.save(update_fields=["value"])

        return

    def delete_token_from_db(self, user, token):
        self.repository.filter(user=user, value=token).delete()
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
