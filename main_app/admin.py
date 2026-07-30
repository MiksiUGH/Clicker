"""Настройки администраторской панели"""

from django.contrib import admin

from main_app.models import User, Color


class UserToAdmin(admin.ModelAdmin):
    """Модель пользователя для админки"""
    model = User
    list_display = ["name", "clicks", "get_colors"]
    list_filter = ["name", "clicks"]
    search_fields = ["name"]

    def get_colors(self, obj):
        """Получение всех цветов"""
        colors = obj.colors.all()
        return ", ".join(color.name for color in colors)

    get_colors.short_description = "Цвета"


class ColorToAdmin(admin.ModelAdmin):
    """Модель цвета для админки"""

    model = Color
    list_display = ["name"]
    list_filter = ["name"]
    search_fields = ["name"]


admin.site.register(User, UserToAdmin)
admin.site.register(Color, ColorToAdmin)
