from auth_app.models import RepositoryFactory, User


class UserService:
    def __init__(self) -> None:
        self.repository = RepositoryFactory.get_repository("UserRepository")

    def create(self, email: str, password: str):
        new_user = self.repository.create(email=email)
        new_user.set_password(password)
        new_user.save()

        return new_user

    def authenticate(self, email: str, password: str):
        user = self.repository.filter(email=email).first()
        if user is not None:
            is_password = user.check_password(password)
            if is_password:
                return user

        return None
