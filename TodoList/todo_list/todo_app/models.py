from django.conf import settings
from django.db import models


class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    title = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name="Название",
    )
    description = models.TextField(verbose_name="Описание")
    start_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания задачи",
    )
    finish_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Планируемая дата завершения задачи",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self) -> str:
        return f"Задача {self.title} пользователя {self.user}"
