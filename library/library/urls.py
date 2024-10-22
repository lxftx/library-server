"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from library.yasg import urlpatterns as yasg

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('book.urls')),
    path('users/', include('users.urls')),
    path('api/v1/', include('api.urls')),
    # api/token/ - используется для получения токена доступа и рефреш-токена. Используя TokenObtainPairView,
    # можно отправить POST-запрос с username и password на api/token/, чтобы получить access и refresh токены.
    path(settings.ACCESS_TOKEN_URL, TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # api/token/refresh/ - используется для обновления токена доступа с помощью рефреш-токена.
    path(settings.REFRESH_TOKEN_URL, TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += yasg

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
