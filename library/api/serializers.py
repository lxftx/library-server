from book.models import (Authors, Bindings, Books, Cities, Countries,
                         Direction, Genres, Languages, Publishing, Translators)
from django.utils import timezone
from rest_framework import serializers


class LanguagesSerializer(serializers.ModelSerializer):
    """Показ всех языков"""

    class Meta:
        model = Languages
        fields = '__all__'


class PublishingSerializer(serializers.ModelSerializer):
    """Шаблон сериалиатора для работы с издательствами"""

    class Meta:
        model = Publishing
        fields = '__all__'


class DirectionSerializer(serializers.ModelSerializer):
    """Показ/Создание/обновление/удаление/вывод одной записи направлении книг"""

    class Meta:
        model = Direction
        fields = '__all__'


class TranslatorsSerializer(serializers.ModelSerializer):
    """Показ всех переводчиков"""

    class Meta:
        model = Translators
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    """Показ всех стран"""
    cities = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = Countries
        fields = ('id', 'name', 'cities')


class CitiesSerializer(serializers.ModelSerializer):
    """Показ/Обновление/удаление/вывод одной записи городов"""

    class Meta:
        model = Cities
        fields = "__all__"


class BooksAuthorsSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        model = Books
        # fields = '__all__'
        fields = ('name', 'ISBN', 'genre')


class AuthorsListSerializer(serializers.ModelSerializer):
    born = serializers.SerializerMethodField()

    class Meta:
        model = Authors
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'date', 'born')

    def get_born(self, obj):
        if obj.born:
            return f"{obj.born.name}, {obj.born.country}"
        else:
            return None


class AuthorsSerializer(serializers.ModelSerializer):
    """Показ всех авторов книг и добавление новой книги"""

    class Meta:
        model = Authors
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'date', 'born', 'image', 'info')


class GenresSerializer(serializers.ModelSerializer):
    """Показ|подробное описание/добавление/удаление/обновление данных жанров книг"""

    class Meta:
        model = Genres
        fields = ('id', 'name')


class BindingsSerializer(serializers.ModelSerializer):
    """Показ/подробное описание/добавление/удаление/обновление данных о переплете"""

    class Meta:
        model = Bindings
        fields = "__all__"


class BooksSerializer(serializers.ModelSerializer):
    """Сериализатор для получения списка книг"""
    genre = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = AuthorsListSerializer(many=True)

    class Meta:
        model = Books
        fields = ('id', 'name', 'genre', 'author', 'quantity')


class BooksRetrieveSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(read_only=True, slug_field='name')
    language = serializers.SlugRelatedField(read_only=True, slug_field='name')
    binding = serializers.SlugRelatedField(read_only=True, slug_field='name')
    author = AuthorsListSerializer(read_only=True, many=True)
    interpreter = TranslatorsSerializer(read_only=True, many=True)
    direction = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)
    publishing = serializers.SlugRelatedField(read_only=True, slug_field='name', many=True)

    class Meta:
        model = Books
        fields = '__all__'


class BooksCreateSerializer(serializers.ModelSerializer):
    """Сериализатор, для добавления книги"""

    class Meta:
        model = Books
        fields = '__all__'

    @staticmethod
    def validate_quantity(value):
        """Проверка, чтобы количество книг было положительным."""
        if value < 0:
            raise serializers.ValidationError("Количество книг не может быть отрицательным числом")
        return value

    @staticmethod
    def validate_year_date(value):
        """Проверка, чтобы передаваемая дата была не больше сегодняшней"""
        if value > timezone.now().year:
            raise serializers.ValidationError("Передаваемая дата не может быть больше сегодняшней")
        return value

    # Бесполезная функция
    # def validate(self, data):
    #     """Проверка на соответствии языка оригинала и языка перевода"""
    #     if 'interpreter' in data and data['language']:
    #         original_language = data['language']
    #         if "Русский" != original_language.name:
    #             raise serializers.ValidationError(
    #                 "Язык перевода не может совпадать с языком оригинала."
    #             )
    #     return data
