"""Модуль с логикой для эндпоинтов"""

import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login, logout

from main_app.models import Color, User
from main_app.forms import RegisterForm, LoginForm


def index(request: HttpRequest) -> HttpResponse:
    """Отображение главной страницы"""
    user_colors = []
    if request.user.is_authenticated:
        user_colors = list(request.user.colors.all())

    return render(
        request,
        "index.html",
        context={
            "user": request.user,
            "user_colors": user_colors,
        },
    )


def register_user(request: HttpRequest) -> HttpResponse:
    """Регистрация пользователя"""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if User.objects.filter(name=username).exists():
                form.add_error("username", "Пользователь с таким именем уже существует")
                return render(request, "register.html", context={"form": form})

            new_user = User.objects.create_user(name=username, password=password)

            login(request, new_user)
            return redirect("index")
        else:
            return render(request, "register.html", context={"form": form})

    return render(request, "register.html", context={"form": RegisterForm()})


def login_user(request: HttpRequest) -> HttpResponse:
    """Авторизация пользователя"""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                form.add_error("password", "Неверное имя пользователя или пароль")

        return render(request, "login.html", context={"form": form})

    return render(request, "login.html", context={"form": LoginForm()})


def logout_user(request: HttpRequest) -> HttpResponse:
    """Выход пользователя"""
    logout(request)
    return redirect("index")


def add_click(request: HttpRequest) -> HttpResponse:
    """Добавдение кликов"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    try:
        data = json.loads(request.body)
        user = request.user
        user.clicks = data.get("clicks", user.clicks)
        user.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def buy_clicker_color(request: HttpRequest) -> HttpResponse:
    """Покупка цветов для кликера"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Unauthorized"}, status=403)

    try:
        data = json.loads(request.body)
        color_name = data.get("color")

        user = request.user
        color = Color.objects.get(name=color_name)

        if user.colors.filter(id=color.id).exists():
            return JsonResponse({"success": False, "message": "Цвет уже куплен"})

        if user.clicks < color.price:
            return JsonResponse({"success": False, "message": "Недостаточно кликов"})

        user.clicks -= color.price
        user.colors.add(color)
        user.save()

        return JsonResponse(
            {"success": True, "new_clicks": user.clicks, "color": color_name}
        )

    except Color.DoesNotExist:
        return JsonResponse({"error": "Color not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
