import json

import requests
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_block_to_login(request, user):
    """Функция ставит блокировку на вход или увеличивает попытку входа"""
    if user.datetime_from_block_login:
        return
    elif user.count_false_logins >= 4:
        user.datetime_from_block_login = timezone.now()
        user.datetime_to_block_login = timezone.now() + timezone.timedelta(hours=5)
    else:
        user.count_false_logins += 1
        messages.warning(request, f'Неверный логин или пароль. У вас осталось {5 - user.count_false_logins} попыток до '
                                  f'блокировки.')


def check_block_to_login(request, user):
    """Функция проверяет на блокировку входа в аккаунт или удаляет запись, если блокировка прошла"""
    if not user.datetime_to_block_login or timezone.now() >= user.datetime_to_block_login:
        user.delete()
        return True
    else:
        messages.error(request, 'Ваш аккаунт временно заблокирован из-за слишком большого количества неудачных '
                                'попыток входа. Попробуйте позже.')
        return False


def get_new_jwt_token(user):
    """Функция создает новый токен ACCESS и REFRESH, передавая пользователя"""
    refresh = RefreshToken.for_user(user)

    # Возвращаем токены в виде JSON
    return {
        'refresh': str(refresh),  # Преобразуем refresh токен в строку
        'access': str(refresh.access_token)  # Преобразуем access токен в строку
    }


def update_or_create_new_token(cookies):
    answer = requests.post(settings.DOMAIN_NAME + settings.REFRESH_TOKEN_URL,
                           headers={'Content-Type': 'application/json'},
                           data=json.dumps({'refresh': cookies.get('ref')}))
    if answer.status_code == 200:
        return {"update": True, "tokens": answer.json()}
    else:
        tokens = requests.post(settings.DOMAIN_NAME + settings.ACCESS_TOKEN_URL,
                               headers={'Content-Type': 'application/json'},
                               data=json.dumps({'username': cookies.get('username'),
                                                'password': cookies.get('password')}))
        return {"update": False, "tokens": tokens}
