from auth_app.services.auth import AuthService
from auth_app.services.token import TokenService
from auth_app.services.user import UserService


class ServiceFactory:
    services = {
        "AuthService": AuthService(
            user_service=UserService(),
            token_service=TokenService(),
        ),
    }

    @classmethod
    def get_service(cls, name):
        return cls.services.get(name)
