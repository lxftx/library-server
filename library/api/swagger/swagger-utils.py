from drf_yasg.inspectors import SwaggerAutoSchema


class CustomAutoSchema(SwaggerAutoSchema):
    """Кастномный класс, который назначет каждому методу свой класс. (по названию модели)"""
    def get_tags(self, operation_keys=None):
        tags = super().get_tags(operation_keys)
        if operation_keys:
            # Используем первый элемент operation_keys, чтобы задать тег, который может быть названием модели.
            operation_keys = [keys for keys in operation_keys if keys not in ['api', 'v1']]
            return [operation_keys[0].title()]
        return tags
