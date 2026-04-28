# Файл: workplaces/admin.py
from django.contrib import admin
from django.contrib.auth import (
    get_user_model,
)  # Правильный способ получить модель пользователя

from .models import Workplace

# Получаем модель пользователя один раз
CustomUser = get_user_model()


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ("desk_number", "employee", "additional_info")

    # Если у вас есть методы, использующие пользователя, они будут работать
    # Например, если вы хотели отображать полное имя:
    # def get_employee_name(self, obj):
    #     return obj.employee.get_full_name()
