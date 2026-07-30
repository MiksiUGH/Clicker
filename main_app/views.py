"""Модуль с логикой для эндпоинтов"""
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Отображение главной страницы

    :param request: http-запрос
    :type request: HttpRequest
    :return: http-ответ
    :rtype: HttpResponse
    """
    ...


def register(request: HttpRequest) -> HttpResponse:
    """Регистрация

    :param request: http-запрос
    :type request: HttpRequest
    :return: http-ответ
    :rtype: HttpResponse
    """
    ...


def login(request: HttpRequest) -> HttpResponse:
    """Вход

    :param request: http-запрос
    :type request: HttpRequest
    :return: http-ответ
    :rtype: HttpResponse
    """
    ...


def logout(request: HttpRequest) -> HttpResponse:
    """Выход

    :param request: http-запрос
    :type request: HttpRequest
    :return: http-ответ
    :rtype: HttpResponse
    """
    ...


def add_click(request: HttpRequest) -> HttpResponse:
    """Добавление клика

    :param request: http-запрос
    :type request: HttpRequest
    :return: http-ответ
    :rtype: HttpResponse
    """
    ...


def buy_clicker_color(request: HttpRequest) -> HttpResponse:
    """Покупка цвета для кликера

    :param request: http-запрос
    :type request: HttpRequest
    :return: http-ответ
    :rtype: HttpResponse
    """
    ...
