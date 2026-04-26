from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField

class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('M', _('Мужской')),
        ('F', _('Женский')),
        ('O', _('Другой')),
    ]
    gender = models.CharField(_('Пол'), max_length=1, choices=GENDER_CHOICES, blank=True)
    middle_name = models.CharField(_('Отчество'), max_length=150, blank=True)
    description = RichTextField(_('Описание'), blank=True)

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

class Skill(models.Model):
    name = models.CharField(_('Название навыка'), max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Навык')
        verbose_name_plural = _('Навыки')

class EmployeeSkill(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_('Сотрудник'))
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name=_('Навык'))
    level = models.PositiveSmallIntegerField(_('Уровень освоения'), default=1)

    class Meta:
        unique_together = ('employee', 'skill')
        verbose_name = _('Навык сотрудника')
        verbose_name_plural = _('Навыки сотрудников')

    def __str__(self):
        return f"{self.employee.get_full_name()} — {self.skill} (уровень {self.level})"