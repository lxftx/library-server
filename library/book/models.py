from django.db import models
from django.urls import reverse_lazy
from django.utils import timezone


class Languages(models.Model):
    """Таблица языков"""
    name = models.CharField(max_length=64, verbose_name="Язык", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"
        ordering = ['name']


class Publishing(models.Model):
    """Таблица издательств"""
    name = models.CharField(max_length=256, verbose_name="Издательство", unique=True)
    info = models.TextField(verbose_name="Информация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"
        ordering = ['name']


class Direction(models.Model):
    """Таблица направлении книг"""
    name = models.CharField(max_length=256, verbose_name="Направление", unique=True)
    info = models.TextField(verbose_name="Информация")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направлении"
        ordering = ['name']


class Translators(models.Model):
    """Таблица переводчиков"""
    first_name = models.CharField(max_length=128, verbose_name="Имя")
    last_name = models.CharField(max_length=256, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=256, verbose_name="Отчество", null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"

    class Meta:
        verbose_name = "Переводчик"
        verbose_name_plural = "Переводчики"
        ordering = ['last_name']


class Countries(models.Model):
    """Таблица стран"""
    name = models.CharField(max_length=128, verbose_name="Страна", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"
        ordering = ['name']


class Cities(models.Model):
    """Таблица городов"""
    name = models.CharField(max_length=128, verbose_name="Город", unique=True)
    country = models.ForeignKey(to=Countries, verbose_name="Страна", on_delete=models.SET_NULL, null=True, blank=True, related_name="cities")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ['name']


class Authors(models.Model):
    """Таблица авторов"""
    first_name = models.CharField(max_length=128, verbose_name="Имя")
    last_name = models.CharField(max_length=256, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=256, verbose_name="Отчество", null=True, blank=True)
    date = models.DateField(verbose_name="Дата рождения", null=True, blank=True)
    born = models.ForeignKey(to=Cities, on_delete=models.SET_NULL, verbose_name="Место рождения", null=True, blank=True)
    image = models.ImageField(upload_to='authors_image/', verbose_name="Изображение автора", null=True, blank=True)
    info = models.TextField(verbose_name="Автобиография")

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.patronymic}"

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"
        ordering = ['last_name']


class Genres(models.Model):
    """Таблица жанров"""
    name = models.CharField(max_length=128, verbose_name="Жанр")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']


class Bindings(models.Model):
    name = models.CharField(verbose_name="Переплет", max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Переплет"
        verbose_name_plural = "Переплеты"
        ordering = ['name']


class Books(models.Model):
    name = models.CharField(max_length=256, verbose_name="Книга")
    info = models.TextField(verbose_name="О книге", null=True, blank=True)
    ISBN = models.CharField(max_length=13, verbose_name="ISBN")
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество книг на складе")
    genre = models.ForeignKey(to=Genres, on_delete=models.SET_NULL, verbose_name="Жанр", null=True, blank=True, related_name="books_genre")
    author = models.ManyToManyField(to=Authors, verbose_name="Автор(-ы)", related_name="books_authors")
    interpreter = models.ManyToManyField(to=Translators, verbose_name="Переводчик(-и)", related_name="interpreter",
                                         blank=True)
    direction = models.ManyToManyField(to=Direction, verbose_name="Направление", related_name="direction", blank=True)
    publishing = models.ManyToManyField(to=Publishing, verbose_name="Издательство", related_name="publishing",
                                        blank=True)
    language = models.ForeignKey(to=Languages, on_delete=models.SET_NULL, verbose_name="Язык", null=True, blank=True)
    year_date = models.PositiveSmallIntegerField(verbose_name="Год издания")
    binding = models.ForeignKey(to=Bindings, verbose_name="Переплет", on_delete=models.SET_NULL, null=True, blank=True)
    page = models.PositiveSmallIntegerField(verbose_name="Страниц(-ы)", null=True, blank=True)
    image = models.ImageField(upload_to="books_image/", verbose_name="Изображение", null=True, blank=True)
    weight = models.PositiveSmallIntegerField(verbose_name="Вес", null=True, blank=True)

    def __str__(self):
        return f"Книга - {self.name}"

    class Meta:
        verbose_name = "Книга(-у)"
        verbose_name_plural = "Книги"
        ordering = ['name']
