import django_filters
from book.models import *
from django import forms
from django.db.models import Q


class AuthorFilter(django_filters.FilterSet):
    """Кастомный фильтр для модели Authors"""

    # lookup_expr = "field lookup":
    # 1) exact - точное совпадение
    # 2) iexact - точное совпадение без учета регистра
    # 3) contains - проверка вхождения  LIKE $hello$
    # 4) icontains - проверка вхождения без учета регистра
    # 5) in - совпадение по переданному списку
    # 6) gte, lte, gt, lt - >=, <=, >, <
    # 7) startswith - проверка начального вхождения  LIKE 'Lennon%'
    # 8) istartswith - проверка начального вхождения без учета регистра
    # 9) endswith, iendswith - проверка конечного вхождения  LIKE '%non'

    # Мы определяем кастомный метод filter_first_name, который будет вызываться для фильтра first_name.
    # first_name = django_filters.CharFilter(method="filter_first_name")
    # last_name = django_filters.CharFilter(lookup_expr='startswith')
    # date_year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    # date__gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    # date__lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    # date = django_filters.DateFromToRangeFilter(field_name='date', lookup_expr='range')

    # Создание фильтра выпадающего списка по поиску ForeignKey
    born_name = django_filters.ModelChoiceFilter(queryset=Cities.objects.all(),
                                                 to_field_name='id',
                                                 field_name='born__name')

    class Meta:
        model = Authors
        fields = {
            'date': ['gte', 'lte'],  # Задаем диапазоны дат
            'first_name': ['icontains'],  # Добавляем фильтрацию по имени
            'last_name': ['icontains'],  # Фильтрация по фамилии
        }

    @staticmethod
    def filter_first_name(queryset, name, value):
        if value:
            names = value.replace(' ', '').split(',') if value.find(',') != -1 else value.split(' ')
            return queryset.filter(Q(first_name__in=names))
        return queryset


class BookFilter(django_filters.FilterSet):
    """Кастомный фильтр для модели Books"""
    genre = django_filters.ModelChoiceFilter(queryset=Genres.objects.all(), field_name='genre', to_field_name='id')
    author = django_filters.ModelChoiceFilter(queryset=Authors.objects.all(), field_name='author', to_field_name='id')
    publishing = django_filters.ModelChoiceFilter(queryset=Publishing.objects.all(),
                                                  field_name='publishing', to_field_name='id')
    binding = django_filters.ModelChoiceFilter(queryset=Bindings.objects.all(), field_name='binding',
                                               to_field_name='id')

    class Meta:
        model = Books
        fields = {
            'name': ['icontains'],
            'ISBN': ['startswith'],
            'year_date': ['gte', 'lte', 'exact'],
        }
