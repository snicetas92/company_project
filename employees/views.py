# Файл: employees/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from django.core.paginator import Paginator
from datetime import date


# --- 1. Главная страница ---
def home(request):
    """
    Главная страница сайта.
    Задача: Вывести 4-х последних сотрудников и общее количество.
    """
    # Получаем всех активных сотрудников, отсортированных по дате найма (новые - первыми)
    all_employees_qs = CustomUser.objects.filter(is_active=True).order_by('-hire_date')

    # Получаем 4-х последних сотрудников
    recent_employees = all_employees_qs[:4]

    # Для каждого из них вычисляем стаж в днях и добавляем как атрибут
    for emp in recent_employees:
        emp.tenure_days = (date.today() - emp.hire_date).days

    context = {
        # Задача 1.1: Общее количество сотрудников
        'total_employees': all_employees_qs.count(),

        # Задача 1.2: Последние 4 сотрудника со стажем
        'recent_employees': recent_employees,

        # Передаем текущую дату (опционально, для других нужд)
        'today': date.today(),
    }

    return render(request, 'home.html', context)


# --- 2. Список сотрудников ---
def employee_list(request):
    """
    Страница со списком всех сотрудников.
    Задача: Пагинация по 10.
    """
    employees_list = CustomUser.objects.filter(is_active=True).order_by('last_name')

    # Задача 2.1: Пагинация по 10 сотрудников на страницу
    paginator = Paginator(employees_list, 10)
    page_number = request.GET.get('page')
    employees = paginator.get_page(page_number)

    # Вычисляем стаж для каждого сотрудника на текущей странице
    for emp in employees:
        emp.tenure_days = (date.today() - emp.hire_date).days

    context = {
        'employees': employees,
        'today': date.today(),
    }

    return render(request, 'employee_list.html', context)


# --- 3. Подробная карточка сотрудника ---
@login_required(login_url='/login/')
def employee_detail(request, pk):
    """
    Подробная информация о конкретном сотруднике.
    Задача: Вывести все данные + стаж + фото.
    """
    employee = get_object_or_404(CustomUser, pk=pk)

    skills = employee.employeeskill_set.select_related('skill').all()

    # Получаем все фото сотрудника в правильном порядке
    photos_qs = employee.photos.all().order_by('order_number')

    # Задача 3.2: Стаж в днях
    tenure_days = (date.today() - employee.hire_date).days

    context = {
        'employee': employee,
        'skills': skills,

        # Задача 3.2: Заглавное фото (первое в галерее)
        'main_photo': photos_qs.first(),

        # Задача 3.2: Галерея без первого фото
        'gallery_photos': photos_qs[1:] if photos_qs.count() > 1 else None,

        # Задача 3.2: Стаж в днях (передаем в шаблон)
        'tenure_days': tenure_days,

        # Задача 3.2: Номер стола (если есть)
        'workplace': getattr(employee, 'assigned_workplace', None),

        'today': date.today(),
    }

    return render(request, 'employee_detail.html', context)


# --- 4. Страница профиля ---
@login_required(login_url='/login/')
def profile(request):
    """
    Страница профиля текущего пользователя.
    Исправляет ошибку AttributeError.
    """
    return render(request, 'profile.html')