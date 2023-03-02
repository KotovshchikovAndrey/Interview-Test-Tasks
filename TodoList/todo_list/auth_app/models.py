from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email: str, password: str):
        if not email:
            raise ValueError("Email Обязательное Поле!")
        elif not password:
            raise ValueError("password Обязательное Поле!")

        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = False
        user.is_admin = False
        user.is_staff = False
        user.is_active = False
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.email


class Token(models.Model):
    value = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name="Токен",
    )
    user = models.ForeignKey(
        "User",
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Токен"
        verbose_name_plural = "Токены"

    def __str__(self) -> str:
        return f"Токен пользователя {self.user}"
