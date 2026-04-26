# workplaces/models.py
from django.db import models
from django.conf import settings


class Workplace(models.Model):
    # ВНИМАНИЕ: Имя поля должно быть desk_number (с нижним подчеркиванием)
    desk_number = models.CharField('Номер стола', max_length=20, unique=True)

    # ВНИМАНИЕ: Имя поля должно быть additional_info (с нижним подчеркиванием)
    additional_info = models.TextField('Дополнительная информация', blank=True)

    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Сотрудник',
        related_name='workplace'
    )