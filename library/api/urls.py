from api.views import (AuthorsViewSet, BindingsViewSet, BooksViewSet,
                       CitiesViewSet, CountriesViewSet, DirectionViewSet,
                       GenreViewSet, LanguagesViewSet, PublishingViewSet,
                       TranslatorViewSet)
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register(r'authors', AuthorsViewSet, basename='authors')
router.register(r'languages', LanguagesViewSet, basename='languages')
router.register(r'publishing', PublishingViewSet, basename='publishing')
router.register(r'direction', DirectionViewSet, basename='direction')
router.register(r'translators', TranslatorViewSet, basename='translators')
router.register(r'countries', CountriesViewSet, basename='countries')
router.register(r'cities', CitiesViewSet, basename='cities')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'bindings', BindingsViewSet, basename='bindings')
router.register(r'books', BooksViewSet, basename='books')


urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token), # Эндпоинт для получения токена (для rest_framework.authtoken)
]
