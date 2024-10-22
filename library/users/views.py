from django.contrib.auth import logout
from django.contrib import auth
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.services import *


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = auth.authenticate(username=username, password=password)
    if user is not None:
        json_tokens = get_new_jwt_token(user)
        response = Response()
        # httponly=True - Когда кука устанавливается с флагом HttpOnly, это означает, что кука будет доступна только
        # через HTTP-заголовки, и JavaScript не сможет получить доступ к этой куке через document.cookie. Браузер
        # хранит куку и отправляет ее обратно на сервер с каждым запросом к этому домену, но JavaScript не может
        # получить доступ к ней.
        # samesite='Lax' - Cookies с флагом SameSite защищают от CSRF атак, ограничивая
        # отправку cookies только на тот же сайт.
        # secure=True Куки с флагом Secure передаются только по HTTPS
        response.set_cookie(key='ref', value=json_tokens.get("refresh"), httponly=True, samesite='Lax')
        response.data = {
            'acc': json_tokens.get("access"),
        }
        return response

    return Response({
        "error": "Invalid Credentials"
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_jwt_token(request):
    ref_token = request.COOKIES.get('ref')
    answer = update_or_create_new_token(ref_token, request.user)
    response = Response()
    if answer.get('update'):
        response.data = {
            'acc': answer.get('tokens').get('access')
        }
    else:
        acc, ref = (answer.get('tokens').values())
        response.set_cookie(key='ref', value=ref, httponly=True, samesite='Lax')
        response.data = {
            'acc': acc
        }
    return response


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('book:index'))
