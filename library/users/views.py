import datetime

from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib.auth.models import User

from users.forms import UserForm
from users.models import UserLogLogin

from users.services import *


class UserLoginView(LoginView):
    form_class = UserForm
    template_name = "users/index.html"

    def form_valid(self, form):
        user = form.get_user()
        user_log_queryset = UserLogLogin.objects.select_related('user').filter(user=user)
        if user_log_queryset.exists():
            if not check_block_to_login(self.request, user_log_queryset.get(user=user)):
                return redirect(reverse_lazy('users:login'))
        return super().form_valid(form)

    def form_invalid(self, form):
        username = form.cleaned_data['username']
        user_queryset = User.objects.filter(username=username)
        if user_queryset.exists():
            dt_now = timezone.now() + datetime.timedelta(hours=5)
            dt_now_str = dt_now.strftime('%d/%m/%Y %H:%M:%S')
            user_log_queryset = (UserLogLogin.objects.select_related('user')
                                 .filter(user=user_queryset.get(username=username)))
            if user_log_queryset.exists():
                user_log = user_log_queryset.get(user=user_queryset.get(username=username))
                add_block_to_login(self.request, user_log)
                user_log.ip_address[dt_now_str] = get_client_ip(self.request)
                user_log.save()
            else:
                UserLogLogin.objects.create(user=user_queryset.get(username=username),
                                            ip_address={dt_now_str: get_client_ip(self.request)})

        return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('schema-swagger-ui')


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('users:login'))
