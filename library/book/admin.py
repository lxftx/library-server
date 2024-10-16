from django.contrib import admin
from django.utils.safestring import mark_safe

from book.models import Books, Languages, Publishing, Direction, Translators, Countries, Authors, Genres, Cities, \
    Bindings


class AdminImage:
    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img style="width: 150px;" src="{obj.image.url}">'"")
        else:
            return 'Нет фото'

    get_image.short_description = "Фотография"


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin, AdminImage):
    list_display = ('name', 'ISBN', 'quantity', 'get_image')
    fieldsets = (
        ("Basic information - Основная информация", {
            # 'classes': ('collapse',),
            'fields': (("name", "ISBN", "quantity"),
                       'info')
        }),
        ("Creators and creators - Творцы и созидательницы", {
            # 'classes': ('collapse',),
            'fields': (("author", "interpreter", "publishing"),)
        }),
        ("Direction - Направление", {
            # 'classes': ('collapse',),
            'fields': (("genre", "direction", "language"),)
        }),
        ("Additional information - Добавочная информация", {
            # 'classes': ('collapse',),
            'fields': (("year_date", "page", "weight", "binding"), ("image", "get_image"))
        })
    )
    search_fields = ('name', 'genre__name', 'direction__name', 'publishing__name')
    list_filter = ('genre__name', 'direction__name', 'publishing__name', 'year_date')
    readonly_fields = ('get_image',)


@admin.register(Bindings)
class BindingsAdmin(admin.ModelAdmin, AdminImage):
    list_display = ('pk', 'name')


@admin.register(Languages)
class LanguagesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Publishing)
class PublishingAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Translators)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'patronymic')
    search_fields = ('first_name', 'last_name', 'patronymic')


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'country__name')


@admin.register(Authors)
class AuthorsAdmin(admin.ModelAdmin, AdminImage):
    list_display = ('pk', 'first_name', 'last_name', 'patronymic', 'get_image')
    search_fields = ('first_name', 'last_name', 'patronymic')
    list_filter = ("born__name", "date")
    fieldsets = (
        ("Basic information - Основная информация", {
            'fields': (("first_name", "last_name", "patronymic"),
                       ("born", "date"),)
        }),
        ("Photo - Фотография", {
            'fields': (("image", "get_image"),)
        })
    )
    readonly_fields = ('get_image',)


@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


admin.site.site_title = "Администрирование Библиотека"
admin.site.site_header = "Библиотека"
admin.site.index_title = "Административная панель"
