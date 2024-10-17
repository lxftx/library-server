from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from api.views import (AuthorsViewSet, BindingsViewSet, BooksViewSet,
                       CitiesViewSet, CountriesViewSet, DirectionViewSet,
                       GenreViewSet, LanguagesViewSet, PublishingViewSet,
                       TranslatorViewSet)

app_name = 'api'


urlpatterns = [
    path('api-token-auth/', obtain_auth_token), # Эндпоинт для получения токена (для rest_framework.authtoken)
    path('languages/', LanguagesViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='languages'),
    path('languages/<int:pk>', LanguagesViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
         }), name='languages-actions'),
    path('publishing/', PublishingViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='publishing'),
    path('publishing/<int:pk>', PublishingViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
        }), name='publishing-actions'),
    path('direction/', DirectionViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='direction'),
    path('direction/<int:pk>', DirectionViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
        }), name='direction-actions'),
    path('translators/', TranslatorViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='translators'),
    path('translators/<int:pk>', TranslatorViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
        }), name='translators-actions'),
    path('countries/', CountriesViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='translators'),
    path('countries/<int:pk>', CountriesViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
        }), name='countries-actions'),
    path('cities/', CitiesViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='cities'),
    path('cities/<int:pk>', CitiesViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
        }), name='cities-actions'),
    path('authors/', AuthorsViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='authors'),
    path('authors/<int:pk>', AuthorsViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
        }), name='authors-actions'),
    path('genres/', GenreViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='genres'),
    path('genres/<int:pk>', GenreViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
        }), name='genres-actions'),
    path('bindings/', BindingsViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='bindings'),
    path('bindings/<int:pk>', BindingsViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
        }), name='bindings-actions'),
    path('books/', BooksViewSet.as_view(
        {
            "get": "list",
            "post": "create"
        }), name='books'),
    path('books/<int:pk>', BooksViewSet.as_view(
        {
            "get": "retrieve",
            "delete": "destroy",
            "put": "update"
        }), name='books-actions'),
]
