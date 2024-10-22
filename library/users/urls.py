from django.urls import path
from users.views import login_view, logout_view, refresh_jwt_token

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('refresh/', refresh_jwt_token, name='refresh'),
    # path('is_login/', is_login, name='is_login'),
]