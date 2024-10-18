from django.db import models
from django.contrib.auth.models import User


class UserLogLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь", db_index=True, blank=True,
                             null=True)
    ip_address = models.JSONField(verbose_name="IP address", default=dict)
    count_false_logins = models.IntegerField(default=0, verbose_name="Количество неверных вхождений")
    datetime_from_block_login = models.DateTimeField(verbose_name="Дата блокировки начиная", blank=True, null=True)
    datetime_to_block_login = models.DateTimeField(verbose_name="Дата блокировки заканчивая", blank=True, null=True)

    class Meta:
        verbose_name = 'LOG LOGIN'
        verbose_name_plural = 'LOG LOGIN'
