import json

from django.utils import timezone
from django.views.decorators.csrf import csrf_protect
from rest_framework import permissions, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.filters import AuthorFilter, BookFilter
from api.serializers import (AuthorsListSerializer, AuthorsSerializer,
                             BindingsSerializer, BooksCreateSerializer,
                             BooksRetrieveSerializer, BooksSerializer,
                             CitiesSerializer, CountrySerializer,
                             DirectionSerializer, GenresSerializer,
                             LanguagesSerializer, PublishingSerializer,
                             TranslatorsSerializer)
from book.models import (Authors, Bindings, Books, Cities, Countries,
                         Direction, Genres, Languages, Publishing, Translators)


class BaseClassViewSet(viewsets.ModelViewSet):
    """Базовый класс для классов наследующихся от viewsets.ModelViewSet"""

    # permission_classes - разрешение на выполнение определенным пользователям
    # permission_classes = [permissions.IsAuthenticated]
    # TokenAuthentication - выполнение каких либо методов через авторизацию по токену
    # SessionAuthentication - выполнение каких либо методов через Django сессии с использованием django.contrib.auth
    # authentication_classes - выполнение методов только через идентификацию по токену
    # authentication_classes = (JWTAuthentication, )

    # При каждом запросе ModelViewSet вызывает метод get_permissions
    def get_permissions(self):
        """Переопределяем метод get_permissions, где назначаем свои собственные разрешения на определенные запросы"""
        if self.action == 'list':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        #     elif self.action == 'retrieve':
        #         permission_classes = [permissions.IsAuthenticated]
        #     elif self.action in ['update', 'partial_update', 'create', 'delete']:
        #         permission_classes = [permissions.IsAdminUser]
        #     else:
        #         permission_classes = [permissions.AllowAny]
        #
        #     # Возвращаем соответствующий список классов разрешений
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        """Переопределили метод perform_create, который срабатывает при создании объекта и выводит информацию о
        создаваемом объекте"""
        super().perform_create(serializer)
        print(f"LOG : "
              f"{timezone.now()} :"
              f" [CREATE] Model({serializer.Meta.model._meta.verbose_name_plural.title()}) -> {serializer.instance}")

    def perform_update(self, serializer):
        """Переопределили метод perform_update, который срабатывает при обновлении объекта и выводит информацию о
        обновляемом объекте"""
        # Вызов стандартного обновления
        super().perform_update(serializer)
        # Добавление своей логики после обновления
        print(f"LOG :"
              f" {timezone.now()} :"
              f" [UPDATE] Model({serializer.Meta.model._meta.verbose_name_plural.title()}) -> {serializer.instance}")

    def perform_destroy(self, instance):
        """Переопределили метод perform_destroy, который срабатывает при удалении объекта и выводит информацию о
        обновляемом объекте"""
        # Вызов стандартного обновления
        super().perform_destroy(instance)
        # Добавление своей логики после обновления
        print(f"LOG :"
              f" {timezone.now()} :"
              f" [DELETE] Model({instance._meta.verbose_name_plural.title()}) -> {instance}")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK, data=json.dumps({"status": "Удалено"}, ensure_ascii=False))


class LanguagesViewSet(BaseClassViewSet):
    """
    API endpoint для управления языками
    """
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer


class PublishingViewSet(BaseClassViewSet):
    """
    API endpoint для управления издательствами
    """
    queryset = Publishing.objects.all()
    serializer_class = PublishingSerializer


class DirectionViewSet(BaseClassViewSet):
    """
    API endpoint для управления направлениями
    """
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer


class TranslatorViewSet(BaseClassViewSet):
    """
    API endpoint для управления переводчиками
    """
    queryset = Translators.objects.all()
    serializer_class = TranslatorsSerializer


class CountriesViewSet(BaseClassViewSet):
    """
    API endpoint для управления странами
    """
    queryset = Countries.objects.all()
    serializer_class = CountrySerializer


class CitiesViewSet(BaseClassViewSet):
    """
    API endpoint для управления городами
    """
    queryset = Cities.objects.all().select_related('country')
    serializer_class = CitiesSerializer


class AuthorsViewSet(BaseClassViewSet):
    """
    API endpoint для управления авторами
    """
    queryset = Authors.objects.all()
    # search_fields - используется у SearchFilter
    # search_fields = ['first_name', 'last_name']
    # filter_backends - передаем модуль фильтрации, если в настройках не указали глобально
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields - используется для простой фильтрации на основе равенства (используется у DjangoFilterBackend)
    # filterset_fields = ['first_name', 'last_name']
    filterset_class = AuthorFilter

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorsListSerializer
        else:
            return AuthorsSerializer


class GenreViewSet(BaseClassViewSet):
    """
    API endpoint для управления жанрами
    """
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer


class BindingsViewSet(BaseClassViewSet):
    """
    API endpoint для управления переплетами
    """
    queryset = Bindings.objects.all()
    serializer_class = BindingsSerializer


class BooksViewSet(BaseClassViewSet):
    """
    API endpoint для управления книгами
    """
    # select_related - Используется для оптимизации запросов, когда у вас есть ForeignKey или OneToOneField,
    # и вы хотите загружать связанные объекты в одном SQL-запросе с использованием JOIN. Делает SQL JOIN с таблицами
    # связанных объектов, чтобы получить все данные за один запрос, что ускоряет доступ к связанным данным.
    # prefetch_related - Используется для оптимизации запросов, когда у вас есть ManyToManyField или ForeignKey и вам
    # нужно загружать связанные объекты, но JOIN неэффективен или невозможен. Выполняет отдельный SQL-запрос для
    # каждой связанной модели и затем связывает результаты в Python, что более эффективно при работе с отношениями
    # ManyToMany и большими наборами данных.
    queryset = Books.objects.select_related(
        "genre", "language", "binding"
    ).prefetch_related(
        "author", "interpreter", "direction", "publishing"
    )
    # filter_backends — это атрибут, который определяет, какие фильтры будут применяться к запросу. Здесь мы добавили
    # filters.SearchFilter, чтобы использовать возможности поиска. Чтобы SearchFilter применялся ко всем viewsets
    # проекта, в settings.py была добавлена кофигурация.
    # filter_backends = [filters.SearchFilter]
    # search_fields — это список полей, по которым будет выполняться поиск. В данном случае можно искать по названию
    # книги (name) и имени автора (author__first_name). В search_fields можно использовать различные выражения для
    # поиска:
    # ^field_name: поиск начинается с заданного значения.
    # =field_name: точное совпадение.
    # @field_name: полнотекстовый поиск (поддерживается только в некоторых базах данных, таких как PostgreSQL).
    # field_name: простой поиск, который ищет совпадения по содержимому.
    # search_fields = ['^name', '=author__first_name']
    filterset_class = BookFilter

    def get_serializer_class(self):
        if self.action == "list":
            return BooksSerializer
        elif self.action == 'retrieve':
            return BooksRetrieveSerializer
        else:
            return BooksCreateSerializer

    # Переопределили метод create, в котором мы сами выполняем действия проверки и сохранения. После успешного
    #         сохранения, выводится полная информация о сохраненной записи
    def create(self, request, *args, **kwargs):
        """API endpoint добавление новой книги"""
        # Используем `BooksCreateSerializer` для валидации и сохранения данных
        serializer = BooksCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            created_book = serializer.save()
            # Сериализуем сохраненный объект с помощью `BooksRetrieveSerializer`
            retrieve_serializer = BooksRetrieveSerializer(created_book)
            # Возвращаем сериализованные данные созданного объекта с кодом 201 (Created)
            return Response(retrieve_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Переопределили метод update для вывода понятных данных при put методе
    def update(self, request, *args, **kwargs):
        """API endpoint обновления данных книги"""
        # Выполняем стандартное обновление partial=True - говорит что обновление будет частичным. False - ожидается,
        # что все поля должны быть переданы, иначе будет ошибка
        partial = kwargs.pop('partial', False)

        # get_object() — это метод, предоставляемый ModelViewSet который автоматически находит объект по его id или
        # другому идентификатору, переданному в URL. Например, если URL запроса выглядит как PUT /books/5/,
        # то get_object() вернет объект Books с id=5.
        instance = self.get_object()

        # Этот метод создает экземпляр сериализатора, который будет использоваться для обновления объекта instance с
        # новыми данными, полученными из request.data
        serializer = self.get_serializer(instance, data=request.data, partial=partial)

        # Проверяет, являются ли данные, переданные в сериализатор, валидными. raise_exception=True: Если данные не
        # валидны, метод автоматически выбрасывает исключение ValidationError, которое возвращает ответ с кодом
        # ошибки (например, 400 Bad Request) и подробностями ошибки валидации.
        serializer.is_valid(raise_exception=True)

        # Этот метод выполняет сохранение обновленных данных в базе данных. Метод perform_update вызывает
        # serializer.save(), который обновляет экземпляр модели в базе данных с учетом данных, прошедших валидацию. В
        # perform_update можно также переопределить логику, если нужно выполнить дополнительные действия перед или
        # после обновления объекта (например, отправить уведомление или логировать изменения).
        self.perform_update(serializer)

        # Используем BooksRetrieveSerializer для сериализации обновленного объекта
        retrieve_serializer = BooksRetrieveSerializer(instance)

        return Response(retrieve_serializer.data)

    def get_object(self):
        """Переопределили метод get_object, который проверяет существует ли такая запись и разрешен ли запрос с
        этим объектом"""
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        # Проверяет, должен ли запрос быть разрешен для данного объекта.
        # Создает соответствующее исключение, если запрос не разрешен.
        self.check_object_permissions(self.request, obj)
        return obj
