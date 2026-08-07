from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_colors(**kwargs):
    """Функция создает базовые цвета при первом запуске миграций"""
    from main_app.models import Color

    default_colors = [
        {"name": "Красный", "price": 50},
        {"name": "Синий", "price": 100},
        {"name": "Зелёный", "price": 150},
    ]
    for data in default_colors:
        Color.objects.get_or_create(
            name=data["name"], defaults={"price": data["price"]}
        )
    print("Базовые цвета успешно созданы или уже существуют!")


class MainAppConfig(AppConfig):
    """Главные настройки приложения"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "main_app"

    def ready(self):
        post_migrate.connect(create_default_colors, sender=self)
