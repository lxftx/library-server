from django.contrib import messages
from django.utils import timezone


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
