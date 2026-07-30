"""Модели БД"""

from django.db import models


class User(models.Model):
    """Пользователь"""

    name: models.CharField = models.CharField(
        "Имя пользователя", max_length=50, unique=True, db_index=True
    )
    password: models.CharField = models.CharField("Пароль пользователя", max_length=128)
    clicks: models.IntegerField = models.IntegerField("Кол-во кликов", default=0)


class Color(models.Model):
    """Цвет кликера"""

    name: models.CharField = models.CharField(
        "Имя пользователя", max_length=50, db_index=True
    )
    users: models.ManyToManyField = models.ManyToManyField(
        User,
        related_name="colors",
        verbose_name="Пользователи",
    )
