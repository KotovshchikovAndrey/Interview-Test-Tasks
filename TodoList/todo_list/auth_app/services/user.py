import typing as tp
from abc import ABC, abstractmethod

from auth_app.models import User


class IUserService(ABC):
    @abstractmethod
    def create(self, email: str, password: str) -> User:
        raise NotImplementedError()

    @abstractmethod
    def authenticate(self, email: str, password: str) -> tp.Optional[User]:
        raise NotImplementedError()


class UserService(IUserService):
    def create(self, email: str, password: str):
        new_user = User.objects.create(email=email)
        new_user.set_password(password)
        new_user.save()

        return new_user

    def authenticate(self, email: str, password: str):
        user = User.objects.filter(email=email).first()
        if user is not None:
            is_password = user.check_password(password)
            if is_password:
                return user

        return None


def get_user_service() -> IUserService:
    return UserService()
