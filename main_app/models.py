"""Модели БД"""

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для модели User (без поля username)"""

    def create_user(self, name, password=None, **extra_fields):
        if not name:
            raise ValueError('Поле "Имя пользователя" обязательно для заполнения')

        user = self.model(name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(name, password, **extra_fields)


class User(AbstractUser):
    """Пользователь"""

    username = None

    name = models.CharField(
        "Имя пользователя", max_length=50, unique=True, db_index=True
    )

    USERNAME_FIELD = "name"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    clicks = models.IntegerField("Кол-во кликов", default=0)

    def __str__(self):
        return self.name


class Color(models.Model):
    """Цвет кликера"""

    name = models.CharField("Название цвета", max_length=50, unique=True, db_index=True)
    price = models.IntegerField("Цена цвета", default=100)
    users = models.ManyToManyField(
        User,
        related_name="colors",
        verbose_name="Пользователи",
    )
