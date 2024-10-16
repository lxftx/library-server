from rest_framework import viewsets, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import (LanguagesSerializer, PublishingSerializer,
                             CitiesSerializer, TranslatorsSerializer,
                             CountrySerializer, AuthorsSerializer,
                             GenresSerializer, BooksSerializer,
                             BindingsSerializer, DirectionSerializer,
                             BooksCreateSerializer, BooksRetrieveSerializer)
from book.models import Languages, Publishing, Direction, Translators, Countries, Cities, Authors, Genres, Books, \
    Bindings


class LanguagesViewSet(viewsets.ModelViewSet):
    """
    Endpoint для просмотра и редактирования данных языков
    """
    queryset = Languages.objects.all()
    serializer_class = LanguagesSerializer
    permission_classes = [permissions.AllowAny]


class PublishingViewSet(viewsets.ModelViewSet):
    """
    Endpoint для просмотра и редактирования данных издательств
    """
    queryset = Publishing.objects.all()
    serializer_class = PublishingSerializer
    permission_classes = [permissions.AllowAny]


class DirectionViewSet(viewsets.ModelViewSet):
    """
    Endpoint для просмотра и редактирования данных направлений
    """
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [permissions.AllowAny]


class TranslatorViewSet(viewsets.ModelViewSet):
    """
    Endpoint для просмотра и редактирования данных переводчиков
    """
    queryset = Translators.objects.all()
    serializer_class = TranslatorsSerializer
    permission_classes = [permissions.AllowAny]


class CountriesViewSet(viewsets.ModelViewSet):
    """
    Endpoint для просмотра и редактирования данных стран
    """
    queryset = Countries.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [permissions.AllowAny]


class CitiesViewSet(viewsets.ModelViewSet):
    """
    Endpoint для просмотра и редактирования данных городов
    """
    queryset = Cities.objects.all().select_related('country')
    serializer_class = CitiesSerializer
    permission_classes = [permissions.AllowAny]


class AuthorsViewSet(viewsets.ModelViewSet):
    """
    Endpoint для просмотра и редактирования данных авторов книг
    """
    queryset = Authors.objects.all()
    serializer_class = AuthorsSerializer
    permission_classes = [permissions.AllowAny]


class GenreViewSet(viewsets.ModelViewSet):
    """
    Endpoint для просмотра и редактирования данных жанров книг
    """
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = [permissions.AllowAny]


class BindingsViewSet(viewsets.ModelViewSet):
    """
    Endpoint для просмотра и редактирования данных жанров книг
    """
    queryset = Bindings.objects.all()
    serializer_class = BindingsSerializer
    permission_classes = [permissions.AllowAny]


class BooksViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления книгами
    """
    queryset = Books.objects.select_related(
            "genre", "language", "binding"
        ).prefetch_related(
            "author", "interpreter", "direction", "publishing"
        )
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == "list":
            return BooksSerializer
        elif self.action == 'retrieve':
            return BooksRetrieveSerializer
        else:
            return BooksCreateSerializer

    def update(self, request, *args, **kwargs):
        """Переопределили метод update для вывода понятных данных при put методе"""
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
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        # Проверяет, должен ли запрос быть разрешен для данного объекта.
        # Создает соответствующее исключение, если запрос не разрешен.
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        """Переопределили метод perform_update, который срабатывает при обновлении объекта и выводит информацию о
        обновляемом объекте"""
        # Вызов стандартного обновления
        super().perform_update(serializer)
        # Добавление своей логики после обновления
        print(f"LOG : [UPDATE] obj -> {serializer.instance}")

    def perform_create(self, serializer):
        """Переопределили метод perform_create, который срабатывает при создании объекта и выводит информацию о
        создаваемом объекте"""
        super().perform_create(serializer)
        print(f"LOG : [CREATE] obj -> {serializer.instance}")