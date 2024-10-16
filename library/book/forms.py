from django import forms


def create_form_for_model(model_class, include_fields=None, exclude_fields=None, custom_fields=None):
    """
    Создает форму на основе переданной модели с возможностью добавления кастомных полей.

    :param model_class: Модель, для которой создается форма.
    :param include_fields: Список полей модели, которые будут включены в форму.
    :param exclude_fields: Список полей модели, которые будут исключены из формы.
    :param custom_fields: Словарь с дополнительными полями для формы (формат: {'field_name': (FieldClass, kwargs)}).
    :return: Класс формы.
    """

    class DynamicModelForm(forms.ModelForm):

        class Meta:
            model = model_class
            fields = include_fields or '__all__'
            exclude = exclude_fields or []

        def __init__(self, *args, **kwargs):
            super(DynamicModelForm, self).__init__(*args, **kwargs)
            # Обновляем виджеты всех полей, чтобы добавить или сохранить атрибуты
            for field_name, field in self.fields.items():
                if custom_fields and field_name in custom_fields:
                    field_class, field_kwargs = custom_fields[field_name]
                    widget_attrs = field_kwargs.get('widget_attrs', {})
                    widget_class = field_kwargs.get('widget')

                    # Если указан класс виджета, используем его
                    if widget_class:
                        field.widget = widget_class(attrs=widget_attrs)
                    else:
                        # Иначе просто обновляем атрибуты текущего виджета
                        field.widget.attrs.update(widget_attrs)
    return DynamicModelForm
