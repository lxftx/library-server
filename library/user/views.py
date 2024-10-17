from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout


def login_view(request):
    if not request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    return redirect(request.META.get('HTTP_REFERER'))


def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)
