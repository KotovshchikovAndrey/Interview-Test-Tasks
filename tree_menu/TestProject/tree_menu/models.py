from django.db import models


class Menu(models.Model):
    name = models.CharField(
        max_length=15,
        null=False,
        blank=False,
        verbose_name="Название",
        unique=True,
    )

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self) -> str:
        return self.name


class MenuItem(models.Model):
    name = models.CharField(
        max_length=20,
        null=False,
        blank=False,
        verbose_name="Элемент меню",
    )
    menu = models.ForeignKey(
        "Menu",
        on_delete=models.CASCADE,
        verbose_name="Меню",
        related_name="items",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Верхний(Родительский) элемент",
        related_name="children",
    )

    class Meta:
        verbose_name = "Элемент меню"
        verbose_name_plural = "Элементы меню"

    def __str__(self) -> str:
        return f"{self.name} для меню {self.menu}"
