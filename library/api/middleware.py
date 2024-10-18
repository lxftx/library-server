from django.shortcuts import redirect
from django.urls import reverse_lazy


class LoginRequiredMiddleware:
    """Middleware для перенаправления неавторизированных пользователей на странице /swagger/"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Проверяем, если запрос идет к swagger и пользователь не авторизован
        if request.path.startswith('/swagger') and request.user and not request.user.is_authenticated:
            return redirect(reverse_lazy('users:login'))

        response = self.get_response(request)
        return response