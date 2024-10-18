from django.urls import path

from users.views import UserLoginView, logout_view

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout')
]