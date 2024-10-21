from book.forms import create_form_for_model
from book.models import (Authors, Bindings, Books, Cities, Countries,
                         Direction, Genres, Languages, Publishing, Translators)
from django import forms
from django.db.models import Model
from django.db.models.base import ModelBase
from django.http import Http404, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from . import models
from .common.views import TitleMixin


def get_name_models():
    all_models = []
    for e in dir(models):
        if isinstance(getattr(models, e), ModelBase) and issubclass(getattr(models, e), Model):
            all_models.append(getattr(models, e))
    all_models = [(model._meta.object_name.lower(), model._meta.verbose_name_plural.title(), model) for model in
                  all_models]
    all_models.sort(key=lambda x: x[0].lower())
    return all_models


def get_info_form_model(request, form_model, pk=None):
    """Функция динамеческого создания ссылки для всех моделей"""
    match form_model:
        case 'languages':
            view = LanguageView.as_view()
            return view(request, pk)
        case 'publishing':
            view = PublishingView.as_view()
            return view(request, pk)
        case 'direction':
            view = DirectionView.as_view()
            return view(request, pk)
        case 'translators':
            view = TranslatorsView.as_view()
            return view(request, pk)
        case 'countries':
            view = CitiesView.as_view()
            return view(request, pk)
        case 'cities':
            view = CitiesView.as_view()
            return view(request, pk)
        case 'authors':
            view = AuthorsView.as_view()
            return view(request, pk)
        case 'genres':
            view = GenresView.as_view()
            return view(request, pk)
        case 'bindings':
            view = BindingsView.as_view()
            return view(request, pk)
        case 'books':
            view = BooksView.as_view()
            return view(request, pk)
        case _:
            raise Http404()
    # return HttpResponse(f'Это форма модели {form_model}')


# def delete_form_model(request, form_model, pk=None):
#     content = ''
#     if request.method == 'POST':
#         all_models = get_name_models()
#         for model in all_models:
#             if model[0] == form_model and model[2].objects.filter(pk=pk):
#                 model[2].objects.filter(pk=pk).delete()
#                 content = {f"Запись №{pk} для модели {model[1]}, была успешно удалена!"}
#                 return HttpResponse(content, status=200, content_type='application/json', charset='utf-8')
#             content = {f"Запись №{pk} для модели {model[1]}, не была найдена!"}
#         return HttpResponse(content, status=404, content_type='application/json', charset='utf-8', reason="Incorrect pk")
#     content = {"Данное действие только через POST"}
#     return HttpResponse(content, status=404, content_type='application/json', charset='utf-8')


class IndexView(TemplateView):
    template_name = 'book/index.html'


class FormListView(TemplateView):
    template_name = 'book/form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FormListView, self).get_context_data(**kwargs)
        all_models = get_name_models()
        context['forms'] = all_models
        return context


class LanguageView(TitleMixin, CreateView, ListView):
    """Представление модели Языки"""
    model = Languages
    template_name = 'book/form_detail.html'
    title = 'Языки'
    model_form_url = 'languages'

    custom_fields = {
        'name': (forms.CharField, {
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Каков язык?'}
        }),
    }

    form_class = create_form_for_model(model_class=Languages, custom_fields=custom_fields)


class PublishingView(TitleMixin, CreateView, ListView):
    """Представление модели Издательства"""
    model = Publishing
    template_name = 'book/form_detail.html'
    title = 'Издательства'
    model_form_url = 'publishing'

    custom_fields = {
        'name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Издательство?'}
        }),
        'info': (forms.CharField, {
            'widget': forms.Textarea,
            'widget_attrs': {'class': 'form__textarea', 'placeholder': 'Информация об издательстве', 'cols': 4,
                             'rows': 4}
        })
    }

    form_class = create_form_for_model(Publishing, custom_fields=custom_fields)


class DirectionView(TitleMixin, CreateView, ListView):
    """Представление модели Направлении"""
    model = Direction
    template_name = 'book/form_detail.html'
    title = 'Направлении'
    model_form_url = 'direction'

    custom_fields = {
        'name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Направление?'}
        }),
        'info': (forms.CharField, {
            'widget': forms.Textarea,
            'widget_attrs': {'class': 'form__textarea', 'placeholder': 'Информация о направлении', 'cols': 4, 'rows': 4}
        })
    }

    form_class = create_form_for_model(Direction, custom_fields=custom_fields)


class TranslatorsView(TitleMixin, CreateView, ListView):
    """Представление модели Переводчиков"""
    model = Translators
    template_name = 'book/form_detail.html'
    title = 'Переводчики'
    model_form_url = 'translators'

    custom_fields = {
        'first_name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Имя?'}
        }),
        'last_name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Фамилия?'}
        }),
        'patronymic': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Отчество?'}
        })
    }

    form_class = create_form_for_model(Translators, custom_fields=custom_fields)


class CountriesView(TitleMixin, CreateView, ListView):
    """Представление модели Страны"""
    model = Countries
    template_name = 'book/form_detail.html'
    title = 'Страны'
    model_form_url = 'countries'

    custom_fields = {
        'name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Страна?'}
        })
    }

    form_class = create_form_for_model(Countries, custom_fields=custom_fields)


class CitiesView(TitleMixin, CreateView, ListView):
    """Представление модели Города"""
    model = Cities
    template_name = 'book/form_detail.html'
    title = 'Города'
    model_form_url = 'cities'

    custom_fields = {
        'name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Город?'}
        }),
        'country': (forms.ModelChoiceField, {
            # 'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Страна?'}
        })
    }

    form_class = create_form_for_model(Cities, custom_fields=custom_fields)


class AuthorsView(TitleMixin, CreateView, ListView):
    """Представление модели Авторы"""
    model = Authors
    template_name = 'book/form_detail.html'
    title = 'Авторы'
    model_form_url = 'authors'

    custom_fields = {
        'first_name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Имя?'}
        }),
        'last_name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Фамилия?'}
        }),
        'patronymic': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Отчество?'}
        }),
        'date': (forms.DateField, {
            'widget': forms.DateInput,
            'widget_attrs': {'type': 'date', 'class': 'form__input', 'placeholder': 'день.месяц.год'}
        }),
        'born': (forms.ModelChoiceField, {
            'widget_attrs': {'class': 'form__input'}
        }),
        'image': (forms.ImageField, {
            'widget': forms.FileInput,
            'widget_attrs': {'class': 'form__input'}
        }),
        'info': (forms.CharField, {
            'widget': forms.Textarea,
            'widget_attrs': {'class': 'form__textarea', 'placeholder': 'Информация о направлении', 'cols': 4, 'rows': 4}
        })
    }

    form_class = create_form_for_model(Authors, custom_fields=custom_fields)


class GenresView(TitleMixin, CreateView, ListView):
    """Представление модели Жанры"""
    model = Genres
    template_name = 'book/form_detail.html'
    title = 'Жанры'
    model_form_url = 'genres'

    custom_fields = {
        'name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Жанр?'}
        })
    }

    form_class = create_form_for_model(Genres, custom_fields=custom_fields)


class BindingsView(TitleMixin, CreateView, ListView):
    """Представление модели Переплет"""
    model = Bindings
    template_name = 'book/form_detail.html'
    title = 'Переплет'
    model_form_url = 'bindings'

    custom_fields = {
        'name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Жанр?'}
        })
    }

    form_class = create_form_for_model(Bindings, custom_fields=custom_fields)


class BooksView(TitleMixin, CreateView, ListView):
    """Представление модели Книги"""
    model = Books
    template_name = 'book/form_detail.html'
    title = 'Книги'
    model_form_url = 'books'

    custom_fields = {
        'name': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Книга?'}
        }),
        'info': (forms.CharField, {
            'widget': forms.Textarea,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Информация о книге?'}
        }),
        'ISBN': (forms.CharField, {
            'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'ISBN?', 'maxlength': '13'}
        }),
        'quantity': (forms.IntegerField, {
            'widget': forms.NumberInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Кол-во книг на складе?'}
        }),
        'genre': (forms.ModelChoiceField, {
            # 'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Жанр?'}
        }),
        'author': (forms.ModelChoiceField, {
            # 'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Автор?'}
        }),
        'interpreter': (forms.ModelChoiceField, {
            # 'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Переводчики?'}
        }),
        'direction': (forms.ModelChoiceField, {
            # 'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Направление?'}
        }),
        'publishing': (forms.ModelChoiceField, {
            # 'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Издательство?'}
        }),
        'language': (forms.ModelChoiceField, {
            # 'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Язык?'}
        }),
        'year_date': (forms.IntegerField, {
            'widget': forms.NumberInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Год издания?'}
        }),
        'binding': (forms.ModelChoiceField, {
            # 'widget': forms.TextInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Переплет?'}
        }),
        'page': (forms.IntegerField, {
            'widget': forms.NumberInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Страниц(-ы)?'}
        }),
        'image': (forms.ImageField, {
            'widget': forms.FileInput,
            'widget_attrs': {'class': 'form__input'}
        }),
        'weight': (forms.IntegerField, {
            'widget': forms.NumberInput,
            'widget_attrs': {'class': 'form__input', 'placeholder': 'Вес?'}
        })
    }

    form_class = create_form_for_model(Books, custom_fields=custom_fields)
