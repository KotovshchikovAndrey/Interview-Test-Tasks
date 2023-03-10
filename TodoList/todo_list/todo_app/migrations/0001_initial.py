# Generated by Django 4.1.7 on 2023-03-01 22:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100, verbose_name="Название")),
                ("description", models.TextField(verbose_name="Описание")),
                (
                    "start_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания задачи"
                    ),
                ),
                (
                    "finish_date",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Планируемая дата завершения задачи",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Задача",
                "verbose_name_plural": "Задачи",
            },
        ),
    ]
