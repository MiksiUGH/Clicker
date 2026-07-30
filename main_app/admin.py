"""Настройки администраторской панели"""

from django.contrib import admin

from main_app.models import User, Color


class UserToAdmin(admin.ModelAdmin):
    """Модель пользователя для админки"""

    list_display = ["name", "get_colors"]
    list_filter = ["name", "get_colors"]
    search_fields = ["name"]

    class Meta:
        """Настройки модели для админки"""

        model = User


class ColorToAdmin(admin.ModelAdmin):
    """Модель цвета для админки"""

    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]

    class Meta:
        """Настройки модели для админки"""

        model = Color


admin.site.register(User, UserToAdmin)
admin.site.register(Color, ColorToAdmin)
