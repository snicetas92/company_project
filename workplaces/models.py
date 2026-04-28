from django.db import models
from django.conf import settings


class Workplace(models.Model):
    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Сотрудник',
        related_name='assigned_workplace'
    )

    desk_number = models.CharField('Номер стола', max_length=20, unique=True)
    additional_info = models.TextField('Дополнительная информация', blank=True)

    def __str__(self):
        return f"Рабочее место {self.desk_number}"