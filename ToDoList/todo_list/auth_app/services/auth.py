from rest_framework.exceptions import AuthenticationFailed


class AuthService:
    def __init__(self, user_service, token_service) -> None:
        self.user_service = user_service
        self.token_service = token_service

    def register(self, user):
        new_user = self.user_service.create(
            email=user["email"],
            password=user["password"],
        )

        return self.set_token_for_user(user=new_user)

    def login(self, user):
        user = self.user_service.authenticate(
            email=user["email"],
            password=user["password"],
        )

        if user is None:
            raise AuthenticationFailed("Неверный логин или пароль!")

        return self.set_token_for_user(user)

    def refresh_tokens(self, old_refresh_token):
        token_payload = self.token_service.decode_token(token=old_refresh_token)

        new_refresh_token = self.token_service.generate_refresh_token(token_payload)
        new_access_token = self.token_service.generate_access_token(token_payload)

        self.token_service.update_token_in_db(
            user_id=token_payload["id"],
            old_token=old_refresh_token,
            new_token=new_refresh_token,
        )

        return new_access_token, new_refresh_token

    def logout(self, user, token):
        self.token_service.delete_token_from_db(user, token)

    def set_token_for_user(self, user):
        token_payload = {
            "id": user.id,
            "email": user.email,
        }

        access_token = self.token_service.generate_access_token(token_payload)
        refresh_token = self.token_service.generate_refresh_token(token_payload)

        self.token_service.set_token(user=user, token=refresh_token)

        return access_token, refresh_token
